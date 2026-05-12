"""CogOS MCP Server — exposes CogOS as an MCP tool server.

Registers with AI tools (Claude Code, Codex CLI, Gemini CLI, etc.)
so they can call CogOS directly without any configuration files.

Usage:
    python -m cog.mcp_server          # run standalone
    cog mcp                            # run via CLI
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cogos")

_kernel = None


def _get_kernel():
    global _kernel
    if _kernel is not None:
        return _kernel
    from cog.config import build_config
    from cog.kernel import Kernel

    config = build_config()
    kernel = Kernel(config)
    kernel.start()
    _kernel = kernel
    return kernel


@mcp.tool()
def cog_run(task: str, path: str | None = None) -> str:
    """Run a cognitive task using CogOS multi-agent orchestration.

    Use this for any complex coding task: building features, debugging,
    refactoring, deploying, or analyzing code. CogOS plans the task,
    routes to the right domain modules (38 available), and orchestrates
    specialized agents to complete it.

    Args:
        task: What you want done. Be specific. Examples:
            "Build a REST API with user auth using Express and PostgreSQL"
            "Debug why the login test is failing in tests/auth.test.py"
            "Refactor the DatabaseManager class to use connection pooling"
            "Deploy this service to AWS ECS with auto-scaling"
        path: Working directory for the task. Defaults to current directory.
    """
    kernel = _get_kernel()
    context = {}
    if path:
        context["path"] = path
    result = kernel.run(task, context=context)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def cog_chat(message: str) -> str:
    """Send a chat message to CogOS for an interactive conversation.

    Use for follow-up questions, exploring ideas, or getting explanations.
    Maintains conversation context across calls.

    Args:
        message: Your message or question to CogOS.
    """
    kernel = _get_kernel()
    result = kernel.chat(message)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def cog_status() -> str:
    """Show CogOS system status: active modules, registered tools, provider info.

    Call this to see what CogOS has available before running a task.
    Shows module count, tool list, and which AI provider is configured.
    """
    kernel = _get_kernel()
    modules = kernel.modules.all()
    active = [m for m in modules.values() if m.state.value == "active"]
    tools = kernel.tools
    config = kernel.config

    status = {
        "version": "0.1.0",
        "modules": {
            "discovered": len(modules),
            "active": len(active),
            "names": [m.name for m in active],
        },
        "tools": {
            "count": len(tools),
            "names": sorted(tools.keys()),
        },
        "provider": {
            "name": config.provider,
            "model": config.model,
            "memory_backend": config.memory_backend,
        },
        "running": True,
    }
    return json.dumps(status, indent=2, default=str)


@mcp.tool()
def cog_modules(query: str | None = None) -> str:
    """List available CogOS domain modules and their capabilities.

    Each module provides prompt extensions, tools, and verifiers for its
    technology (Python, AWS, Docker, Kubernetes, etc.). Use this to discover
    what expertise CogOS can bring to your task.

    Args:
        query: Optional filter. Pass a keyword like "python", "aws", "docker"
            to find relevant modules.
    """
    kernel = _get_kernel()
    modules = kernel.modules.all()
    results = []
    for mod in modules.values():
        info = {
            "name": mod.name,
            "state": mod.state.value,
            "capabilities": mod.capabilities,
            "version": mod.version,
        }
        if mod.error:
            info["error"] = mod.error
        if query and query.lower() not in mod.name.lower():
            has_match = any(
                query.lower() in c.lower() for c in mod.capabilities
            )
            if not has_match:
                continue
        results.append(info)
    return json.dumps(results, indent=2, default=str)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
