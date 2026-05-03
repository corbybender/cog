from __future__ import annotations

import json
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]


@dataclass
class LLMMessage:
    role: MessageRole
    content: str | None = None
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None
    name: str | None = None


@dataclass
class LLMResponse:
    content: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    finish_reason: str = ""
    model: str = ""
    usage: dict[str, int] = field(default_factory=dict)

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0

    @property
    def is_empty(self) -> bool:
        return not self.content and not self.tool_calls


class ProviderToolResult:
    def __init__(self, tool_call_id: str, content: str, is_error: bool = False):
        self.tool_call_id = tool_call_id
        self.content = content
        self.is_error = is_error


StreamCallback = Callable[[str, str, dict[str, Any] | None], None]


class LLMProvider(ABC):
    @abstractmethod
    def complete(
        self,
        messages: list[LLMMessage],
        tools: list[ToolDefinition] | None = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system: str | None = None,
    ) -> LLMResponse: ...

    @abstractmethod
    def get_model_name(self) -> str: ...

    def complete_stream(
        self,
        messages: list[LLMMessage],
        tools: list[ToolDefinition] | None = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system: str | None = None,
        on_chunk: StreamCallback | None = None,
    ) -> LLMResponse:
        return self.complete(messages, tools, temperature, max_tokens, system)


def tool_def_from_dict(
    name: str, description: str, params: dict[str, Any]
) -> ToolDefinition:
    return ToolDefinition(name=name, description=description, parameters=params)


def tool_def_for(name: str, tool: Any) -> ToolDefinition:
    import inspect

    sig = inspect.signature(tool.execute)
    properties: dict[str, Any] = {}
    required: list[str] = []

    for pname, param in sig.parameters.items():
        if pname in ("self", "kwargs", "args"):
            continue
        prop: dict[str, Any] = {"type": "string"}
        if param.default is inspect.Parameter.empty:
            required.append(pname)
        properties[pname] = prop

    return ToolDefinition(
        name=name,
        description=tool.description if hasattr(tool, "description") else name,
        parameters={
            "type": "object",
            "properties": properties,
            "required": required,
        },
    )


def estimate_tokens(messages: list[LLMMessage]) -> int:
    total = 0
    for msg in messages:
        if msg.content:
            total += len(msg.content) // 4
        if msg.tool_calls:
            for tc in msg.tool_calls:
                total += len(json.dumps(tc.arguments)) // 4
    return total


def trim_messages(
    messages: list[LLMMessage], max_tokens: int = 80000
) -> list[LLMMessage]:
    if estimate_tokens(messages) <= max_tokens:
        return messages
    if len(messages) <= 2:
        return messages
    system_msgs = [m for m in messages if m.role == MessageRole.SYSTEM]
    rest = [m for m in messages if m.role != MessageRole.SYSTEM]
    kept: list[LLMMessage] = []
    budget = max_tokens
    for msg in reversed(rest):
        size = estimate_tokens([msg])
        if budget - size < max_tokens // 4:
            break
        kept.insert(0, msg)
        budget -= size
    return system_msgs + kept


def truncate_tool_output(output: str, max_chars: int = 8000) -> str:
    if len(output) <= max_chars:
        return output
    half = max_chars // 2 - 20
    return output[:half] + "\n\n... [truncated] ...\n\n" + output[-half:]
