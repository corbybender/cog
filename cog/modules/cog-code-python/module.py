from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult
from cog.verification.base import Verifier, VerificationResult, VerificationStatus


class PythonLintTool(Tool):
    name = "python.lint"
    description = "Run Python linting with ruff or flake8"
    required_permissions = ["shell.execute"]

    def execute(self, *args, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        path = kwargs.get("path", ".")
        shell = ShellTool()
        result = shell.execute(
            command=f"ruff check {path} --output-format concise", timeout=60
        )
        return result


class PythonTestTool(Tool):
    name = "python.test"
    description = "Run Python tests with pytest"
    required_permissions = ["shell.execute"]

    def execute(self, *args, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        path = kwargs.get("path", ".")
        shell = ShellTool()
        result = shell.execute(
            command=f"python -m pytest {path} -v --tb=short", timeout=120
        )
        return result


class PythonSyntaxVerifier(Verifier):
    name = "python.syntax"
    description = "Verify Python files compile without syntax errors"

    def verify(self, target, **kwargs) -> VerificationResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        result = shell.execute(command=f"python -m py_compile {target}", timeout=30)
        if result.success:
            return VerificationResult(
                verifier=self.name,
                status=VerificationStatus.PASSED,
                message=f"Syntax OK: {target}",
            )
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.FAILED,
            message=f"Syntax error in {target}",
            details={"error": result.error},
        )


class CogCodePython(CogModule):
    name = "cog-code-python"
    version = "1.0.0"
    description = "Python code reasoning module"

    def register_tools(self) -> list[Tool]:
        return [PythonLintTool(), PythonTestTool()]

    def register_verifiers(self) -> list[Verifier]:
        return [PythonSyntaxVerifier()]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "Python Expertise: You have deep knowledge of Python 3.11+, including "
            "type hints, dataclasses, async/await, pathlib, and modern Python patterns. "
            "Prefer modern idiomatic Python when writing or reviewing code."
        ]

    def get_capabilities(self) -> list[str]:
        return ["read_code", "write_code", "debug", "test", "lint"]


module = CogCodePython()
