from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult
from cog.verification.base import Verifier, VerificationResult, VerificationStatus


class CargoBuildTool(Tool):
    name = "cargo.build"
    description = "Build Rust project with Cargo"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", release: bool = False, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        release_flag = "--release" if release else ""
        command = f"cd {path} && cargo build {release_flag}"
        result = shell.execute(command=command, timeout=300)
        return result


class CargoTestTool(Tool):
    name = "cargo.test"
    description = "Run Rust tests with Cargo"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"cd {path} && cargo test"
        result = shell.execute(command=command, timeout=300)
        return result


class CargoCheckTool(Tool):
    name = "cargo.check"
    description = "Check Rust code without building"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"cd {path} && cargo check"
        result = shell.execute(command=command, timeout=180)
        return result


class RustClippyTool(Tool):
    name = "rust.clippy"
    description = "Run Rust linter Clippy"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"cd {path} && cargo clippy -- -D warnings"
        result = shell.execute(command=command, timeout=180)
        return result


class RustfmtTool(Tool):
    name = "rust.fmt"
    description = "Format Rust code with rustfmt"
    required_permissions = ["shell.execute"]

    def execute(self, path: str = ".", check: bool = False, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        check_flag = "--check" if check else ""
        command = f"cd {path} && cargo fmt {check_flag}"
        result = shell.execute(command=command, timeout=60)
        return result


class RustSyntaxVerifier(Verifier):
    name = "rust.syntax"
    description = "Verify Rust files compile without syntax errors"

    def verify(self, target, **kwargs) -> VerificationResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        # Use cargo check to verify syntax
        result = shell.execute(
            command=f"cd {target} && cargo check", timeout=60
        )
        if result.success:
            return VerificationResult(
                verifier=self.name,
                status=VerificationStatus.PASSED,
                message=f"Rust syntax OK: {target}",
            )
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.FAILED,
            message=f"Rust syntax error in {target}",
            details={"error": result.error},
        )


class CogCodeRust(CogModule):
    name = "cog-code-rust"
    version = "1.0.0"
    description = "Rust code reasoning and tooling module"

    def register_tools(self) -> list[Tool]:
        return [
            CargoBuildTool(),
            CargoTestTool(),
            CargoCheckTool(),
            RustClippyTool(),
            RustfmtTool(),
        ]

    def register_verifiers(self) -> list[Verifier]:
        return [RustSyntaxVerifier()]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## Rust Expertise",
            "You have deep knowledge of Rust including:",
            "- Ownership, borrowing, and lifetimes",
            "- Trait system and generics",
            "- Pattern matching and error handling",
            "- Cargo package management",
            "- Unsafe Rust and FFI",
            "- Concurrency with async/await",
            "- Zero-cost abstractions",
            "- Rust best practices and idioms",
            "",
            "When working with Rust code:",
            "- Respect ownership rules",
            "- Use Result<T, E> for error handling",
            "- Leverage the trait system",
            "- Prefer iterators over loops",
            "- Use cargo for building and testing",
        ]

    def get_capabilities(self) -> list[str]:
        return [
            "read_rust",
            "write_rust",
            "cargo_operations",
            "rust_analysis",
            "rust_testing",
            "rust_linting",
            "rust_formatting",
        ]


module = CogCodeRust()
