from __future__ import annotations

import tempfile
from pathlib import Path

from cog.kernel import Kernel, KernelConfig
from cog.memory import MemoryEntry, MemoryType, SQLiteMemoryBackend
from cog.module_loader import ModuleLoader
from cog.permissions import Permission, PermissionSet
from cog.planner import Planner
from cog.router import CapabilityRouter
from cog.tools.filesystem import FileReadTool, FileWriteTool, FileListTool
from cog.tools.shell import ShellTool
from cog.verification.base import VerificationLayer, VerificationStatus


class TestPermissions:
    def test_grant_and_check(self) -> None:
        ps = PermissionSet()
        ps.grant(Permission.FILESYSTEM_READ)
        assert ps.is_allowed(Permission.FILESYSTEM_READ)
        assert not ps.is_allowed(Permission.FILESYSTEM_WRITE)

    def test_revoke(self) -> None:
        ps = PermissionSet.all()
        ps.revoke(Permission.SHELL_EXECUTE)
        assert not ps.is_allowed(Permission.SHELL_EXECUTE)

    def test_check_raises(self) -> None:
        ps = PermissionSet.none()
        try:
            ps.check(Permission.FILESYSTEM_READ)
            assert False, "Should have raised"
        except PermissionError:
            pass


class TestMemory:
    def test_store_and_retrieve(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db = SQLiteMemoryBackend(f.name)
            entry = MemoryEntry(
                id="test-1",
                memory_type=MemoryType.SEMANTIC,
                content="Python is a programming language",
                tags=["python", "programming"],
            )
            db.store(entry)
            retrieved = db.retrieve("test-1")
            assert retrieved is not None
            assert retrieved.content == "Python is a programming language"
            assert retrieved.memory_type == MemoryType.SEMANTIC
            db.close()

    def test_search(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db = SQLiteMemoryBackend(f.name)
            for i in range(5):
                db.store(
                    MemoryEntry(
                        id=f"test-{i}",
                        memory_type=MemoryType.SEMANTIC,
                        content=f"Test entry about python number {i}",
                        tags=["test"],
                    )
                )
            results = db.search("python", limit=3)
            assert len(results) == 3
            db.close()

    def test_delete(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db = SQLiteMemoryBackend(f.name)
            db.store(
                MemoryEntry(
                    id="del-me", memory_type=MemoryType.TASK, content="delete this"
                )
            )
            assert db.retrieve("del-me") is not None
            assert db.delete("del-me")
            assert db.retrieve("del-me") is None
            db.close()


class TestFilesystemTools:
    def test_read_write(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("hello world")
            path = f.name

        read_tool = FileReadTool()
        result = read_tool.execute(path=path)
        assert result.success
        assert "hello world" in result.output

    def test_list(self) -> None:
        tool = FileListTool()
        result = tool.execute(path=".")
        assert result.success

    def test_write(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name

        tool = FileWriteTool()
        result = tool.execute(path=path, content="test content")
        assert result.success


class TestShellTool:
    def test_echo(self) -> None:
        tool = ShellTool()
        result = tool.execute(command="echo hello")
        assert result.success
        assert "hello" in result.output

    def test_dry_run(self) -> None:
        tool = ShellTool()
        result = tool.execute(command="echo hello", dry_run=True)
        assert result.success
        assert "DRY RUN" in result.output


class TestPlanner:
    def test_create_plan(self) -> None:
        planner = Planner()
        plan = planner.create_plan("inspect this repository and summarize architecture")
        assert len(plan.steps) > 0
        assert plan.status == "ready"

    def test_plan_progress(self) -> None:
        planner = Planner()
        plan = planner.create_plan("fix the bug")
        step = plan.current_step()
        assert step is not None
        assert step.status == "pending"


class TestRouter:
    def test_route_python(self) -> None:
        router = CapabilityRouter()
        result = router.route("write a python script")
        assert result.module is not None
        assert "python" in result.module or "code" in result.module

    def test_route_unknown(self) -> None:
        router = CapabilityRouter()
        result = router.route("do something")
        assert result is not None


class TestModuleLoader:
    def test_discover(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        discovered = loader.discover()
        assert len(discovered) >= 1
        names = [m.name for m in discovered]
        assert "cog-code-python" in names

    def test_load(self) -> None:
        loader = ModuleLoader(search_paths=["modules"])
        loader.discover()
        module = loader.load("cog-code-python")
        assert module.instance is not None


class TestVerification:
    def test_file_exists(self) -> None:
        vl = VerificationLayer()
        result = vl.verify("file.exists", "idea.md")
        assert result.status == VerificationStatus.PASSED

    def test_file_not_exists(self) -> None:
        vl = VerificationLayer()
        result = vl.verify("file.exists", "nonexistent.txt")
        assert result.status == VerificationStatus.FAILED


class TestKernel:
    def test_kernel_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = KernelConfig(
                modules_path="modules",
                memory_path=str(Path(tmpdir) / "test.db"),
                memory_backend="sqlite",
            )
            kernel = Kernel(config)
            kernel.start()
            assert kernel.memory is not None
            kernel.stop()

    def test_kernel_run_dry(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = KernelConfig(
                modules_path="modules",
                memory_path=str(Path(tmpdir) / "test.db"),
                dry_run=True,
                memory_backend="sqlite",
            )
            kernel = Kernel(config)
            result = kernel.run("inspect this repository", context={"path": "."})
            assert "plan" in result
            assert result["steps_total"] > 0
            kernel.stop()
