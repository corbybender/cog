#!/usr/bin/env python3
"""CogOS CLI - Command-line interface"""

import click
import json
from pathlib import Path
from typing import Dict, Any
import sys

sys.path.insert(0, str(Path(__file__).parent))

from cog.kernel import Kernel, KernelConfig
from cog.__init__ import __version__


@click.group()
@click.version_option(version=__version__)
def cli():
    """CogOS - Cognitive Operating System"""
    pass


@cli.command()
@click.argument("task", required=False)
@click.option("--modules", "-m", multiple=True, help="Modules to activate")
@click.option("--dry-run", "-n", is_flag=True, help="Show plan without executing")
@click.option("--chat", "mode", flag_value="chat", help="Interactive chat mode")
def run(task, modules, dry_run, mode):
    """Run a task with CogOS"""
    if mode or not task:
        _interactive_mode(modules)
        return

    config = KernelConfig(
        modules_path="modules",
        dry_run=dry_run,
        memory_backend="sqlite",
    )
    kernel = Kernel(config)
    result = kernel.run(task)
    click.echo(result.get("output", json.dumps(result, indent=2, default=str)))
    kernel.stop()


@cli.command()
@click.argument("project_name")
@click.option("--profile", "-p", type=click.Choice(["web-fullstack", "data-science", "devops", "mobile", "minimal"]), default="minimal")
def init(project_name, profile):
    """Initialize a new CogOS project"""
    project_path = Path(project_name)
    if project_path.exists():
        click.echo(f"Directory {project_name} already exists")
        return

    project_path.mkdir()
    cogos_dir = project_path / ".cogos"
    cogos_dir.mkdir()

    config = {
        "project": {"name": project_name, "profile": profile},
        "modules": [],
        "settings": {"cache_enabled": True, "auto_improve": True}
    }
    (cogos_dir / "config.json").write_text(json.dumps(config, indent=2))
    click.echo(f"Project {project_name} initialized!")


@cli.command()
def status():
    """Show CogOS status"""
    config = KernelConfig(modules_path="modules", memory_backend="sqlite")
    kernel = Kernel(config)
    kernel.start()
    tools = kernel.tools
    click.echo(f"CogOS v{__version__}")
    click.echo(f"Modules discovered: {len(kernel.modules.discover())}")
    click.echo(f"Tools registered: {len(tools)}")
    click.echo(f"Memory backend: {config.memory_backend}")
    kernel.stop()


@cli.command()
def chat():
    """Interactive chat mode"""
    _interactive_mode()


def _interactive_mode(modules=()):
    config = KernelConfig(
        modules_path="modules",
        memory_backend="sqlite",
    )
    kernel = Kernel(config)
    kernel.start()
    click.echo(f"CogOS v{__version__} - Interactive mode (type 'exit' to quit)")
    while True:
        try:
            message = click.prompt("", default="", show_default=False)
            if message.lower() in ("exit", "quit"):
                break
            if not message.strip():
                continue
            result = kernel.chat(message)
            click.echo(result.get("content", ""))
        except (KeyboardInterrupt, EOFError):
            break
    kernel.stop()
    click.echo("Goodbye!")


if __name__ == "__main__":
    cli()
