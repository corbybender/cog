from __future__ import annotations

import tempfile
from pathlib import Path

from cog.cog_module import CogModule, HookContext
from cog.kernel import Kernel, KernelConfig
from cog.module_loader import ModuleLoader, ModuleState
from cog.tools.base import Tool, ToolResult
from cog.verification.base import Verifier, VerificationResult, VerificationStatus


class DemoTool(Tool):
    name = "demo.hello"
    description = "Says hello"
    required_permissions = []

    def execute(self, *args, **kwargs) -> ToolResult:
        return ToolResult(success=True, output=f"hello {kwargs.get('name', 'world')}")


class DemoVerifier(Verifier):
    name = "demo.check"
    description = "A demo verifier"

    def verify(self, target, **kwargs) -> VerificationResult:
        return VerificationResult(
            verifier=self.name,
            status=VerificationStatus.PASSED,
            message=f"Checked: {target}",
        )


class DemoModule(CogModule):
    name = "demo-module"
    version = "0.1.0"
    description = "A test module"
    _loaded = False
    _unloaded = False

    def register_tools(self) -> list[Tool]:
        return [DemoTool()]

    def register_verifiers(self) -> list[Verifier]:
        return [DemoVerifier()]

    def get_prompt_extensions(self) -> list[str]:
        return ["Demo module knowledge: you have access to demo.hello tool."]

    def get_capabilities(self) -> list[str]:
        return ["demo", "test"]

    def on_load(self) -> None:
        DemoModule._loaded = True

    def on_unload(self) -> None:
        DemoModule._unloaded = True


class TestCogModuleABC:
    def test_default_methods(self) -> None:
        class MinimalModule(CogModule):
            name = "minimal"
            description = "minimal module"

        m = MinimalModule()
        assert m.register_tools() == []
        assert m.register_verifiers() == []
        assert m.get_prompt_extensions() == []
        assert m.get_capabilities() == []
        m.on_load()
        m.on_unload()

    def test_describe(self) -> None:
        m = DemoModule()
        d = m.describe()
        assert d["name"] == "demo-module"
        assert "demo.hello" in d["tools"]
        assert "demo.check" in d["verifiers"]
        assert d["capabilities"] == ["demo", "test"]
        assert d["prompt_extensions"] == 1

    def test_hook_context(self) -> None:
        ctx = HookContext(task="test task", context={"path": "."})
        assert ctx.task == "test task"
        assert ctx.result is None

        ctx.result = {"success": True}
        assert ctx.result["success"]

    def test_pre_post_hooks(self) -> None:
        m = DemoModule()
        ctx = HookContext(task="do something")
        ctx2 = m.pre_execute(ctx)
        assert ctx2.task == "do something"
        ctx3 = m.post_execute(ctx2)
        assert ctx3.task == "do something"


class TestModuleLoaderCogModule:
    def test_discover_cog_code_python(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        discovered = loader.discover()
        names = [m.name for m in discovered]
        assert "cog-code-python" in names
        assert "cog-git" in names

    def test_load_finds_cog_module(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        loader.discover()
        mod = loader.load("cog-code-python")
        assert mod.state == ModuleState.LOADED
        assert mod.cog_module is not None
        assert mod.cog_module.name == "cog-code-python"

    def test_load_cog_git(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        loader.discover()
        mod = loader.load("cog-git")
        assert mod.state == ModuleState.LOADED
        assert mod.cog_module is not None
        assert mod.cog_module.name == "cog-git"

    def test_activate_calls_on_load(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        loader.discover()
        mod = loader.activate("cog-code-python")
        assert mod.state == ModuleState.ACTIVE
        assert mod.cog_module is not None

    def test_unload_calls_on_unload(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        loader.discover()
        loader.activate("cog-code-python")
        assert loader.unload("cog-code-python")
        mod = loader.get("cog-code-python")
        assert mod is not None
        assert mod.state == ModuleState.UNLOADED
        assert mod.cog_module is None

    def test_get_tools_from_modules(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        loader.discover()
        loader.activate("cog-code-python")
        loader.activate("cog-git")
        tools = loader.get_tools()
        assert "python.lint" in tools
        assert "python.test" in tools
        assert "git.status" in tools
        assert "git.log" in tools
        assert "git.diff" in tools
        assert "git.branch" in tools

    def test_get_verifiers_from_modules(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        loader.discover()
        loader.activate("cog-code-python")
        verifiers = loader.get_verifiers()
        names = [v.name for v in verifiers]
        assert "python.syntax" in names

    def test_get_prompt_extensions(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        loader.discover()
        loader.activate("cog-code-python")
        loader.activate("cog-git")
        extensions = loader.get_prompt_extensions()
        assert len(extensions) == 2
        assert any("Python" in e for e in extensions)
        assert any("Git" in e for e in extensions)


class TestKernelModuleIntegration:
    def test_kernel_integrates_module_tools(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = KernelConfig(
                modules_path="modules",
                memory_path=str(Path(tmpdir) / "test.db"),
                memory_backend="sqlite",
            )
            kernel = Kernel(config)
            kernel.start()
            tools = kernel.tools
            assert "python.lint" in tools
            assert "python.test" in tools
            assert "git.status" in tools
            assert "git.log" in tools
            assert "filesystem.read" in tools
            kernel.stop()

    def test_kernel_integrates_module_verifiers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = KernelConfig(
                modules_path="modules",
                memory_path=str(Path(tmpdir) / "test.db"),
                memory_backend="sqlite",
            )
            kernel = Kernel(config)
            kernel.start()
            verifiers = kernel.verification.available_verifiers
            assert "python.syntax" in verifiers
            kernel.stop()

    def test_kernel_system_prompt_includes_modules(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = KernelConfig(
                modules_path="modules",
                memory_path=str(Path(tmpdir) / "test.db"),
                memory_backend="sqlite",
            )
            kernel = Kernel(config)
            kernel.start()
            prompt = kernel._build_system_prompt("test python code")
            assert "Module Knowledge" in prompt
            assert "Python" in prompt
            assert "Git" in prompt
            kernel.stop()

    def test_module_tools_are_functional(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        loader.discover()
        loader.activate("cog-code-python")
        tools = loader.get_tools()
        assert "python.lint" in tools
        lint_tool = tools["python.lint"]
        desc = lint_tool.describe()
        assert desc["name"] == "python.lint"

    def test_status_shows_all_tools(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = KernelConfig(
                modules_path="modules",
                memory_path=str(Path(tmpdir) / "test.db"),
                memory_backend="sqlite",
            )
            kernel = Kernel(config)
            kernel.start()
            tools = kernel.tools
            assert (
                len(tools) >= 9
            )  # 5 builtin + python.lint, python.test, git.status, git.log, git.diff, git.branch
            kernel.stop()
