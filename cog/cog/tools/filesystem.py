from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import Tool, ToolResult


class FileReadTool(Tool):
    name = "filesystem.read"
    description = "Read file contents from the filesystem"
    required_permissions = ["filesystem.read"]

    def execute(self, path: str, encoding: str = "utf-8", **kwargs: Any) -> ToolResult:
        try:
            p = Path(path).resolve()
            if not p.exists():
                return ToolResult(
                    success=False, output="", error=f"File not found: {path}"
                )
            if not p.is_file():
                return ToolResult(success=False, output="", error=f"Not a file: {path}")
            content = p.read_text(encoding=encoding)
            return ToolResult(
                success=True,
                output=content,
                metadata={"path": str(p), "size": p.stat().st_size},
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))


class FileWriteTool(Tool):
    name = "filesystem.write"
    description = "Write content to a file on the filesystem"
    required_permissions = ["filesystem.write"]

    def execute(
        self, path: str, content: str, encoding: str = "utf-8", **kwargs: Any
    ) -> ToolResult:
        try:
            p = Path(path).resolve()
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding=encoding)
            return ToolResult(
                success=True,
                output=f"Written {len(content)} bytes to {p}",
                metadata={"path": str(p), "size": len(content)},
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))


class FileListTool(Tool):
    name = "filesystem.list"
    description = "List files and directories"
    required_permissions = ["filesystem.read"]

    def execute(self, path: str = ".", pattern: str = "*", **kwargs: Any) -> ToolResult:
        try:
            p = Path(path).resolve()
            if not p.exists():
                return ToolResult(
                    success=False, output="", error=f"Path not found: {path}"
                )
            if not p.is_dir():
                return ToolResult(
                    success=False, output="", error=f"Not a directory: {path}"
                )
            entries = sorted(p.glob(pattern))
            lines = []
            for entry in entries:
                prefix = "D " if entry.is_dir() else "F "
                lines.append(f"{prefix}{entry.name}")
            return ToolResult(
                success=True,
                output="\n".join(lines),
                metadata={"path": str(p), "count": len(lines)},
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))


class FileSearchTool(Tool):
    name = "filesystem.search"
    description = "Search for files matching a glob pattern recursively"
    required_permissions = ["filesystem.read"]

    def execute(
        self, path: str = ".", pattern: str = "**/*", **kwargs: Any
    ) -> ToolResult:
        try:
            p = Path(path).resolve()
            if not p.exists():
                return ToolResult(
                    success=False, output="", error=f"Path not found: {path}"
                )
            if not p.is_dir():
                return ToolResult(
                    success=False, output="", error=f"Not a directory: {path}"
                )
            matches = sorted(p.glob(pattern))
            lines = [str(m.relative_to(p)) for m in matches if m.is_file()]
            return ToolResult(
                success=True,
                output="\n".join(lines),
                metadata={"path": str(p), "count": len(lines)},
            )
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))
