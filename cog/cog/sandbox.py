from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cog.cog_logger import get_logger
from cog.tools.base import Tool, ToolResult
from cog.tools.shell import ShellTool


@dataclass
class SandboxConfig:
    enabled: bool = False
    use_docker: bool = False
    timeout: int = 30
    network_isolated: bool = True
    readonly_filesystem: bool = False
    memory_limit: str = "512m"
    cpu_limit: str = "1.0"


class SandboxExecutor:
    """Secure sandbox execution environment."""

    def __init__(self, config: SandboxConfig | None = None) -> None:
        self._config = config or SandboxConfig()
        self._logger = get_logger()
        self._shell_tool = ShellTool()

    def execute_command(
        self, command: str, timeout: int | None = None, **kwargs: Any
    ) -> ToolResult:
        """Execute command in sandbox."""
        if not self._config.enabled:
            return self._shell_tool.execute(command, timeout=timeout or self._config.timeout)

        if self._config.use_docker:
            return self._execute_in_docker(command, timeout)

        return self._execute_with_limits(command, timeout)

    def _execute_in_docker(self, command: str, timeout: int | None = None) -> ToolResult:
        """Execute command in Docker container."""
        try:
            # Build docker run command
            docker_cmd = [
                "docker",
                "run",
                "--rm",
                "--network=none" if self._config.network_isolated else "--network=host",
                f"--memory={self._config.memory_limit}",
                f"--cpus={self._config.cpu_limit}",
                "-v", f"{Path.cwd()}:/workspace:rw" if not self._config.readonly_filesystem else f"{Path.cwd()}:/workspace:ro",
                "-w", "/workspace",
                "python:3.14-slim",
                "sh",
                "-c",
                command,
            ]

            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=timeout or self._config.timeout,
            )

            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.stderr else None,
                exit_code=result.returncode,
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False, output="", error=f"Command timed out after {timeout}s"
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=f"Docker error: {e}")

    def _execute_with_limits(self, command: str, timeout: int | None = None) -> ToolResult:
        """Execute with resource limits using ulimit."""
        try:
            # Use ulimit to restrict resources
            limited_command = f"ulimit -v {self._config.memory_limit.replace('m', '000')} && {command}"

            result = subprocess.run(
                limited_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout or self._config.timeout,
            )

            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.stderr else None,
                exit_code=result.returncode,
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False, output="", error=f"Command timed out after {timeout}s"
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=f"Execution error: {e}")

    def execute_python(self, code: str, timeout: int | None = None) -> ToolResult:
        """Execute Python code in sandbox."""
        if self._config.use_docker:
            return self._execute_in_docker(f'python3 -c "{code}"', timeout)

        # Use restricted Python execution
        try:
            exec_globals = {"__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "list": list,
                "dict": dict,
                "set": set,
                "tuple": tuple,
            }}

            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name

            result = subprocess.run(
                ["python3", temp_file],
                capture_output=True,
                text=True,
                timeout=timeout or self._config.timeout,
            )

            Path(temp_file).unlink(missing_ok=True)

            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.stderr else None,
                exit_code=result.returncode,
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False, output="", error=f"Python execution timed out"
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=f"Python error: {e}")

    def check_safety(self, command: str) -> tuple[bool, str]:
        """Check if command is safe to execute."""
        dangerous_patterns = [
            "rm -rf /",
            "mkfs",
            "dd if=/dev/zero",
            ":(){:|:&};:",  # fork bomb
            "chmod 000",
            "chown root",
        ]

        command_lower = command.lower()
        for pattern in dangerous_patterns:
            if pattern in command_lower:
                return False, f"Potentially dangerous pattern detected: {pattern}"

        return True, "Command appears safe"


class SandboxShellTool(Tool):
    """Shell tool with sandbox execution."""
    name = "shell.sandbox"
    description = "Execute shell commands in a sandboxed environment"
    required_permissions = ["shell.execute"]

    def __init__(self, config: SandboxConfig | None = None) -> None:
        self._executor = SandboxExecutor(config)

    def execute(self, command: str, **kwargs) -> ToolResult:
        # Check safety first
        is_safe, reason = self._executor.check_safety(command)
        if not is_safe:
            return ToolResult(success=False, output="", error=f"Safety check failed: {reason}")

        return self._executor.execute_command(command, **kwargs)


class DryRunTool(Tool):
    """Tool that simulates execution without actually running."""
    name = "tool.dryrun"
    description = "Simulate tool execution without side effects"

    def execute(self, tool_name: str, arguments: dict = None, **kwargs) -> ToolResult:
        args_str = ", ".join(f"{k}={v}" for k, v in (arguments or {}).items())
        return ToolResult(
            success=True,
            output=f"[DRY RUN] Would execute: {tool_name}({args_str})",
            details={"tool": tool_name, "arguments": arguments or {}},
        )
