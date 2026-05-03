from __future__ import annotations

import subprocess
from typing import Any

from .base import Tool, ToolResult


class ShellTool(Tool):
    name = "shell.execute"
    description = "Execute shell commands"
    required_permissions = ["shell.execute"]

    DESTRUCTIVE_PATTERNS = (
        "rm -rf",
        "del /",
        "format ",
        "mkfs.",
        "dd if=",
        "> /dev/",
        "shutdown",
        "reboot",
    )

    def execute(
        self,
        command: str,
        timeout: int = 120,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        dry_run: bool = False,
        **kwargs: Any,
    ) -> ToolResult:
        if dry_run:
            return self.dry_run(command=command)

        if self._is_destructive(command):
            return ToolResult(
                success=False,
                output="",
                error=f"Destructive command detected. Requires explicit approval: {command}",
                exit_code=-1,
            )

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env=env,
            )
            output = result.stdout
            if result.stderr:
                output += f"\n[STDERR]\n{result.stderr}"
            return ToolResult(
                success=result.returncode == 0,
                output=output.strip(),
                error=result.stderr.strip() if result.returncode != 0 else None,
                exit_code=result.returncode,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                output="",
                error=f"Command timed out after {timeout}s",
                exit_code=-1,
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e), exit_code=-1)

    def _is_destructive(self, command: str) -> bool:
        lower = command.lower().strip()
        return any(lower.startswith(p) for p in self.DESTRUCTIVE_PATTERNS)
