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

    provider_info = _detect_provider()

    if provider_info:
        config_content = _generate_config(**provider_info)
        if target.exists() and not args.force:
            print(f"{target} exists. Use --force to overwrite.")
        else:
            target.write_text(config_content)
            print(f"Created {target} with auto-detected provider:")
            print(f"  provider: {provider_info['provider']}")
            print(f"  model: {provider_info['model']}")
            base = provider_info.get("base_url")
            if base:
                print(f"  base_url: {base}")
    else:
        if target.exists() and not args.force:
            print(f"{target} exists. Use --force to overwrite.")
        else:
            content = _generate_template_config()
            target.write_text(content)
            print(f"Created {target}")
            print()
            _print_provider_setup_help()

    _register_all()
    _write_agents_md(Path("AGENTS.md"))

    print()
    print("CogOS is ready. Your AI tool will discover it automatically via MCP.")


def _detect_provider() -> dict | None:
    import os

    # 1. Check existing env vars
    provider = os.environ.get("COG_PROVIDER")
    model = os.environ.get("COG_MODEL")
    api_key = os.environ.get("COG_API_KEY")
    base_url = os.environ.get("COG_BASE_URL")

    if provider and model:
        return {
            "provider": provider,
            "model": model,
            "api_key": api_key or "ollama",
            "base_url": base_url,
        }

    # 2. Check OpenAI env
    if os.environ.get("OPENAI_API_KEY"):
        return {
            "provider": "openai",
            "model": os.environ.get("COG_MODEL", "gpt-4o"),
            "api_key": os.environ["OPENAI_API_KEY"],
            "base_url": os.environ.get("OPENAI_BASE_URL"),
        }

    # 3. Check Anthropic env
    if os.environ.get("ANTHROPIC_API_KEY"):
        return {
            "provider": "anthropic",
            "model": os.environ.get("COG_MODEL", "claude-sonnet-4-20250514"),
            "api_key": os.environ["ANTHROPIC_API_KEY"],
            "base_url": None,
        }

    # 4. Scan AI tool configs for provider info
    tool_provider = _scan_tool_configs()
    if tool_provider:
        return tool_provider

    # 5. Check for Ollama
    if _is_ollama_running():
        model_name = _get_ollama_default_model()
        return {
            "provider": "openai",
            "model": model_name,
            "api_key": "ollama",
            "base_url": "http://localhost:11434/v1",
        }

    return None


def _scan_tool_configs() -> dict | None:
    import json
    from pathlib import Path

    # opencode config has full provider details
    opencode_cfg = Path.home() / ".config" / "opencode" / "opencode.json"
    if opencode_cfg.exists():
        try:
            data = json.loads(opencode_cfg.read_text())
            providers = data.get("provider", {})
            for prov_name, prov_cfg in providers.items():
                opts = prov_cfg.get("options", {})
                base_url = opts.get("baseURL")
                api_key = opts.get("apiKey")
                models = prov_cfg.get("models", {})

                if base_url and models:
                    first_model = next(iter(models))
                    return {
                        "provider": "openai",
                        "model": first_model,
                        "api_key": api_key or "ollama",
                        "base_url": base_url,
                    }
        except Exception:
            pass

    # Cursor settings may have API key info
    cursor_settings = Path.home() / ".cursor" / "settings.json"
    if cursor_settings.exists():
        try:
            data = json.loads(cursor_settings.read_text())
            ai_key = data.get("aiKey") or data.get("apiKey")
            if ai_key and ai_key != "":
                return {
                    "provider": "openai",
                    "model": "gpt-4o",
                    "api_key": ai_key,
                    "base_url": None,
                }
        except Exception:
            pass

    # Check for LM Studio (common local dev setup)
    try:
        import urllib.request
        req = urllib.request.Request("http://localhost:1234/v1/models", method="GET")
        with urllib.request.urlopen(req, timeout=1) as resp:
            data = json.loads(resp.read())
            models = data.get("data", [])
            if models:
                model_id = models[0].get("id", "default")
                return {
                    "provider": "openai",
                    "model": model_id,
                    "api_key": "lm-studio",
                    "base_url": "http://localhost:1234/v1",
                }
    except Exception:
        pass

    return None


def _is_ollama_running() -> bool:
    import urllib.request
    import urllib.error

    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=1):
            return True
    except Exception:
        return False


def _get_ollama_default_model() -> str:
    import json
    import urllib.request

    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read())
            models = data.get("models", [])
            if models:
                return models[0].get("name", "llama3")
    except Exception:
        pass
    return "llama3"


def _generate_config(
    provider: str, model: str, api_key: str, base_url: str | None
) -> str:
    lines = [
        f"provider: {provider}",
        f"model: {model}",
        f"api_key: {api_key}",
    ]
    if base_url:
        lines.append(f"base_url: {base_url}")
    lines.extend([
        "",
        "# Per-agent overrides — each can have its own model",
        "agents:",
        "  planner:",
        "    provider: openai",
        "    model: gpt-4o-mini        # cheap model for task planning",
        "    api_key: YOUR_KEY_HERE",
        "",
        "  document_writer:",
        "    provider: openai",
        "    model: gpt-4o-mini        # cheap model for doc generation",
        "    api_key: YOUR_KEY_HERE",
        "",
        "  # executor — writes and runs code (uncomment to override host AI)",
        "  # executor:",
        "  #   provider: openai",
        "  #   model: gpt-4o",
        "  #   api_key: YOUR_KEY_HERE",
        "",
        "  # researcher — web search and analysis (uncomment to override host AI)",
        "  # researcher:",
        "  #   provider: openai",
        "  #   model: gpt-4o-mini",
        "  #   api_key: YOUR_KEY_HERE",
        "",
        "modules_path: modules",
        "memory_backend: sqlite",
        "memory_path: cog_memory.db",
        "log_level: INFO",
        "max_agent_iterations: 20",
    ])
    return "\n".join(lines) + "\n"


def _generate_template_config() -> str:
    return (
        "# CogOS Configuration\n"
        "# CogOS needs an LLM provider to run tasks (cog_run, cog_chat).\n"
        "# cog_status and cog_modules work without a provider.\n"
        "#\n"
        "# Option 1: OpenAI / any OpenAI-compatible API (Ollama, LM Studio, etc.)\n"
        "#   provider: openai\n"
        "#   model: gpt-4o\n"
        "#   api_key: sk-...\n"
        "#   base_url: https://api.openai.com/v1  # optional, for compatible APIs\n"
        "#\n"
        "# Option 2: Ollama (local, free)\n"
        "#   provider: openai\n"
        "#   model: llama3  # run 'ollama list' to see available models\n"
        "#   api_key: ollama\n"
        "#   base_url: http://localhost:11434/v1\n"
        "#\n"
        "# Option 3: Anthropic\n"
        "#   provider: anthropic\n"
        "#   model: claude-sonnet-4-20250514\n"
        "#   api_key: sk-ant-...\n"
        "#\n"
        "# Or set env vars: COG_PROVIDER, COG_MODEL, COG_API_KEY, COG_BASE_URL\n"
        "\n"
        "provider: openai\n"
        "model: gpt-4o\n"
        "api_key: YOUR_API_KEY_HERE\n"
        "\n"
        "# Per-agent overrides — each can have its own model\n"
        "agents:\n"
        "  planner:\n"
        "    provider: openai\n"
        "    model: gpt-4o-mini        # cheap model for task planning\n"
        "    api_key: YOUR_KEY_HERE\n"
        "\n"
        "  document_writer:\n"
        "    provider: openai\n"
        "    model: gpt-4o-mini        # cheap model for doc generation\n"
        "    api_key: YOUR_KEY_HERE\n"
        "\n"
        "  # executor — writes and runs code (uncomment to override host AI)\n"
        "  # executor:\n"
        "  #   provider: openai\n"
        "  #   model: gpt-4o\n"
        "  #   api_key: YOUR_KEY_HERE\n"
        "\n"
        "  # researcher — web search and analysis (uncomment to override host AI)\n"
        "  # researcher:\n"
        "  #   provider: openai\n"
        "  #   model: gpt-4o-mini\n"
        "  #   api_key: YOUR_KEY_HERE\n"
        "\n"
        "modules_path: modules\n"
        "memory_backend: sqlite\n"
        "memory_path: cog_memory.db\n"
        "log_level: INFO\n"
        "max_agent_iterations: 20\n"
    )


def _print_provider_setup_help() -> None:
    import os
    from pathlib import Path

    print("No LLM provider auto-detected. CogOS needs one to run tasks.")
    print("Pick the easiest option for your setup:")
    print()

    detected_tools = []
    if Path.home() / ".claude.json" in [Path.home() / ".claude.json"] if (Path.home() / ".claude.json").exists() else []:
        detected_tools.append("claude")
    if (Path.home() / ".codex" / "config.toml").exists():
        detected_tools.append("codex")
    if (Path.home() / ".gemini" / "settings.json").exists():
        detected_tools.append("gemini")

    if detected_tools:
        print(f"Detected: {', '.join(detected_tools)}")
        print("These tools use their own API keys internally — CogOS can't reuse them.")
        print()

    if _is_ollama_running():
        model_name = _get_ollama_default_model()
        print("EASIEST: Ollama is running! Just add to cog.yaml:")
        print(f"  provider: openai")
        print(f"  model: {model_name}")
        print(f"  api_key: ollama")
        print(f"  base_url: http://localhost:11434/v1")
        print()
        print("Or set env vars:")
        print(f"  export COG_PROVIDER=openai COG_MODEL={model_name} COG_API_KEY=ollama COG_BASE_URL=http://localhost:11434/v1")
    else:
        print("EASIEST: Use Ollama (free, local):")
        print("  1. Install: curl -fsSL https://ollama.com/install.sh | sh")
        print("  2. Run:     ollama pull llama3 && ollama serve")
        print("  3. Re-run:  cog init --force")
        print()
        print("Or edit cog.yaml with any OpenAI-compatible provider:")
        print("  provider: openai")
        print("  model: gpt-4o")
        print("  api_key: sk-...")
        print()
        print("Or set env vars: COG_PROVIDER, COG_MODEL, COG_API_KEY")

    print()
    print("(cog_status and cog_modules work without a provider — only cog_run needs one)")


_AGENTS_BLOCK_START = "<!-- cogos:start -->"
_AGENTS_BLOCK_END = "<!-- cogos:end -->"

_COG_AGENTS_BLOCK = f"""{_AGENTS_BLOCK_START}
# CogOS — Cognitive Operating System

CogOS is a library of 55 domain expert modules registered as an MCP server.

## How to use CogOS

For ANY coding task, call `cog_run(task="what you want done")`. It returns
relevant expert knowledge from modules (Docker, Kubernetes, TypeScript, React,
AWS, Python, Terraform, etc.). Use that expertise to complete the task correctly.

### MCP Tools
- `cog_run(task, path?)` — Get expert guidance for a task. Returns domain expertise from relevant modules.
- `cog_modules(query?)` — Browse available modules and capabilities.
- `cog_status()` — Check module count, active tools, system status.
- `cog_chat(message)` — Ask follow-up questions about domain topics.

### Example
```
// When asked to "deploy to Kubernetes with Helm"
cog_run("deploy Docker container to Kubernetes with Helm")
// Returns: K8s expertise (pods, services, Helm charts), Docker expertise,
// plus best practices and commands — use these to do the task right.
```

No LLM configuration needed — CogOS enriches YOU with domain knowledge.

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
    "opencode": {
        "file": "~/.config/opencode/opencode.json",
        "key": "mcp",
        "format": "opencode",
    },
    "cursor": {
        "file": ".cursor/mcp.json",
        "key": "mcpServers",
        "format": "json",
    },
    "vscode": {
        "file": ".vscode/mcp.json",
        "key": "servers",
        "format": "json",
    },
    "goose": {
        "file": "~/.config/goose/config.yaml",
        "key": "extensions",
        "format": "goose",
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
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            if cfg["format"] == "json":
                if not cfg_path.exists():
                    if tool_name in ("cursor", "vscode"):
                        _register_project_json(cfg_path, server_entry, tool_name, registered)
                    continue
                with open(cfg_path) as f:
                    data = json.load(f)
                servers = data.setdefault(cfg["key"], {})
                servers["cogos"] = server_entry
                with open(cfg_path, "w") as f:
                    json.dump(data, f, indent=2)
                registered.append(f"{tool_name} ({cfg_path})")
            elif cfg["format"] == "toml":
                _register_toml(cfg_path, server_entry, tool_name, registered)
            elif cfg["format"] == "opencode":
                _register_opencode(cfg_path, server_entry, tool_name, registered)
            elif cfg["format"] == "goose":
                _register_goose(cfg_path, server_entry, tool_name, registered)
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


def _register_opencode(
    cfg_path: Path, server_entry: dict, tool_name: str, registered: list
) -> None:
    import json as _json

    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    if cfg_path.exists():
        with open(cfg_path) as f:
            data = _json.load(f)
    else:
        data = {}
    mcp = data.setdefault("mcp", {})
    mcp["cogos"] = {
        "type": "local",
        "command": [server_entry["command"]] + server_entry["args"],
    }
    with open(cfg_path, "w") as f:
        _json.dump(data, f, indent=2)
    registered.append(f"{tool_name} ({cfg_path})")


def _register_project_json(
    cfg_path: Path, server_entry: dict, tool_name: str, registered: list
) -> None:
    import json as _json

    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    if cfg_path.exists():
        with open(cfg_path) as f:
            data = _json.load(f)
    else:
        data = {}
    key = _TOOL_CONFIGS[tool_name]["key"]
    servers = data.setdefault(key, {})
    servers["cogos"] = server_entry
    with open(cfg_path, "w") as f:
        _json.dump(data, f, indent=2)
    registered.append(f"{tool_name} ({cfg_path})")


def _register_goose(
    cfg_path: Path, server_entry: dict, tool_name: str, registered: list
) -> None:
    try:
        import yaml
    except ImportError:
        return
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    if cfg_path.exists():
        with open(cfg_path) as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    extensions = data.setdefault("extensions", [])
    ext_entry = {
        "name": "cogos",
        "type": "stdio",
        "cmd": server_entry["command"],
        "args": server_entry["args"],
    }
    for ext in extensions:
        if ext.get("name") == "cogos":
            return
    extensions.append(ext_entry)
    with open(cfg_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)
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
