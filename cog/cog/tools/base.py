from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:
    success: bool
    output: str
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    exit_code: int = 0


class Tool(ABC):
    name: str
    description: str
    required_permissions: list[str] = field(default_factory=list)

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> ToolResult: ...

    def dry_run(self, *args: Any, **kwargs: Any) -> ToolResult:
        return ToolResult(
            success=True,
            output=f"[DRY RUN] {self.name}: would execute with args {kwargs}",
        )

    def describe(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "required_permissions": self.required_permissions,
        }
