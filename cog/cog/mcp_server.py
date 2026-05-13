"""CogOS MCP Server — exposes CogOS as an MCP tool server.

Architecture: The calling AI tool (Claude Code, Cursor, opencode, etc.) IS the LLM.
CogOS does NOT need its own separate LLM provider. Instead, CogOS:

1. Discovers and loads 71 domain expert modules
2. When the AI calls cog_run(), CogOS finds relevant modules and returns
   their expertise as context for the AI to use
3. The AI then executes the task itself using that expertise

This means CogOS works with ANY AI tool, zero API key configuration needed.
The AI tool is already running — CogOS just makes it smarter.

Usage:
    python -m cog.mcp_server          # run standalone
    cog mcp                            # run via CLI
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

_PACKAGE_DIR = Path(__file__).resolve().parent
_PROJECT_DIR = _PACKAGE_DIR.parent

mcp = FastMCP(
    "cogos",
    instructions=(
        "You have access to CogOS — a library of 71 domain expert modules. "
        "Call cog_run(task) for ANY coding task. It returns relevant expert knowledge "
        "from modules like Docker, Kubernetes, TypeScript, React, AWS, etc. that you "
        "should follow when completing the task. Call cog_modules(query) to browse modules."
    ),
)

_kernel = None


def _get_kernel():
    global _kernel
    if _kernel is not None:
        return _kernel

    os.chdir(str(_PROJECT_DIR))
    from cog.config import build_config
    from cog.kernel import Kernel

    config = build_config()

    search_paths = [config.modules_path, str(_PACKAGE_DIR / "modules")]
    config.modules_path = search_paths[0]

    kernel = Kernel(config)
    kernel._module_loader._search_paths = [Path(p) for p in search_paths]

    try:
        kernel.start()
    except Exception:
        pass

    _kernel = kernel
    return kernel


def _find_relevant_modules(task: str, kernel) -> list[dict[str, Any]]:
    task_lower = task.lower()
    words = set(task_lower.split())
    bigrams = {f"{task_lower.split()[i]} {task_lower.split()[i+1]}"
               for i in range(len(task_lower.split()) - 1)}

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
                if name_lower.startswith(f"cog-{word}") or f"-{word}-" in name_lower or name_lower.endswith(f"-{word}"):
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
    return [item for _, item in scored[:5]]


def _get_module_expertise(mod_name: str, kernel) -> list[str]:
    for mod in kernel.modules.get_active():
        if mod.cog_module is None:
            continue
        if mod.name == mod_name or mod_name in mod.name.lower():
            return mod.cog_module.get_prompt_extensions()
    return []


@mcp.tool()
def cog_run(task: str, path: str | None = None) -> str:
    """Get expert guidance for a coding task. Returns relevant domain expertise from CogOS modules.

    Call this for ANY coding task. CogOS finds relevant expert modules (Docker, Kubernetes,
    TypeScript, React, AWS, Python, etc.) and returns their knowledge. Use this expertise
    to complete the task correctly following domain best practices.

    Args:
        task: What you want done. Examples: "Build a REST API with auth",
              "Debug failing Kubernetes deployment", "Optimize MongoDB queries",
              "Create a Next.js app with SSR", "Write Terraform for AWS"
        path: Working directory. Defaults to current directory.
    """
    kernel = _get_kernel()

    relevant = _find_relevant_modules(task, kernel)

    if not relevant:
        return json.dumps({
            "task": task,
            "modules_found": 0,
            "guidance": "No specific module matched. Proceed with general best practices.",
            "available_hints": [
                "Call cog_modules() to see all available modules",
                "Call cog_modules(query='docker') to search for specific topics",
            ],
        })

    all_expertise = []
    module_names = []
    for mod_info in relevant:
        expertise = _get_module_expertise(mod_info["name"], kernel)
        if expertise:
            all_expertise.extend(expertise)
            module_names.append(mod_info["name"])

    result = {
        "task": task,
        "modules_found": len(relevant),
        "relevant_modules": [
            {"name": m["name"], "description": m["description"], "relevance": m["relevance"]}
            for m in relevant
        ],
        "expertise": "\n".join(all_expertise) if all_expertise else "No expertise content found.",
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
    """Show CogOS status: active modules, registered tools, provider info.

    WHEN TO USE: To check if CogOS is properly configured, or when the user
    asks "what can cog do?" or "what modules are available?".

    Returns module count, tool count, and provider/model info.
    """
    kernel = _get_kernel()
    modules = kernel.modules.all()
    active = [m for m in modules.values() if m.state.value == "active"]
    tools = kernel.tools
    config = kernel.config

    provider_info = {
        "name": config.provider,
        "model": config.model,
        "status": "ready" if config.provider else "not needed (host AI is the LLM)",
    }

    status = {
        "version": "0.1.0",
        "modules": {
            "discovered": len(modules),
            "active": len(active),
            "names": sorted(m.name for m in active),
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
            has_match = any(
                query.lower() in c.lower() for c in mod.capabilities
            )
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

    Args:
        message: Your question or topic. Examples: "Tell me more about Docker multi-stage builds",
                 "What are the best practices for React Server Components?",
                 "How do I optimize this MongoDB aggregation pipeline?"
    """
    kernel = _get_kernel()

    relevant = _find_relevant_modules(message, kernel)

    all_expertise = []
    for mod_info in relevant:
        expertise = _get_module_expertise(mod_info["name"], kernel)
        if expertise:
            all_expertise.extend(expertise)

    if not all_expertise:
        return json.dumps({
            "response": "No specific module matched your question. Try cog_modules(query='...') to find relevant modules.",
        })

    return json.dumps({
        "relevant_modules": [m["name"] for m in relevant],
        "expertise": "\n".join(all_expertise),
    }, indent=2, default=str)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
