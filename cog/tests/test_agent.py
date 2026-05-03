from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from cog.agent import Agent, AgentConfig, AgentResult
from cog.kernel import Kernel, KernelConfig
from cog.permissions import PermissionSet
from cog.planner import Planner
from cog.providers.base import (
    LLMMessage,
    LLMProvider,
    LLMResponse,
    MessageRole,
    ToolCall,
    ToolDefinition,
)
from cog.providers.openai_provider import OpenAIProvider
from cog.providers.anthropic_provider import AnthropicProvider
from cog.router import CapabilityRouter
from cog.tools.filesystem import FileReadTool, FileListTool


class MockProvider(LLMProvider):
    def __init__(self, responses: list[LLMResponse] | None = None) -> None:
        self._responses = responses or []
        self._call_count = 0

    def complete(
        self,
        messages: list[LLMMessage],
        tools: list[ToolDefinition] | None = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system: str | None = None,
    ) -> LLMResponse:
        if self._call_count < len(self._responses):
            resp = self._responses[self._call_count]
            self._call_count += 1
            return resp
        return LLMResponse(content="done", finish_reason="stop")

    def get_model_name(self) -> str:
        return "mock-model"


class TestMockProvider:
    def test_simple_response(self) -> None:
        provider = MockProvider(
            [
                LLMResponse(content="Hello world", finish_reason="stop"),
            ]
        )
        resp = provider.complete(
            messages=[
                LLMMessage(role=MessageRole.USER, content="hi"),
            ]
        )
        assert resp.content == "Hello world"
        assert not resp.has_tool_calls

    def test_tool_call_response(self) -> None:
        provider = MockProvider(
            [
                LLMResponse(
                    content=None,
                    tool_calls=[
                        ToolCall(
                            id="tc1", name="filesystem.list", arguments={"path": "."}
                        ),
                    ],
                    finish_reason="tool_calls",
                ),
                LLMResponse(content="Here are the files: ...", finish_reason="stop"),
            ]
        )
        resp1 = provider.complete(
            messages=[
                LLMMessage(role=MessageRole.USER, content="list files"),
            ]
        )
        assert resp1.has_tool_calls
        assert resp1.tool_calls[0].name == "filesystem.list"

        resp2 = provider.complete(
            messages=[
                LLMMessage(
                    role=MessageRole.TOOL,
                    content="file1.py\nfile2.py",
                    tool_call_id="tc1",
                ),
            ]
        )
        assert resp2.content == "Here are the files: ..."

    def test_model_name(self) -> None:
        provider = MockProvider()
        assert provider.get_model_name() == "mock-model"


class TestAgent:
    def test_agent_simple_task(self) -> None:
        provider = MockProvider(
            [
                LLMResponse(content="The answer is 42", finish_reason="stop"),
            ]
        )
        tools = {"filesystem.read": FileReadTool()}
        agent = Agent(provider=provider, tools=tools)
        result = agent.run("What is the answer?")
        assert result.success
        assert "42" in result.output
        assert result.iterations == 1

    def test_agent_tool_calling(self) -> None:
        provider = MockProvider(
            [
                LLMResponse(
                    content=None,
                    tool_calls=[
                        ToolCall(
                            id="tc1", name="filesystem.list", arguments={"path": "."}
                        ),
                    ],
                ),
                LLMResponse(content="Found several files", finish_reason="stop"),
            ]
        )
        tools = {"filesystem.list": FileListTool()}
        agent = Agent(provider=provider, tools=tools)
        result = agent.run("list files in current directory")
        assert result.success
        assert result.iterations == 2
        assert len(result.steps) == 2
        assert result.steps[0].tool_call is not None
        assert result.steps[0].tool_call.name == "filesystem.list"

    def test_agent_unknown_tool(self) -> None:
        provider = MockProvider(
            [
                LLMResponse(
                    content=None,
                    tool_calls=[
                        ToolCall(id="tc1", name="nonexistent.tool", arguments={}),
                    ],
                ),
                LLMResponse(
                    content="Tool not available, here's what I know...",
                    finish_reason="stop",
                ),
            ]
        )
        tools = {"filesystem.list": FileListTool()}
        agent = Agent(provider=provider, tools=tools)
        result = agent.run("do something")
        assert result.success
        assert result.steps[0].tool_error is not None

    def test_agent_max_iterations(self) -> None:
        infinite_tool_calls = [
            LLMResponse(
                content=None,
                tool_calls=[
                    ToolCall(
                        id=f"tc{i}", name="filesystem.list", arguments={"path": "."}
                    ),
                ],
            )
            for i in range(30)
        ]
        provider = MockProvider(responses=infinite_tool_calls)
        tools = {"filesystem.list": FileListTool()}
        config = AgentConfig(max_iterations=5)
        agent = Agent(provider=provider, tools=tools, config=config)
        result = agent.run("keep going")
        assert not result.success
        assert result.iterations == 5

    def test_agent_provider_error(self) -> None:
        # Clear cache to avoid state pollution
        from cog.cache import get_cache
        cache = get_cache()
        cache._llm_cache.clear()

        failing = MagicMock(spec=LLMProvider)
        failing.complete.side_effect = RuntimeError("API down")
        failing.get_model_name.return_value = "failing"
        tools = {"filesystem.list": FileListTool()}
        agent = Agent(provider=failing, tools=tools)
        result = agent.run("do something")
        assert not result.success
        assert "API down" in result.output


class TestProviderConversion:
    def test_openai_provider_instantiation(self) -> None:
        with patch("cog.providers.openai_provider.openai") as mock_openai:
            mock_openai.OpenAI.return_value = MagicMock()
            provider = OpenAIProvider(model="gpt-4o", api_key="test-key")
            assert provider.get_model_name() == "gpt-4o"

    def test_anthropic_provider_instantiation(self) -> None:
        with patch("cog.providers.anthropic_provider.anthropic") as mock_anthropic:
            mock_anthropic.Anthropic.return_value = MagicMock()
            provider = AnthropicProvider(
                model="claude-sonnet-4-20250514", api_key="test-key"
            )
            assert provider.get_model_name() == "claude-sonnet-4-20250514"


class TestKernelAgent:
    def test_kernel_with_provider_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = KernelConfig(
                modules_path="modules",
                memory_path=str(Path(tmpdir) / "test.db"),
                provider="openai",
                model="gpt-4o",
                memory_backend="sqlite",
            )
            kernel = Kernel(config)
            kernel.start()
            assert kernel.provider is None
            kernel.stop()

    def test_kernel_dry_run_still_works(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = KernelConfig(
                modules_path="modules",
                memory_path=str(Path(tmpdir) / "test.db"),
                dry_run=True,
                memory_backend="sqlite",
            )
            kernel = Kernel(config)
            result = kernel.run("inspect this repository", context={"path": "."})
            assert result["dry_run"] is True
            assert result["success"]
            kernel.stop()

    def test_kernel_chat(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = KernelConfig(
                modules_path="modules",
                memory_path=str(Path(tmpdir) / "test.db"),
                memory_backend="sqlite",
            )
            kernel = Kernel(config)
            kernel.start()
            mock_provider = MockProvider(
                [
                    LLMResponse(content="Hello! How can I help?", finish_reason="stop"),
                ]
            )
            kernel._provider = mock_provider
            kernel._agent = Agent(
                provider=mock_provider,
                tools=kernel.tools,
            )
            resp = kernel.chat("hi")
            assert resp["content"] == "Hello! How can I help?"
            kernel.stop()


class TestAgentConfig:
    def test_default_config(self) -> None:
        config = AgentConfig()
        assert config.max_iterations == 20
        assert config.temperature == 0.1

    def test_custom_config(self) -> None:
        config = AgentConfig(max_iterations=10, temperature=0.5)
        assert config.max_iterations == 10
        assert config.temperature == 0.5


class TestLLMMessage:
    def test_message_roles(self) -> None:
        msg = LLMMessage(role=MessageRole.SYSTEM, content="You are helpful")
        assert msg.role == MessageRole.SYSTEM
        msg2 = LLMMessage(role=MessageRole.USER, content="Hello")
        assert msg2.role == MessageRole.USER
        msg3 = LLMMessage(
            role=MessageRole.ASSISTANT,
            content="Hi",
            tool_calls=[ToolCall(id="1", name="test", arguments={})],
        )
        assert msg3.tool_calls is not None

    def test_response_properties(self) -> None:
        resp = LLMResponse(content="test")
        assert not resp.has_tool_calls
        assert not resp.is_empty
        resp2 = LLMResponse()
        assert resp2.is_empty
        resp3 = LLMResponse(tool_calls=[ToolCall(id="1", name="t", arguments={})])
        assert resp3.has_tool_calls
