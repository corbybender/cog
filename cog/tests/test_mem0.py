from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from cog.kernel import Kernel, KernelConfig
from cog.memory.base import MemoryBackend, MemoryEntry, MemoryType
from cog.memory.mem0_backend import Mem0MemoryBackend


class MockMem0:
    def __init__(self) -> None:
        self._memories: list[dict[str, Any]] = []

    def add(
        self, messages, *, user_id=None, agent_id=None, metadata=None, infer=True, **kw
    ):
        content = messages if isinstance(messages, str) else str(messages)
        mem_id = f"mem-{len(self._memories)}"
        self._memories.append(
            {
                "id": mem_id,
                "memory": content,
                "metadata": metadata or {},
                "score": 0.95,
            }
        )
        return {"results": [{"id": mem_id, "memory": content, "event": "ADD"}]}

    def search(
        self,
        query,
        *,
        user_id=None,
        agent_id=None,
        limit=100,
        filters=None,
        threshold=None,
        rerank=True,
        **kw,
    ):
        results = self._memories[:limit]
        return {"results": results}

    def delete(self, memory_id):
        self._memories = [m for m in self._memories if m["id"] != memory_id]


class TestMem0Backend:
    def test_store_and_search(self) -> None:
        with patch("cog.memory.mem0_backend.Memory") as mock_cls:
            mock_cls.return_value = MockMem0()
            mock_cls.from_config.return_value = MockMem0()
            backend = Mem0MemoryBackend()

            entry = MemoryEntry(
                id="",
                memory_type=MemoryType.SEMANTIC,
                content="Python is a programming language",
                tags=["python"],
            )
            backend.store(entry)

            results = backend.search("Python", limit=5)
            assert len(results) >= 1

    def test_get_relevant_context(self) -> None:
        with patch("cog.memory.mem0_backend.Memory") as mock_cls:
            mock = MockMem0()
            mock_cls.return_value = mock
            mock_cls.from_config.return_value = mock

            backend = Mem0MemoryBackend()
            entry = MemoryEntry(
                id="",
                memory_type=MemoryType.SEMANTIC,
                content="User prefers dark mode",
                tags=["preference"],
            )
            backend.store(entry)

            context = backend.get_relevant_context("theme preference")
            assert "dark mode" in context

    def test_empty_context(self) -> None:
        with patch("cog.memory.mem0_backend.Memory") as mock_cls:
            mock_cls.return_value = MockMem0()
            mock_cls.from_config.return_value = MockMem0()
            backend = Mem0MemoryBackend()
            context = backend.get_relevant_context("nothing")
            assert context == ""

    def test_store_conversation(self) -> None:
        with patch("cog.memory.mem0_backend.Memory") as mock_cls:
            mock = MockMem0()
            mock_cls.return_value = mock
            mock_cls.from_config.return_value = mock
            backend = Mem0MemoryBackend()

            messages = [
                {"role": "user", "content": "I like Python"},
                {"role": "assistant", "content": "Noted, you prefer Python"},
            ]
            result = backend.store_conversation(messages)
            assert "results" in result

    def test_delete(self) -> None:
        with patch("cog.memory.mem0_backend.Memory") as mock_cls:
            mock = MockMem0()
            mock_cls.return_value = mock
            mock_cls.from_config.return_value = mock
            backend = Mem0MemoryBackend()

            entry = MemoryEntry(
                id="",
                memory_type=MemoryType.SEMANTIC,
                content="test memory",
            )
            backend.store(entry)
            assert backend.delete("mem-0")


class TestKernelMem0Integration:
    def test_kernel_starts_with_mem0(self) -> None:
        with patch("cog.memory.mem0_backend.Memory") as mock_cls:
            mock_cls.return_value = MockMem0()
            mock_cls.from_config.return_value = MockMem0()

            with tempfile.TemporaryDirectory() as tmpdir:
                config = KernelConfig(
                    modules_path="modules",
                    memory_path=str(Path(tmpdir) / "test.db"),
                    memory_backend="mem0",
                )
                kernel = Kernel(config)
                kernel.start()
                assert kernel.memory is not None
                assert isinstance(kernel.memory, Mem0MemoryBackend)
                kernel.stop()

    def test_kernel_starts_with_sqlite(self) -> None:
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

    def test_kernel_builds_system_prompt_with_memory(self) -> None:
        with patch("cog.memory.mem0_backend.Memory") as mock_cls:
            mock = MockMem0()
            mock_cls.return_value = mock
            mock_cls.from_config.return_value = mock

            config = KernelConfig(memory_backend="mem0")
            kernel = Kernel(config)
            kernel.start()

            entry = MemoryEntry(
                id="",
                memory_type=MemoryType.SEMANTIC,
                content="Project uses TypeScript with React",
            )
            kernel.memory.store(entry)

            prompt = kernel._build_system_prompt("what tech stack")
            assert "Relevant Memory" in prompt
            assert "TypeScript with React" in prompt
            kernel.stop()

    def test_kernel_builds_system_prompt_without_memory(self) -> None:
        config = KernelConfig(memory_backend="sqlite")
        kernel = Kernel(config)
        kernel.start()
        prompt = kernel._build_system_prompt("test task")
        assert "CogOS agent" in prompt
        kernel.stop()

    def test_search_memory(self) -> None:
        with patch("cog.memory.mem0_backend.Memory") as mock_cls:
            mock = MockMem0()
            mock_cls.return_value = mock
            mock_cls.from_config.return_value = mock

            config = KernelConfig(memory_backend="mem0")
            kernel = Kernel(config)
            kernel.start()

            entry = MemoryEntry(
                id="",
                memory_type=MemoryType.SEMANTIC,
                content="User prefers vim keybindings",
            )
            kernel.memory.store(entry)

            results = kernel.search_memory("vim")
            assert len(results) >= 1
            kernel.stop()
