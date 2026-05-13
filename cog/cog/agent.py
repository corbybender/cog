from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any, Callable

from cog.cache import get_cache
from cog.cog_logger import get_logger
from cog.permissions import Permission, PermissionSet
from cog.providers.base import (
    LLMMessage,
    LLMProvider,
    LLMResponse,
    MessageRole,
    StreamCallback,
    ToolCall,
    ToolDefinition,
    tool_def_for,
    trim_messages,
    truncate_tool_output,
)
from cog.tools.base import Tool, ToolResult


AGENT_SYSTEM_PROMPT = """You are a CogOS agent — a modular cognitive execution engine. You complete tasks by reasoning step-by-step and calling tools.

Rules:
- Analyze the task carefully before acting
- Use tools to gather information and make changes
- Verify your work when possible
- Be concise and accurate
- Report clear results
- If a task fails, explain why and suggest next steps
- Do NOT make destructive changes without explicit approval"""

MAX_ITERATIONS = 20
MAX_TOOL_RETRIES = 2
TOOL_OUTPUT_MAX_CHARS = 8000


@dataclass
class AgentConfig:
    max_iterations: int = MAX_ITERATIONS
    temperature: float = 0.1
    max_tokens: int = 4096
    system_prompt: str = AGENT_SYSTEM_PROMPT
    require_approval_for: set[str] = field(
        default_factory=lambda: {"filesystem.write", "shell.execute"}
    )
    max_tool_output_chars: int = TOOL_OUTPUT_MAX_CHARS
    max_tool_retries: int = MAX_TOOL_RETRIES
    max_context_tokens: int = 80000
    max_total_tokens: int = 0


@dataclass
class AgentStep:
    iteration: int
    thought: str | None = None
    tool_call: ToolCall | None = None
    tool_result: str | None = None
    tool_error: str | None = None
    retries: int = 0
    approved: bool = True


@dataclass
class AgentResult:
    success: bool
    output: str
    steps: list[AgentStep] = field(default_factory=list)
    total_tokens: int = 0
    iterations: int = 0
    cost_estimate: float = 0.0


class TokenTracker:
    def __init__(self, max_tokens: int = 0) -> None:
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        self._max = max_tokens

    def add(self, usage: dict[str, int]) -> None:
        self.prompt_tokens += usage.get("prompt_tokens", 0)
        self.completion_tokens += usage.get("completion_tokens", 0)
        self.total_tokens += usage.get("total_tokens", 0)

    @property
    def over_limit(self) -> bool:
        return self._max > 0 and self.total_tokens >= self._max

    def estimate_cost(self, model: str = "") -> float:
        if "gpt-4" in model and "mini" not in model:
            return (self.prompt_tokens * 0.00003) + (self.completion_tokens * 0.00006)
        if "claude" in model and "haiku" not in model:
            return (self.prompt_tokens * 0.000003) + (self.completion_tokens * 0.000015)
        return (self.prompt_tokens * 0.0000005) + (self.completion_tokens * 0.0000015)


ApprovalCallback = Callable[[str, dict[str, Any]], bool]


class Agent:
    def __init__(
        self,
        provider: LLMProvider,
        tools: dict[str, Tool],
        permissions: PermissionSet | None = None,
        config: AgentConfig | None = None,
    ) -> None:
        self._provider = provider
        self._tools = tools
        self._permissions = permissions or PermissionSet.all()
        self._config = config or AgentConfig()
        self._logger = get_logger()
        self._cache = get_cache()
        self._tool_defs = self._build_tool_defs()
        self._tracker = TokenTracker(max_tokens=self._config.max_total_tokens)
        self._approval_cb: ApprovalCallback | None = None
        self._on_step: Callable[[AgentStep], None] | None = None
        self._conversation: list[LLMMessage] = []
        self._stream_cb: StreamCallback | None = None

    def _build_tool_defs(self) -> list[ToolDefinition]:
        return [tool_def_for(name, tool) for name, tool in self._tools.items()]

    def set_approval_callback(self, cb: ApprovalCallback) -> None:
        self._approval_cb = cb

    def set_step_callback(self, cb: Callable[[AgentStep], None]) -> None:
        self._on_step = cb

    def set_stream_callback(self, cb: StreamCallback) -> None:
        self._stream_cb = cb

    @property
    def token_tracker(self) -> TokenTracker:
        return self._tracker

    def run(self, task: str, context: dict[str, Any] | None = None) -> AgentResult:
        self._logger.info("agent", f"Starting task: {task[:100]}")
        self._tracker = TokenTracker(max_tokens=self._config.max_total_tokens)

        messages: list[LLMMessage] = self._conversation.copy()
        context_str = ""
        if context:
            context_str = "\n\nAdditional context:\n"
            for k, v in context.items():
                context_str += f"- {k}: {v}\n"

        messages.append(
            LLMMessage(role=MessageRole.USER, content=f"{task}{context_str}")
        )

        result = AgentResult(success=False, output="")
        model = ""

        for i in range(self._config.max_iterations):
            if self._tracker.over_limit:
                result.output = (
                    f"Token limit reached ({self._tracker.total_tokens} tokens used)."
                )
                result.total_tokens = self._tracker.total_tokens
                result.iterations = i
                result.cost_estimate = self._tracker.estimate_cost(model)
                return result

            messages = trim_messages(messages, self._config.max_context_tokens)

            try:
                response = self._call_llm(messages)
            except Exception as e:
                self._logger.error("agent", f"Provider error: {e}")
                result.output = f"LLM provider error: {e}"
                result.iterations = i
                result.total_tokens = self._tracker.total_tokens
                return result

            model = response.model or model
            self._tracker.add(response.usage)

            if response.content:
                step = AgentStep(iteration=i, thought=response.content)
                result.steps.append(step)
                self._notify_step(step)

            if not response.has_tool_calls:
                self._conversation = messages + [
                    LLMMessage(role=MessageRole.ASSISTANT, content=response.content)
                ]
                result.success = True
                result.output = response.content or "Task completed with no output."
                result.total_tokens = self._tracker.total_tokens
                result.iterations = i + 1
                result.cost_estimate = self._tracker.estimate_cost(model)
                self._logger.info("agent", "Task completed")
                return result

            messages.append(
                LLMMessage(
                    role=MessageRole.ASSISTANT,
                    content=response.content,
                    tool_calls=response.tool_calls,
                )
            )

            for tc in response.tool_calls:
                tool_result = self._execute_with_retry(tc, i, result)
                truncated = truncate_tool_output(
                    tool_result.output
                    if tool_result.success
                    else f"Error: {tool_result.error}",
                    self._config.max_tool_output_chars,
                )
                messages.append(
                    LLMMessage(
                        role=MessageRole.TOOL,
                        content=truncated,
                        tool_call_id=tc.id,
                        name=tc.name,
                    )
                )

        self._conversation = messages
        result.output = "Max iterations reached without completion."
        result.total_tokens = self._tracker.total_tokens
        result.iterations = self._config.max_iterations
        result.cost_estimate = self._tracker.estimate_cost(model)
        self._logger.warning("agent", "Max iterations reached")
        return result

    def _call_llm(self, messages: list[LLMMessage]) -> LLMResponse:
        # Check cache for similar requests
        cached_response = self._cache.get_llm_response(messages, self._tool_defs)
        if cached_response and not self._stream_cb:
            self._logger.info("agent", "Using cached LLM response")
            return cached_response

        try:
            if self._stream_cb:
                response = self._provider.complete_stream(
                    messages=messages,
                    tools=self._tool_defs,
                    temperature=self._config.temperature,
                    max_tokens=self._config.max_tokens,
                    system=self._config.system_prompt,
                    on_chunk=self._stream_cb,
                )
            else:
                response = self._provider.complete(
                    messages=messages,
                    tools=self._tool_defs,
                    temperature=self._config.temperature,
                    max_tokens=self._config.max_tokens,
                    system=self._config.system_prompt,
                )

            # Cache the response
            if not self._stream_cb:
                self._cache.set_llm_response(messages, self._tool_defs, response)

            return response
        except Exception:
            # Don't cache on errors - let them propagate normally
            raise

    def _execute_with_retry(
        self, tc: ToolCall, iteration: int, result: AgentResult
    ) -> ToolResult:
        step = AgentStep(iteration=iteration, tool_call=tc)
        tool_result = self._execute_tool(tc)
        step.approved = tool_result.success or "Permission denied" not in (
            tool_result.error or ""
        )
        retries = 0

        while not tool_result.success and retries < self._config.max_tool_retries:
            retries += 1
            step.retries = retries
            self._logger.info("agent", f"Retrying {tc.name} (attempt {retries})")
            tool_result = self._execute_tool(tc)

        if tool_result.success:
            step.tool_result = tool_result.output
        else:
            step.tool_error = tool_result.error
        result.steps.append(step)
        self._notify_step(step)
        return tool_result

    def _execute_tool(self, tool_call: ToolCall) -> ToolResult:
        tool = self._tools.get(tool_call.name)
        if tool is None:
            return ToolResult(
                success=False, output="", error=f"Unknown tool: {tool_call.name}"
            )

        # Check cache for expensive tools
        cacheable_tools = ["filesystem.read", "web.fetch", "web.search"]
        if tool_call.name in cacheable_tools:
            cached = self._cache.get_tool_result(tool_call.name, tool_call.arguments)
            if cached is not None:
                self._logger.info("agent", f"Using cached result for {tool_call.name}")
                return cached

        if self._needs_approval(tool_call.name):
            if self._approval_cb and not self._approval_cb(
                tool_call.name, tool_call.arguments
            ):
                return ToolResult(
                    success=False,
                    output="",
                    error=f"Tool call {tool_call.name} was not approved by user.",
                )

        for perm_str in getattr(tool, "required_permissions", []):
            try:
                self._permissions.check(Permission(perm_str))
            except PermissionError as e:
                return ToolResult(success=False, output="", error=str(e))

        self._logger.info(
            "agent",
            f"Calling tool: {tool_call.name}({list(tool_call.arguments.keys())})",
        )
        try:
            result = tool.execute(**tool_call.arguments)

            # Cache successful results for expensive tools
            if tool_call.name in cacheable_tools and result.success:
                ttl = 600 if "web" in tool_call.name else 300  # 10 min for web, 5 for files
                self._cache.set_tool_result(tool_call.name, tool_call.arguments, result, ttl=ttl)

            return result
        except TypeError as e:
            self._logger.warning("agent", f"Tool arg error: {tool_call.name}: {e}")
            return ToolResult(
                success=False,
                output="",
                error=f"Invalid arguments for {tool_call.name}: {e}",
            )
        except Exception as e:
            self._logger.error("agent", f"Tool error: {tool_call.name}: {e}")
            return ToolResult(
                success=False, output="", error=f"{type(e).__name__}: {e}"
            )

    def _needs_approval(self, tool_name: str) -> bool:
        return tool_name in self._config.require_approval_for

    def _notify_step(self, step: AgentStep) -> None:
        if self._on_step:
            try:
                self._on_step(step)
            except Exception:
                pass

    def chat(self, messages: list[LLMMessage]) -> LLMResponse:
        return self._provider.complete(
            messages=messages,
            tools=self._tool_defs,
            temperature=self._config.temperature,
            max_tokens=self._config.max_tokens,
            system=self._config.system_prompt,
        )

    def get_conversation(self) -> list[LLMMessage]:
        return list(self._conversation)

    def clear_conversation(self) -> None:
        self._conversation.clear()
