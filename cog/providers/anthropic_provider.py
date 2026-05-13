from __future__ import annotations

import json
import os
from typing import Any

import anthropic

from .base import (
    LLMMessage,
    LLMProvider,
    LLMResponse,
    MessageRole,
    StreamCallback,
    ToolCall,
    ToolDefinition,
)


class AnthropicProvider(LLMProvider):
    def __init__(
        self,
        model: str = "claude-sonnet-4-20250514",
        api_key: str | None = None,
    ) -> None:
        self._model = model
        client_kwargs: dict[str, Any] = {}
        if api_key:
            client_kwargs["api_key"] = api_key
        elif os.environ.get("ANTHROPIC_API_KEY"):
            client_kwargs["api_key"] = os.environ["ANTHROPIC_API_KEY"]
        self._client = anthropic.Anthropic(**client_kwargs)

    def complete(
        self,
        messages: list[LLMMessage],
        tools: list[ToolDefinition] | None = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system: str | None = None,
    ) -> LLMResponse:
        api_messages = self._convert_messages(messages)
        kwargs: dict[str, Any] = {
            "model": self._model,
            "messages": api_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = self._convert_tools(tools)

        response = self._client.messages.create(**kwargs)

        content_text = ""
        tool_calls = []
        for block in response.content:
            if block.type == "text":
                content_text += block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=block.input if isinstance(block.input, dict) else {},
                    )
                )

        usage = {}
        if response.usage:
            usage = {
                "prompt_tokens": getattr(response.usage, "input_tokens", 0),
                "completion_tokens": getattr(response.usage, "output_tokens", 0),
            }

        return LLMResponse(
            content=content_text or None,
            tool_calls=tool_calls,
            finish_reason=response.stop_reason or "",
            model=response.model,
            usage=usage,
        )

    def get_model_name(self) -> str:
        return self._model

    def complete_stream(
        self,
        messages: list[LLMMessage],
        tools: list[ToolDefinition] | None = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system: str | None = None,
        on_chunk: StreamCallback | None = None,
    ) -> LLMResponse:
        api_messages = self._convert_messages(messages)
        kwargs: dict[str, Any] = {
            "model": self._model,
            "messages": api_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = self._convert_tools(tools)

        content_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        model = self._model
        finish_reason = ""

        try:
            with self._client.messages.stream(**kwargs) as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        if hasattr(event.delta, "text"):
                            content_parts.append(event.delta.text)
                            if on_chunk:
                                on_chunk("content", event.delta.text, None)
                    elif event.type == "message_stop":
                        finish_reason = "stop"
                message = stream.get_final_message()
                model = message.model or model
                for block in message.content:
                    if block.type == "tool_use":
                        tool_calls.append(
                            ToolCall(
                                id=block.id,
                                name=block.name,
                                arguments=block.input
                                if isinstance(block.input, dict)
                                else {},
                            )
                        )
                if message.stop_reason:
                    finish_reason = message.stop_reason
        except Exception:
            return self.complete(messages, tools, temperature, max_tokens, system)

        return LLMResponse(
            content="".join(content_parts) or None,
            tool_calls=tool_calls,
            finish_reason=finish_reason,
            model=model,
        )

    @staticmethod
    def _convert_messages(messages: list[LLMMessage]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                continue
            if msg.role == MessageRole.TOOL:
                result.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": msg.tool_call_id,
                                "content": msg.content or "",
                            }
                        ],
                    }
                )
            elif msg.tool_calls:
                content_blocks: list[dict[str, Any]] = []
                if msg.content:
                    content_blocks.append({"type": "text", "text": msg.content})
                for tc in msg.tool_calls:
                    content_blocks.append(
                        {
                            "type": "tool_use",
                            "id": tc.id,
                            "name": tc.name,
                            "input": tc.arguments,
                        }
                    )
                result.append({"role": "assistant", "content": content_blocks})
            else:
                result.append({"role": msg.role.value, "content": msg.content or ""})
        return result

    @staticmethod
    def _convert_tools(tools: list[ToolDefinition]) -> list[dict[str, Any]]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.parameters,
            }
            for t in tools
        ]
