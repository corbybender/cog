from __future__ import annotations

import argparse
import json
import sys

from cog.config import build_config, generate_default_config
from cog.kernel import Kernel, KernelConfig


def _build_config(args: argparse.Namespace, **overrides: object) -> KernelConfig:
    cli_overrides: dict = {
        "modules_path": getattr(args, "modules", None),
        "memory_path": getattr(args, "memory", None),
        "provider": getattr(args, "provider", None),
        "model": getattr(args, "model", None),
        "memory_backend": getattr(args, "memory_backend", None),
    }
    for k, v in list(cli_overrides.items()):
        if v is None:
            del cli_overrides[k]
    cli_overrides.update(overrides)
    return build_config(cli_overrides=cli_overrides)


def _make_stream_callback():
    import threading

    lock = threading.Lock()
    state = {"first": True}

    def on_chunk(kind: str, data: str, meta: object) -> None:
        with lock:
            if kind == "content":
                if state["first"]:
                    print()
                    state["first"] = False
                print(data, end="", flush=True)

    return on_chunk


def _make_approval_callback():
    def on_approval(tool_name: str, args: dict) -> bool:
        print(
            f"\n  [approval] {tool_name}({', '.join(f'{k}={v}' for k, v in args.items())})"
        )
        try:
            resp = input("  Allow? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False
        return resp in ("y", "yes")

    return on_approval


def cmd_run(args: argparse.Namespace) -> None:
    config = _build_config(args, dry_run=args.dry_run)
    kernel = Kernel(config)

    if not args.no_stream:
        kernel.set_stream_callback(_make_stream_callback())

    if config.require_approval:
        kernel.set_approval_callback(_make_approval_callback())

    def on_step(step: object) -> None:
        tc = getattr(step, "tool_call", None)
        if tc:
            name = getattr(tc, "name", "?")
            print(f"\n  [tool] {name}...", end="", flush=True)

    kernel.set_step_callback(on_step)

    try:
        result = kernel.run(args.task, context={"path": args.path})
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            _print_result(result, dry_run=args.dry_run)
    finally:
        kernel.stop()


def _print_result(result: dict, dry_run: bool = False) -> None:
    if dry_run and "plan" in result:
        print(result["plan"])
        print()
        print(
            f"Result: DRY RUN ({result['steps_completed']}/{result['steps_total']} steps)"
        )
        return

    status = "SUCCESS" if result["success"] else "FAILED"
    iterations = result.get("iterations", "?")
    tokens = result.get("total_tokens", 0)
    cost = result.get("cost_estimate", 0.0)

    print(f"\nResult: {status}")
    if tokens:
        cost_str = f" | Cost: ${cost:.4f}" if cost else ""
        print(f"Tokens: {tokens} | Iterations: {iterations}{cost_str}")
    print()

    output = result.get("output", "")
    if output:
        print(output)
    else:
        print("(no output)")

    steps = result.get("steps", [])
    if steps:
        print()
        print("Execution trace:")
        for s in steps:
            prefix = "  "
            if s.get("tool"):
                prefix += f"[{s['tool']}] "
            if s.get("thought"):
                print(f"{prefix}Thought: {s['thought'][:150]}")
            if s.get("result"):
                print(f"  Result: {s['result'][:150]}")
            if s.get("error"):
                print(f"  Error: {s['error']}")
            if s.get("retries"):
                print(f"  Retries: {s['retries']}")
            if not s.get("approved", True):
                print(f"  DENIED")


def cmd_chat(args: argparse.Namespace) -> None:
    config = _build_config(args)
    kernel = Kernel(config)
    kernel.start()
    print(f"CogOS Chat (model: {config.model}, memory: {config.memory_backend})")
    print("Type 'exit' or Ctrl+C to quit.")
    print()
    try:
        while True:
            try:
                user_input = input("you> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if user_input.lower() in ("exit", "quit"):
                break
            if not user_input:
                continue
            response = kernel.chat(user_input)
            if response.get("content"):
                print(f"cog> {response['content']}")
            if response.get("tool_calls"):
                for tc in response["tool_calls"]:
                    print(f"  [tool] {tc['name']}({tc['arguments']})")
            print()
    finally:
        kernel.stop()


def cmd_memory(args: argparse.Namespace) -> None:
    config = _build_config(args)
    kernel = Kernel(config)
    kernel.start()

    if args.memory_action == "search":
        results = kernel.search_memory(args.query, limit=args.limit)
        if not results:
            print("No memories found.")
        for entry in results:
            print(f"  [{entry.memory_type.value}] {entry.content[:200]}")
            if entry.confidence < 1.0:
                print(f"    confidence: {entry.confidence:.0%}")
    elif args.memory_action == "add":
        mem = kernel.memory
        if mem is None:
            print("Memory backend not initialized.")
            kernel.stop()
            return
        from cog.memory.base import MemoryEntry, MemoryType

        mem.store(
            MemoryEntry(
                id="",
                memory_type=MemoryType.SEMANTIC,
                content=args.content,
                tags=args.tags.split(",") if args.tags else [],
            )
        )
        print(f"Stored: {args.content[:100]}")
    elif args.memory_action == "list":
        results = kernel.search_memory("*", limit=args.limit)
        if not results:
            print("No memories found.")
        for entry in results:
            print(f"  [{entry.memory_type.value}] {entry.content[:200]}")
    else:
        print("Usage: cog memory [search|add|list]")

    kernel.stop()


def cmd_modules(args: argparse.Namespace) -> None:
    config = _build_config(args)
    kernel = Kernel(config)
    kernel.start()
    modules = kernel.modules.all()
    if not modules:
        print("No modules found.")
        return
    for mod in modules.values():
        state = mod.state.value
        caps = ", ".join(mod.capabilities) if mod.capabilities else "none"
        print(f"  {mod.name} ({state}) - {caps}")
        if mod.error:
            print(f"    Error: {mod.error}")
    kernel.stop()


def cmd_install(args: argparse.Namespace) -> None:
    config = _build_config(args)
    kernel = Kernel(config)
    kernel.start()

    try:
        entry = kernel.registry.get(args.module)
        if not entry:
            print(f"Module '{args.module}' not found in registry.")
            print("Use 'cog search <query>' to find available modules.")
            kernel.stop()
            return

        print(f"Installing {args.module} v{entry.version}")
        print(f"  Description: {entry.description}")
        print(f"  Author: {entry.author}")
        print(f"  Trust: {entry.trust_level.value}")

        if entry.dependencies:
            deps = ", ".join(entry.dependencies)
            print(f"  Dependencies: {deps}")

        if not args.yes:
            try:
                resp = input("Continue? [y/N] ").strip().lower()
                if resp not in ("y", "yes"):
                    print("Installation cancelled.")
                    kernel.stop()
                    return
            except (EOFError, KeyboardInterrupt):
                print("\nInstallation cancelled.")
                kernel.stop()
                return

        success = kernel.registry.install(args.module, modules_path=config.modules_path)
        if success:
            print(f"✓ Installed {args.module}")
            print("Run 'cog modules' to verify installation.")
        else:
            print(f"✗ Installation failed for {args.module}")
    finally:
        kernel.stop()


def cmd_search(args: argparse.Namespace) -> None:
    config = _build_config(args)
    kernel = Kernel(config)
    kernel.start()

    try:
        results = kernel.registry.search(args.query)
        if not results:
            print(f"No modules found matching '{args.query}'")
            kernel.stop()
            return

        print(f"Found {len(results)} module(s):\n")
        for entry in results:
            print(f"  {entry.name} v{entry.version}")
            print(f"    {entry.description}")
            print(f"    Author: {entry.author} | Trust: {entry.trust_level.value}")
            if entry.dependencies:
                print(f"    Dependencies: {', '.join(entry.dependencies)}")
            print()
    finally:
        kernel.stop()


def cmd_publish(args: argparse.Namespace) -> None:
    config = _build_config(args)
    kernel = Kernel(config)
    kernel.start()

    try:
        success = kernel.registry.publish(args.path)
        if success:
            print("✓ Module published to local registry")
            print("Use 'cog search <name>' to verify.")
        else:
            print("✗ Failed to publish module")
    finally:
        kernel.stop()


def cmd_verify(args: argparse.Namespace) -> None:
    config = _build_config(args)
    kernel = Kernel(config)
    kernel.start()
    result = kernel.verification.verify(args.verifier, args.target)
    print(f"[{result.status.value}] {result.verifier}: {result.message}")
    kernel.stop()


def cmd_status(args: argparse.Namespace) -> None:
    config = _build_config(args)
    kernel = Kernel(config)
    kernel.start()

    modules = kernel.modules.all()
    active = [m for m in modules.values() if m.state.value == "active"]
    tools = kernel.tools
    verifiers = kernel.verification.available_verifiers

    print("CogOS Status")
    print(f"  Modules: {len(active)} active / {len(modules)} discovered")
    print(f"  Tools: {', '.join(tools.keys())}")
    print(f"  Verifiers: {', '.join(verifiers)}")
    print(f"  Provider: {config.provider} ({config.model})")
    print(f"  Memory: {config.memory_backend}")
    mem = kernel.memory
    if mem:
        mem_type = type(mem).__name__
        print(f"  Memory backend: {mem_type}")

    kernel.stop()


def cmd_init(args: argparse.Namespace) -> None:
    from pathlib import Path

    target = Path(args.output)
    if target.exists() and not args.force:
        print(f"{target} already exists. Use --force to overwrite.")
        return
    content = generate_default_config()
    target.write_text(content)
    print(f"Created {target}")

    _register_all()
    _write_agents_md(Path("AGENTS.md"))

    print()
    print("CogOS is ready. Your AI tool will discover it automatically via MCP.")


_AGENTS_BLOCK_START = "<!-- cogos:start -->"
_AGENTS_BLOCK_END = "<!-- cogos:end -->"

_COG_AGENTS_BLOCK = f"""{_AGENTS_BLOCK_START}
# CogOS — Cognitive Operating System

CogOS is a modular cognitive runtime with 38 domain modules, 70 tools, and
multi-agent orchestration. It is registered as an MCP server in this project.

## How to Use

When the user mentions **cog**, **cogos**, or **CogOS**, call the `cog_run` MCP tool
with their task. Do NOT read CogOS source code — just call `cog_run` and it handles
planning, routing, and execution automatically.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `cog_run` | Run a cognitive task (primary tool) |
| `cog_chat` | Interactive conversation with CogOS |
| `cog_status` | Show active modules, tools, provider info |
| `cog_modules` | List/filter domain modules |

{_AGENTS_BLOCK_END}
"""


def _write_agents_md(agents_path: Path) -> None:
    if agents_path.exists():
        existing = agents_path.read_text()
        if _AGENTS_BLOCK_START in existing:
            print(f"AGENTS.md already has CogOS section (skipped)")
            return
        agents_path.write_text(_COG_AGENTS_BLOCK + "\n" + existing)
        print(f"Prepended CogOS info to {agents_path}")
    else:
        agents_path.write_text(_COG_AGENTS_BLOCK + "\n")
        print(f"Created {agents_path}")


def cmd_register(args: argparse.Namespace) -> None:
    _register_all()


def cmd_mcp(args: argparse.Namespace) -> None:
    from cog.mcp_server import main as mcp_main

    mcp_main()


_TOOL_CONFIGS = {
    "claude": {
        "file": "~/.claude.json",
        "key": "mcpServers",
        "format": "json",
    },
    "codex": {
        "file": "~/.codex/config.toml",
        "key": "mcp_servers",
        "format": "toml",
    },
    "gemini": {
        "file": "~/.gemini/settings.json",
        "key": "mcpServers",
        "format": "json",
    },
}


def _register_all() -> None:
    import json
    import shutil
    import sys
    from pathlib import Path

    python_path = shutil.which("python") or sys.executable
    server_entry = {
        "command": python_path,
        "args": ["-m", "cog.mcp_server"],
    }

    registered = []

    for tool_name, cfg in _TOOL_CONFIGS.items():
        cfg_path = Path(cfg["file"]).expanduser()
        if not cfg_path.exists():
            continue
        try:
            if cfg["format"] == "json":
                with open(cfg_path) as f:
                    data = json.load(f)
                servers = data.setdefault(cfg["key"], {})
                servers["cogos"] = server_entry
                with open(cfg_path, "w") as f:
                    json.dump(data, f, indent=2)
                registered.append(f"{tool_name} ({cfg_path})")
            elif cfg["format"] == "toml":
                _register_toml(cfg_path, server_entry, tool_name, registered)
        except Exception as e:
            print(f"  Warning: could not register with {tool_name}: {e}")

    if registered:
        print("Registered CogOS MCP server with:")
        for r in registered:
            print(f"  - {r}")
    else:
        print("No AI tool configs found. To register manually, add to your tool's MCP config:")
        print(f"  {json.dumps(server_entry, indent=4)}")


def _register_toml(
    cfg_path: Path, server_entry: dict, tool_name: str, registered: list
) -> None:
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    with open(cfg_path, "rb") as f:
        data = tomllib.load(f)

    lines = cfg_path.read_text().splitlines() if cfg_path.exists() else []
    section = "[mcp_servers.cogos]"
    entries = [
        f'command = "{server_entry["command"]}"',
        f'args = {json.dumps(server_entry["args"])}',
    ]
    if any(section in l for l in lines):
        return
    with open(cfg_path, "a") as f:
        f.write(f"\n{section}\n")
        for e in entries:
            f.write(f"{e}\n")
    registered.append(f"{tool_name} ({cfg_path})")


def cmd_create(args: argparse.Namespace) -> None:
    import json
    from pathlib import Path

    raw_name = args.name.strip().lower()
    if not raw_name.startswith("cog-"):
        raw_name = f"cog-{raw_name}"
    parts = raw_name.split("-")
    if len(parts) < 2:
        print("Module name must have a category, e.g. 'cog-cloud-aws' or 'cloud-aws'")
        return

    module_name = raw_name
    class_name = "".join(p.capitalize() for p in parts)
    tool_class = f"{class_name}Tool"
    verifier_class = f"{class_name}Verifier"
    category = parts[1]
    topic = "-".join(parts[2:]) if len(parts) > 2 else parts[1]
    description = args.description or f"{topic or category} module"

    output_dir = Path(args.output) / module_name
    if output_dir.exists() and not args.force:
        print(f"{output_dir} already exists. Use --force to overwrite.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "name": module_name,
        "version": "0.1.0",
        "description": description,
        "capabilities": [f"{topic}_operations"] if topic else [f"{category}_operations"],
        "requires": [],
        "permissions": ["shell.execute"],
        "entrypoint": "module.py",
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    module_py = f'''from __future__ import annotations

from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult
from cog.verification.base import Verifier, VerificationResult, VerificationStatus


class {tool_class}(Tool):
    name = "{module_name}.{topic}.run"
    description = "Run a {topic} operation"
    required_permissions = ["shell.execute"]

    def execute(self, command: str = "", **kwargs) -> ToolResult:
        # TODO: implement your tool logic here
        # Use ShellTool for CLI commands, or write custom logic
        from cog.tools.shell import ShellTool
        shell = ShellTool()
        if not command:
            return ToolResult(success=False, output="", error="No command provided")
        return shell.execute(command=command, timeout=60)


class {verifier_class}(Verifier):
    name = "{module_name}.{topic}.check"
    description = "Verify {topic} is available"

    def verify(self, target, **kwargs) -> VerificationResult:
        # TODO: implement a health check for your module
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.PASSED,
            message="{topic} is available",
        )


class {class_name}(CogModule):
    name = "{module_name}"
    version = "0.1.0"
    description = "{description}"

    def register_tools(self) -> list[Tool]:
        return [
            {tool_class}(),
        ]

    def register_verifiers(self) -> list[Verifier]:
        return [
            {verifier_class}(),
        ]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## {topic.capitalize()} Expertise",
            "You understand {topic} including:",
            "- Add your domain knowledge here",
            "- Best practices and common patterns",
            "- Security considerations",
        ]

    def get_capabilities(self) -> list[str]:
        return {manifest["capabilities"]}


module = {class_name}()
'''

    (output_dir / "module.py").write_text(module_py)

    print(f"Created {output_dir}/")
    print(f"  {output_dir / 'manifest.json'}")
    print(f"  {output_dir / 'module.py'}")
    print()
    print("Next steps:")
    print(f"  1. Edit {output_dir / 'module.py'} — add your tools and domain knowledge")
    print(f"  2. Edit {output_dir / 'manifest.json'} — add capabilities and permissions")
    print(f"  3. Run 'cog modules' to verify CogOS discovers your module")
    print(f"  4. Share: publish to a git repo or package as a pip-installable module")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="cog",
        description="CogOS - Cognitive Operating System",
    )
    parser.add_argument("--modules", default=None, help="Modules directory path")
    parser.add_argument("--memory", default=None, help="Memory database path")
    parser.add_argument(
        "--provider", default=None, help="LLM provider (openai, anthropic)"
    )
    parser.add_argument("--model", default=None, help="Model name")
    parser.add_argument(
        "--memory-backend",
        default=None,
        dest="memory_backend",
        help="Memory backend: mem0 or sqlite",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    init_parser = subparsers.add_parser("init", help="Create a cog.yaml config file")
    init_parser.add_argument("--output", default="cog.yaml", help="Output file path")
    init_parser.add_argument(
        "--force", action="store_true", help="Overwrite existing file"
    )

    run_parser = subparsers.add_parser("run", help="Run a cognitive task")
    run_parser.add_argument("task", help="The task to execute")
    run_parser.add_argument(
        "--path", default=".", help="Working directory for the task"
    )
    run_parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without execution"
    )
    run_parser.add_argument("--json", action="store_true", help="Output as JSON")
    run_parser.add_argument(
        "--no-stream", action="store_true", help="Disable streaming output"
    )

    chat_parser = subparsers.add_parser("chat", help="Interactive chat with the agent")

    memory_parser = subparsers.add_parser("memory", help="Manage agent memory")
    memory_parser.add_argument(
        "memory_action", choices=["search", "add", "list"], help="Memory action"
    )
    memory_parser.add_argument("--query", default="", help="Search query")
    memory_parser.add_argument("--content", default="", help="Content to add")
    memory_parser.add_argument("--tags", default="", help="Comma-separated tags")
    memory_parser.add_argument("--limit", type=int, default=10, help="Result limit")

    status_parser = subparsers.add_parser("status", help="Show system status")

    modules_parser = subparsers.add_parser("modules", help="List available modules")

    install_parser = subparsers.add_parser("install", help="Install a module from registry")
    install_parser.add_argument("module", help="Module name to install")
    install_parser.add_argument(
        "--yes", "-y", action="store_true", help="Skip confirmation prompt"
    )

    search_parser = subparsers.add_parser("search", help="Search module registry")
    search_parser.add_argument("query", help="Search query")

    publish_parser = subparsers.add_parser("publish", help="Publish module to registry")
    publish_parser.add_argument("path", default=".", help="Path to module directory")

    verify_parser = subparsers.add_parser("verify", help="Run a verification check")
    verify_parser.add_argument("verifier", help="Verifier name")
    verify_parser.add_argument("target", help="Target to verify")

    mcp_parser = subparsers.add_parser(
        "mcp", help="Run the MCP server (for AI tool integration)"
    )

    register_parser = subparsers.add_parser(
        "register", help="Register CogOS as an MCP server with your AI tools"
    )

    create_parser = subparsers.add_parser(
        "create", help="Scaffold a new CogOS module"
    )
    create_parser.add_argument(
        "name", help="Module name, e.g. 'cog-cloud-aws' or 'cloud-aws'"
    )
    create_parser.add_argument(
        "--description", "-d", default=None, help="Module description"
    )
    create_parser.add_argument(
        "--output", default="modules", help="Parent directory (default: modules/)"
    )
    create_parser.add_argument(
        "--force", action="store_true", help="Overwrite existing module directory"
    )

    args = parser.parse_args(argv)

    commands = {
        "init": cmd_init,
        "run": cmd_run,
        "chat": cmd_chat,
        "memory": cmd_memory,
        "modules": cmd_modules,
        "install": cmd_install,
        "search": cmd_search,
        "publish": cmd_publish,
        "verify": cmd_verify,
        "status": cmd_status,
        "mcp": cmd_mcp,
        "register": cmd_register,
        "create": cmd_create,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
