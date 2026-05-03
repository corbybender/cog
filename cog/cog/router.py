from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cog.module_loader import ModuleLoader


@dataclass
class RouteResult:
    module: str | None
    confidence: float
    alternatives: list[str] = field(default_factory=list)
    reasoning: str = ""


_CAPABILITY_MAP: dict[str, list[str]] = {
    "python": ["cog-code-python", "cog-code", "code-core"],
    "rust": ["cog-code-rust", "cog-code", "code-core"],
    "javascript": ["cog-code-js", "cog-code", "code-core"],
    "typescript": ["cog-code-ts", "cog-code", "code-core"],
    "powershell": ["cog-shell-powershell", "cog-shell", "tool-core"],
    "bash": ["cog-shell-linux", "cog-shell", "tool-core"],
    "shell": ["cog-shell", "tool-core"],
    "sql": ["cog-db-sql", "cog-db", "code-core"],
    "math": ["cog-math-algebra", "math-core"],
    "algebra": ["cog-math-algebra", "math-core"],
    "calculus": ["cog-math-calculus", "math-core"],
    "memory": ["cog-memory-vector", "memory-core"],
    "research": ["cog-web-research", "tool-core"],
    "web": ["cog-web-research", "tool-core"],
    "sitefinity": ["cog-sitefinity", "cog-dotnet", "code-core"],
    "dotnet": ["cog-dotnet", "code-core"],
    "code": ["cog-code", "code-core"],
    "test": ["cog-code", "code-core"],
    "debug": ["cog-code", "code-core"],
    "inspect": ["cog-code", "code-core"],
    "analyze": ["cog-code", "code-core"],
    "filesystem": ["tool-core"],
}


class CapabilityRouter:
    def __init__(self, module_loader: ModuleLoader | None = None) -> None:
        self._loader = module_loader

    def route(self, task: str, context: dict[str, Any] | None = None) -> RouteResult:
        words = task.lower().split()
        candidates: dict[str, float] = {}

        for word in words:
            for key, modules in _CAPABILITY_MAP.items():
                if key in word or word in key:
                    for i, mod in enumerate(modules):
                        candidates[mod] = candidates.get(mod, 0) + (1.0 / (i + 1))

        if self._loader:
            active = self._loader.get_active()
            for mod_name in list(candidates):
                if not any(m.name == mod_name for m in active):
                    candidates[mod_name] *= 0.5

        if not candidates:
            return RouteResult(
                module=None,
                confidence=0.0,
                reasoning="No matching capability found",
            )

        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        best_module = sorted_candidates[0][0]
        max_score = sorted_candidates[0][1]
        confidence = min(max_score / 3.0, 1.0)
        alternatives = [m for m, _ in sorted_candidates[1:4]]

        return RouteResult(
            module=best_module,
            confidence=confidence,
            alternatives=alternatives,
            reasoning=f"Matched based on keywords: {[w for w in words if any(w in k for k in _CAPABILITY_MAP)]}",
        )

    def route_step(self, action: str, description: str = "") -> RouteResult:
        combined = f"{action} {description}".strip()
        return self.route(combined)
