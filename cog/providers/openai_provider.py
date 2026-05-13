from __future__ import annotations

import json
import os
import sys
from typing import Any

import openai

from .base import (
    LLMMessage,
    LLMProvider,
    LLMResponse,
    MessageRole,
    StreamCallback,
    ToolCall,
    ToolDefinition,
)


class OpenAIProvider(LLMProvider):
    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self._model = model
        client_kwargs: dict[str, Any] = {}
        if api_key:
            client_kwargs["api_key"] = api_key
        elif os.environ.get("OPENAI_API_KEY"):
            client_kwargs["api_key"] = os.environ["OPENAI_API_KEY"]
        if base_url:
            client_kwargs["base_url"] = base_url
        self._client = openai.OpenAI(**client_kwargs)

    def complete(
        self,
        messages: list[LLMMessage],
        tools: list[ToolDefinition] | None = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system: str | None = None,
    ) -> LLMResponse:
        api_messages = self._convert_messages(messages, system)
        kwargs = self._build_kwargs(api_messages, tools, temperature, max_tokens)
        response = self._client.chat.completions.create(**kwargs)
        return self._parse_response(response)

    def complete_stream(
        self,
        messages: list[LLMMessage],
        tools: list[ToolDefinition] | None = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        system: str | None = None,
        on_chunk: StreamCallback | None = None,
    ) -> LLMResponse:
        api_messages = self._convert_messages(messages, system)
        kwargs = self._build_kwargs(api_messages, tools, temperature, max_tokens)
        kwargs["stream"] = True

        content_parts: list[str] = []
        tool_calls_map: dict[int, dict[str, Any]] = {}
        model = self._model
        finish_reason = ""

        try:
            stream = self._client.chat.completions.create(**kwargs)
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                if delta.content:
                    content_parts.append(delta.content)
                    if on_chunk:
                        on_chunk("content", delta.content, None)
                if delta.tool_calls:
                    for tc_chunk in delta.tool_calls:
                        idx = tc_chunk.index
                        if idx not in tool_calls_map:
                            tool_calls_map[idx] = {
                                "id": tc_chunk.id or "",
                                "name": "",
                                "arguments": "",
                            }
                        if tc_chunk.id:
                            tool_calls_map[idx]["id"] = tc_chunk.id
                        if tc_chunk.function:
                            if tc_chunk.function.name:
                                tool_calls_map[idx]["name"] = tc_chunk.function.name
                                if on_chunk:
                                    on_chunk("tool_call", tc_chunk.function.name, None)
                            if tc_chunk.function.arguments:
                                tool_calls_map[idx]["arguments"] += (
                                    tc_chunk.function.arguments
                                )
                if chunk.choices[0].finish_reason:
                    finish_reason = chunk.choices[0].finish_reason
                model = chunk.model or model
        except Exception:
            return self.complete(messages, tools, temperature, max_tokens, system)

        content = "".join(content_parts) or None
        tool_calls = []
        for idx in sorted(tool_calls_map):
            tc_data = tool_calls_map[idx]
            try:
                args = json.loads(tc_data["arguments"])
            except json.JSONDecodeError:
                args = {"raw": tc_data["arguments"]}
            tool_calls.append(
                ToolCall(id=tc_data["id"], name=tc_data["name"], arguments=args)
            )

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            finish_reason=finish_reason,
            model=model,
        )

    def get_model_name(self) -> str:
        return self._model

    def _build_kwargs(
        self,
        api_messages: list[dict[str, Any]],
        tools: list[ToolDefinition] | None,
        temperature: float,
        max_tokens: int,
    ) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": self._model,
            "messages": api_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            kwargs["tools"] = self._convert_tools(tools)
            kwargs["tool_choice"] = "auto"
        return kwargs

    def _parse_response(self, response: Any) -> LLMResponse:
        choice = response.choices[0]
        tool_calls = []
        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    args = {"raw": tc.function.arguments}
                tool_calls.append(
                    ToolCall(id=tc.id, name=tc.function.name, arguments=args)
                )
        usage = {}
        if response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        return LLMResponse(
            content=choice.message.content,
            tool_calls=tool_calls,
            finish_reason=choice.finish_reason or "",
            model=response.model,
            usage=usage,
        )

    @staticmethod
    def _convert_messages(
        messages: list[LLMMessage], system: str | None = None
    ) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        if system:
            result.append({"role": "system", "content": system})
        for msg in messages:
            if msg.tool_calls:
                d: dict[str, Any] = {
                    "role": "assistant",
                    "content": msg.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.name,
                                "arguments": json.dumps(tc.arguments),
                            },
                        }
                        for tc in msg.tool_calls
                    ],
                }
                result.append(d)
            elif msg.role == MessageRole.TOOL:
                result.append(
                    {
                        "role": "tool",
                        "tool_call_id": msg.tool_call_id,
                        "content": msg.content,
                    }
                )
            else:
                result.append({"role": msg.role.value, "content": msg.content})
        return result

    @staticmethod
    def _convert_tools(tools: list[ToolDefinition]) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                },
            }
            for t in tools
        ]
