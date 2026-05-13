from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class VerificationStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


@dataclass
class VerificationResult:
    verifier: str
    status: VerificationStatus
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


class Verifier(ABC):
    name: str
    description: str

    @abstractmethod
    def verify(self, target: Any, **kwargs: Any) -> VerificationResult: ...

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "description": self.description}


class ShellDryRunVerifier(Verifier):
    name = "shell.dry_run"
    description = "Verifies shell commands by running in dry-run mode"

    def verify(self, target: Any, **kwargs: Any) -> VerificationResult:
        if not isinstance(target, str):
            return VerificationResult(
                verifier=self.name,
                status=VerificationStatus.FAILED,
                message="Target must be a string command",
            )
        from cog.tools.shell import ShellTool

        tool = ShellTool()
        result = tool.execute(command=target, dry_run=True)
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.PASSED
            if result.success
            else VerificationStatus.FAILED,
            message=result.output,
            confidence=0.8,
        )


class FileExistsVerifier(Verifier):
    name = "file.exists"
    description = "Verifies that a file exists at the given path"

    def verify(self, target: Any, **kwargs: Any) -> VerificationResult:
        from pathlib import Path

        if not isinstance(target, str):
            return VerificationResult(
                verifier=self.name,
                status=VerificationStatus.FAILED,
                message="Target must be a file path string",
            )
        p = Path(target)
        exists = p.exists()
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.PASSED if exists else VerificationStatus.FAILED,
            message=f"File {'exists' if exists else 'not found'}: {target}",
            details={"path": str(p.resolve()), "exists": exists},
        )


class TestRunnerVerifier(Verifier):
    name = "test.runner"
    description = "Runs tests and verifies they pass"

    def verify(self, target: Any, **kwargs: Any) -> VerificationResult:
        if not isinstance(target, str):
            target = "pytest"
        from cog.tools.shell import ShellTool

        tool = ShellTool()
        result = tool.execute(command=target, timeout=kwargs.get("timeout", 300))
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.PASSED
            if result.success
            else VerificationStatus.FAILED,
            message=result.output[:500]
            if result.output
            else result.error or "No output",
            details={"exit_code": result.exit_code},
            confidence=1.0 if result.success else 0.0,
        )


class VerificationLayer:
    def __init__(self) -> None:
        self._verifiers: dict[str, Verifier] = {}
        self.register(ShellDryRunVerifier())
        self.register(FileExistsVerifier())
        self.register(TestRunnerVerifier())

    def register(self, verifier: Verifier) -> None:
        self._verifiers[verifier.name] = verifier

    def verify(
        self, verifier_name: str, target: Any, **kwargs: Any
    ) -> VerificationResult:
        verifier = self._verifiers.get(verifier_name)
        if verifier is None:
            return VerificationResult(
                verifier=verifier_name,
                status=VerificationStatus.FAILED,
                message=f"Unknown verifier: {verifier_name}",
            )
        return verifier.verify(target, **kwargs)

    def verify_all(self, checks: list[dict[str, Any]]) -> list[VerificationResult]:
        results = []
        for check in checks:
            check = dict(check)  # shallow copy to avoid mutating caller's dicts
            name = check.pop("verifier")
            target = check.pop("target")
            results.append(self.verify(name, target, **check))
        return results

    @property
    def available_verifiers(self) -> list[str]:
        return list(self._verifiers.keys())
