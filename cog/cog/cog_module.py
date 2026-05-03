from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from cog.tools.base import Tool
    from cog.verification.base import Verifier


@dataclass
class HookContext:
    task: str
    context: dict[str, Any] = field(default_factory=dict)
    result: dict[str, Any] | None = None


class CogModule(ABC):
    name: str
    version: str = "0.1.0"
    description: str = ""

    def register_tools(self) -> list[Tool]:
        return []

    def register_verifiers(self) -> list[Verifier]:
        return []

    def get_prompt_extensions(self) -> list[str]:
        return []

    def get_capabilities(self) -> list[str]:
        return []

    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass

    def pre_execute(self, ctx: HookContext) -> HookContext:
        return ctx

    def post_execute(self, ctx: HookContext) -> HookContext:
        return ctx

    def describe(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "tools": [t.name for t in self.register_tools()],
            "verifiers": [v.name for v in self.register_verifiers()],
            "capabilities": self.get_capabilities(),
            "prompt_extensions": len(self.get_prompt_extensions()),
        }
