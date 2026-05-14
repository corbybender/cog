"""CogOS MCP Server — exposes CogOS as an MCP tool server.

Architecture: The calling AI tool (Claude Code, Cursor, opencode, etc.) IS the LLM.
CogOS does NOT need its own separate LLM provider. Instead, CogOS:

1. Discovers and loads 55 domain expert modules
2. When the AI calls cog_run(), CogOS queries the ChunkIndex to find the most
   relevant individual prompt extensions and returns them as context
3. The AI then executes the task itself using that expertise

Token efficiency features (automatic, no config needed):
- Chunk-level scoring: returns the best individual extensions, not whole modules
- Session deduplication: chunks already returned this session are skipped
- Character budget: total expertise is capped at max_expertise_chars (default 6000)
- Module count: top-3 modules for browsing, chunk index for expertise retrieval

Usage:
    python -m cog.mcp_server          # run standalone
    cog mcp                            # run via CLI
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

_PACKAGE_DIR = Path(__file__).resolve().parent
_PROJECT_DIR = _PACKAGE_DIR.parent

mcp = FastMCP(
    "cogos",
    instructions=(
        "You have access to CogOS — a library of 55 domain expert modules. "
        "Call cog_run(task) for ANY coding task. It returns relevant expert knowledge "
        "from modules like Docker, Kubernetes, TypeScript, React, AWS, etc. that you "
        "should follow when completing the task. Call cog_modules(query) to browse modules."
    ),
)

_kernel = None
_chunk_index = None

# Session-level deduplication: chunk hashes returned this server process lifetime.
# Resets only when the MCP server process restarts (i.e. a new session).
_session_hashes: set[str] = set()


def _get_kernel():
    global _kernel
    if _kernel is not None:
        return _kernel

    os.chdir(str(_PROJECT_DIR))
    from cog.config import build_config
    from cog.kernel import Kernel

    config = build_config()

    search_paths = [config.modules_path]
    if config.modules_path != str(_PACKAGE_DIR / "modules"):
        search_paths.append(str(_PACKAGE_DIR / "modules"))

    kernel = Kernel(config)
    kernel._module_loader._search_paths = [Path(p) for p in search_paths]

    try:
        kernel.start()
    except Exception:
        pass

    _kernel = kernel
    return kernel


def _get_chunk_index():
    """Return the session-scoped ChunkIndex, building it on first call."""
    global _chunk_index
    if _chunk_index is not None and _chunk_index.built:
        return _chunk_index

    from cog.chunk_index import ChunkIndex
    kernel = _get_kernel()
    _chunk_index = ChunkIndex()
    _chunk_index.build(kernel)
    return _chunk_index


# ---------------------------------------------------------------------------
# Module-level browsing helper (used by cog_modules, NOT for expertise text)
# ---------------------------------------------------------------------------

_STOPWORDS = frozenset(
    "a an the to is are was were be been being have has had do does did "
    "will would shall should can could may might must of in on at by for "
    "with from and or but not no so if then than too very just that this "
    "it its i me my we our you your he him his she her they them their "
    "what which who whom how when where why all each every both few more "
    "most other some such only own same also about up out into over after".split()
)

_TECH_KEYWORDS = {
    "js": "javascript", "ts": "typescript", "k8s": "kubernetes",
    "docker": "docker", "container": "docker", "pod": "kubernetes",
    "deploy": "deploy", "api": "api", "rest": "api",
    "graphql": "graphql", "grpc": "grpc", "db": "database",
    "sql": "database", "postgres": "database", "mysql": "database",
    "mongo": "database", "redis": "database", "aws": "aws",
    "gcp": "gcp", "azure": "azure", "react": "react",
    "vue": "vue", "angular": "angular", "svelte": "svelte",
    "next": "nextjs", "nuxt": "nuxtjs", "python": "python",
    "rust": "rust", "go": "go", "java": "java", "php": "php",
    "ruby": "ruby", "swift": "swift", "kotlin": "kotlin",
    "css": "css", "html": "html", "git": "git",
    "terraform": "terraform", "ansible": "ansible",
    "helm": "kubernetes", "npm": "npm", "yarn": "yarn",
    "linux": "linux", "mac": "macos", "windows": "windows",
    "test": "testing", "playwright": "playwright", "selenium": "selenium",
}


def _tokenize(text: str) -> tuple[list[str], list[str]]:
    words = [w for w in text.lower().split() if w not in _STOPWORDS and len(w) > 1]
    bigrams = [f"{words[i]} {words[i + 1]}" for i in range(len(words) - 1)]
    return words, bigrams


def _find_relevant_modules(task: str, kernel, top_n: int = 3) -> list[dict[str, Any]]:
    """Score modules by name/capability/description match. Used for browsing only."""
    words, bigrams = _tokenize(task)

    expanded: set[str] = set()
    for w in words:
        expanded.add(w)
        mapped = _TECH_KEYWORDS.get(w)
        if mapped:
            expanded.add(mapped)
    words = list(expanded)

    scored: list[tuple[float, dict[str, Any]]] = []

    for mod in kernel.modules.get_active():
        if mod.cog_module is None:
            continue

        name_lower = mod.name.lower()
        caps = [c.lower() for c in mod.capabilities]
        desc = (mod.manifest.description or "").lower()

        score = 0.0
        for word in words:
            if word in name_lower:
                score += 5.0
                if (
                    name_lower.startswith(f"cog-{word}")
                    or f"-{word}-" in name_lower
                    or name_lower.endswith(f"-{word}")
                ):
                    score += 5.0
            for cap in caps:
                if word in cap:
                    score += 2.0
            if word in desc:
                score += 1.0
        for bigram in bigrams:
            if bigram in desc:
                score += 3.0
            if bigram in name_lower:
                score += 8.0
            for cap in caps:
                if bigram in cap:
                    score += 4.0

        if score > 0:
            scored.append((score, {
                "name": mod.name,
                "description": mod.manifest.description,
                "capabilities": mod.capabilities,
                "relevance": round(score, 1),
            }))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:top_n]]


# ---------------------------------------------------------------------------
# MCP tools
# ---------------------------------------------------------------------------

@mcp.tool()
def cog_run(task: str, path: str | None = None) -> str:
    """Get expert guidance for a coding task. Returns relevant domain expertise from CogOS modules.

    Call this for ANY coding task. CogOS finds relevant expert modules (Docker, Kubernetes,
    TypeScript, React, AWS, Python, etc.) and returns their knowledge. Use this expertise
    to complete the task correctly following domain best practices.

    Token-efficient: returns only the highest-scoring individual knowledge chunks,
    capped to a character budget, with session deduplication so repeated topics
    don't re-consume context.

    Args:
        task: What you want done. Examples: "Build a REST API with auth",
              "Debug failing Kubernetes deployment", "Optimize MongoDB queries",
              "Create a Next.js app with SSR", "Write Terraform for AWS"
        path: Working directory. Defaults to current directory.
    """
    kernel = _get_kernel()
    index = _get_chunk_index()
    max_chars = kernel.config.max_expertise_chars

    if not index.built or index.size == 0:
        # Chunk index empty — fall back to module-level metadata only
        relevant = _find_relevant_modules(task, kernel)
        if not relevant:
            return json.dumps({
                "task": task,
                "modules_found": 0,
                "guidance": "No specific module matched. Proceed with general best practices.",
            })
        return json.dumps({
            "task": task,
            "modules_found": len(relevant),
            "relevant_modules": relevant,
            "guidance": "Module index not yet built. Use module names above as domain context.",
        })

    chunks = index.query(task, max_chars=max_chars, exclude_hashes=_session_hashes)

    skipped = 0
    if not chunks:
        # Everything relevant was already returned this session
        skipped_check = index.query(task, max_chars=max_chars)
        skipped = len(skipped_check)
        if skipped:
            return json.dumps({
                "task": task,
                "note": (
                    f"All {skipped} relevant knowledge chunks were already returned "
                    "earlier in this session. Proceed using the expertise already in context."
                ),
            })
        return json.dumps({
            "task": task,
            "modules_found": 0,
            "guidance": "No specific module matched. Proceed with general best practices.",
        })

    # Register returned chunks for session deduplication
    for chunk in chunks:
        _session_hashes.add(chunk.hash)

    # Derive which modules contributed (for the AI's awareness)
    modules_hit: dict[str, int] = {}
    for chunk in chunks:
        modules_hit[chunk.module] = modules_hit.get(chunk.module, 0) + 1

    expertise_text = "\n\n".join(chunk.text for chunk in chunks)
    total_chars = len(expertise_text)

    result: dict[str, Any] = {
        "task": task,
        "chunks_returned": len(chunks),
        "chunks_skipped_dedup": skipped,
        "total_chars": total_chars,
        "modules_contributing": [
            {"name": name, "chunks": count}
            for name, count in sorted(modules_hit.items(), key=lambda x: -x[1])
        ],
        "expertise": expertise_text,
        "instructions": (
            "Use the expertise above to complete this task. Follow the domain-specific "
            "best practices, patterns, and commands from the relevant modules."
        ),
    }

    if path:
        result["working_directory"] = path

    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def cog_status() -> str:
    """Show CogOS status: active modules, chunk index size, token budget, provider info.

    WHEN TO USE: To check if CogOS is properly configured, or when the user
    asks "what can cog do?" or "what modules are available?".
    """
    kernel = _get_kernel()
    index = _get_chunk_index()
    modules = kernel.modules.all()
    active = [m for m in modules.values() if m.state.value == "active"]
    tools = kernel.tools
    config = kernel.config

    provider_info = {
        "name": config.provider,
        "model": config.model,
        "status": "ready" if config.provider and config.provider != "host" else "host AI is the LLM",
    }

    status = {
        "version": "0.1.0",
        "modules": {
            "discovered": len(modules),
            "active": len(active),
            "names": sorted(m.name for m in active),
        },
        "chunk_index": {
            "built": index.built,
            "total_chunks": index.size,
            "max_expertise_chars": config.max_expertise_chars,
            "session_chunks_returned": len(_session_hashes),
        },
        "tools": {
            "count": len(tools),
            "names": sorted(tools.keys()),
        },
        "provider": provider_info,
        "running": True,
        "architecture": "CogOS enriches the calling AI with domain expertise. No separate LLM needed.",
    }
    return json.dumps(status, indent=2, default=str)


@mcp.tool()
def cog_modules(query: str | None = None) -> str:
    """List CogOS domain modules (Python, AWS, Docker, Kubernetes, etc.).

    WHEN TO USE: When the user asks what modules or capabilities CogOS has,
    or when you need to check if CogOS supports a specific technology.

    Args:
        query: Optional filter keyword like "python", "aws", "docker".
    """
    kernel = _get_kernel()
    modules = kernel.modules.all()
    results = []
    for mod in modules.values():
        info = {
            "name": mod.name,
            "state": mod.state.value,
            "capabilities": mod.capabilities,
            "version": mod.manifest.version,
        }
        if mod.error:
            info["error"] = mod.error
        if query and query.lower() not in mod.name.lower():
            has_match = any(query.lower() in c.lower() for c in mod.capabilities)
            if not has_match:
                desc = (mod.manifest.description or "").lower()
                if query.lower() not in desc:
                    continue
        results.append(info)
    return json.dumps(results, indent=2, default=str)


@mcp.tool()
def cog_chat(message: str) -> str:
    """Ask CogOS a follow-up question about domain expertise.

    WHEN TO USE: After a cog_run, when you need more detail on a specific
    technology or pattern mentioned in the expert guidance.

    Uses the same chunk index and session deduplication as cog_run, so
    follow-up calls won't re-send expertise already in context.

    Args:
        message: Your question or topic. Examples: "Tell me more about Docker multi-stage builds",
                 "What are the best practices for React Server Components?",
                 "How do I optimize this MongoDB aggregation pipeline?"
    """
    kernel = _get_kernel()
    index = _get_chunk_index()
    max_chars = kernel.config.max_expertise_chars

    chunks = index.query(message, max_chars=max_chars, exclude_hashes=_session_hashes)

    if not chunks:
        return json.dumps({
            "response": (
                "No new expertise found — either no module matched or all relevant "
                "chunks were already returned this session. "
                "Try cog_modules(query='...') to find relevant modules."
            ),
        })

    for chunk in chunks:
        _session_hashes.add(chunk.hash)

    modules_hit = sorted({chunk.module for chunk in chunks})
    return json.dumps({
        "relevant_modules": modules_hit,
        "chunks_returned": len(chunks),
        "expertise": "\n\n".join(chunk.text for chunk in chunks),
    }, indent=2, default=str)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
