from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any, Callable

from cog.agent import Agent, AgentConfig, AgentResult, ApprovalCallback
from cog.cog_module import HookContext
from cog.logging import CogLogger, get_logger
from cog.memory import MemoryBackend, MemoryEntry, MemoryType
from cog.memory.mem0_backend import Mem0MemoryBackend
from cog.memory.sqlite_backend import SQLiteMemoryBackend
from cog.module_loader import ModuleLoader, ModuleState
from cog.permissions import Permission, PermissionSet
from cog.planner import Plan, PlanStep, Planner
from cog.providers.base import LLMMessage, LLMProvider, MessageRole, StreamCallback
from cog.registry import Registry
from cog.router import CapabilityRouter
from cog.tools import Tool, ToolResult
from cog.tools.filesystem import (
    FileListTool,
    FileReadTool,
    FileSearchTool,
    FileWriteTool,
)
from cog.tools.shell import ShellTool
from cog.tools.web import WebFetchTool, WebSearchTool
from cog.verification.base import VerificationLayer


@dataclass
class KernelConfig:
    modules_path: str = "modules"
    memory_path: str = "cog_memory.db"
    log_level: str = "INFO"
    sandbox_enabled: bool = False
    dry_run: bool = False
    provider: str | None = None
    model: str | None = None
    max_agent_iterations: int = 20
    memory_backend: str = "mem0"
    mem0_config: dict[str, Any] | None = None
    memory_user_id: str = "cogos-agent"
    memory_agent_id: str = "cogos"
    api_key: str | None = None
    base_url: str | None = None
    max_total_tokens: int = 0
    require_approval: bool = False
    stream: bool = True


class Kernel:
    def __init__(self, config: KernelConfig | None = None) -> None:
        self._config = config or KernelConfig()
        self._logger = get_logger()
        self._module_loader = ModuleLoader(search_paths=[self._config.modules_path])
        self._router = CapabilityRouter(self._module_loader)
        self._planner = Planner()
        self._registry = Registry()
        self._verification = VerificationLayer()
        self._tools: dict[str, Tool] = {}
        self._permissions = PermissionSet.all()
        self._memory: MemoryBackend | None = None
        self._provider: LLMProvider | None = None
        self._agent: Agent | None = None
        self._running = False
        self._module_prompt_extensions: list[str] = []
        self._approval_cb: ApprovalCallback | None = None
        self._stream_cb: StreamCallback | None = None
        self._on_step: Callable[[Any], None] | None = None

        self._register_builtin_tools()

    def _register_builtin_tools(self) -> None:
        for tool in [
            FileReadTool(),
            FileWriteTool(),
            FileListTool(),
            FileSearchTool(),
            ShellTool(),
            WebFetchTool(),
            WebSearchTool(),
        ]:
            self._tools[tool.name] = tool

    def _integrate_modules(self) -> None:
        module_tools = self._module_loader.get_tools()
        for name, tool in module_tools.items():
            self._tools[name] = tool
            self._logger.info("kernel", f"  Registered tool: {name} (from module)")
        module_verifiers = self._module_loader.get_verifiers()
        for v in module_verifiers:
            self._verification.register(v)
            self._logger.info(
                "kernel", f"  Registered verifier: {v.name} (from module)"
            )
        self._module_prompt_extensions = self._module_loader.get_prompt_extensions()
        if self._module_prompt_extensions:
            self._logger.info(
                "kernel",
                f"  Loaded {len(self._module_prompt_extensions)} prompt extension(s) from modules",
            )

    def _run_module_hooks(self, hook: str, ctx: HookContext) -> HookContext:
        for mod in self._module_loader.get_active():
            if mod.cog_module is None:
                continue
            handler = getattr(mod.cog_module, hook, None)
            if handler is not None:
                try:
                    ctx = handler(ctx)
                except Exception as e:
                    self._logger.warning(
                        "kernel", f"Module {mod.name} hook {hook} failed: {e}"
                    )
        return ctx

    def _init_memory(self) -> None:
        if self._memory is not None:
            return
        if self._config.memory_backend == "mem0":
            self._memory = Mem0MemoryBackend(
                config=self._config.mem0_config,
                agent_id=self._config.memory_agent_id,
                user_id=self._config.memory_user_id,
            )
            self._logger.info("kernel", "Memory backend: Mem0")
        else:
            self._memory = SQLiteMemoryBackend(self._config.memory_path)
            self._logger.info(
                "kernel", f"Memory backend: SQLite ({self._config.memory_path})"
            )

    def _init_provider(self) -> None:
        if self._provider is not None:
            return
        if not self._config.provider:
            raise ValueError(
                "No LLM provider configured. Set 'provider' in cog.yaml, "
                "use --provider on the CLI, or set COG_PROVIDER env var."
            )
        if not self._config.model:
            raise ValueError(
                "No LLM model configured. Set 'model' in cog.yaml, "
                "use --model on the CLI, or set COG_MODEL env var."
            )
        if not self._config.api_key:
            raise ValueError(
                "No API key configured. Set 'api_key' in cog.yaml, "
                "set COG_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY env var, "
                "or pass api_key= to the constructor."
            )
        if self._config.provider == "anthropic":
            from cog.providers.anthropic_provider import AnthropicProvider

            self._provider = AnthropicProvider(
                model=self._config.model, api_key=self._config.api_key
            )
        else:
            from cog.providers.openai_provider import OpenAIProvider

            self._provider = OpenAIProvider(
                model=self._config.model,
                api_key=self._config.api_key,
                base_url=self._config.base_url,
            )
        self._logger.info(
            "kernel", f"Provider initialized: {self._provider.get_model_name()}"
        )

    def _build_system_prompt(self, task: str) -> str:
        base = """You are a CogOS agent — a modular cognitive execution engine. You complete tasks by reasoning step-by-step and calling tools.

Rules:
- Analyze the task carefully before acting
- Use tools to gather information and make changes
- Verify your work when possible
- Be concise and accurate
- Report clear results
- If a task fails, explain why and suggest next steps
- Do NOT make destructive changes without explicit approval"""
        if self._module_prompt_extensions:
            base += "\n\n## Module Knowledge"
            for ext in self._module_prompt_extensions:
                base += f"\n\n{ext}"
        memory_context = self._get_memory_context(task)
        if memory_context:
            base += f"\n\n## Relevant Memory\n\n{memory_context}"
        return base

    def _get_memory_context(self, query: str) -> str:
        if self._memory is None:
            return ""
        try:
            if isinstance(self._memory, Mem0MemoryBackend):
                return self._memory.get_relevant_context(query, limit=5)
            entries = self._memory.search(query, limit=5)
            if not entries:
                return ""
            return "\n".join(f"- {e.content}" for e in entries)
        except Exception:
            return ""

    def _init_agent(self, task: str = "") -> None:
        self._init_provider()
        assert self._provider is not None
        self._planner = Planner(provider=self._provider)
        agent_config = AgentConfig(
            max_iterations=self._config.max_agent_iterations,
            system_prompt=self._build_system_prompt(task),
            max_total_tokens=self._config.max_total_tokens,
        )
        self._agent = Agent(
            provider=self._provider,
            tools=self._tools,
            permissions=self._permissions,
            config=agent_config,
        )
        if self._approval_cb:
            self._agent.set_approval_callback(self._approval_cb)
        if self._stream_cb:
            self._agent.set_stream_callback(self._stream_cb)
        if self._on_step:
            self._agent.set_step_callback(self._on_step)
        self._logger.info("kernel", "Agent initialized")

    def set_approval_callback(self, cb: ApprovalCallback) -> None:
        self._approval_cb = cb
        if self._agent:
            self._agent.set_approval_callback(cb)

    def set_stream_callback(self, cb: StreamCallback) -> None:
        self._stream_cb = cb
        if self._agent:
            self._agent.set_stream_callback(cb)

    def set_step_callback(self, cb: Callable[[Any], None]) -> None:
        self._on_step = cb
        if self._agent:
            self._agent.set_step_callback(cb)

    def start(self) -> None:
        self._logger.info("kernel", "Starting CogOS kernel...")
        self._init_memory()
        discovered = self._module_loader.discover()
        self._logger.info("kernel", f"Discovered {len(discovered)} modules")
        activation_order = self._module_loader._resolve_activation_order()
        for mod in activation_order:
            if mod.state != ModuleState.ERROR:
                self._module_loader.activate(mod.name)
                deps = mod.manifest.requires
                if deps:
                    self._logger.info(
                        "kernel",
                        f"  Activated: {mod.name} (requires: {', '.join(deps)})",
                    )
                else:
                    self._logger.info("kernel", f"Activated module: {mod.name}")
        self._integrate_modules()
        self._running = True
        self._logger.info("kernel", "CogOS kernel ready")

    def stop(self) -> None:
        self._logger.info("kernel", "Stopping CogOS kernel...")
        for mod in self._module_loader.get_active():
            self._module_loader.unload(mod.name)
        if self._memory:
            if isinstance(self._memory, SQLiteMemoryBackend):
                self._memory.close()
            elif isinstance(self._memory, Mem0MemoryBackend):
                self._memory.close()
        self._running = False
        self._logger.info("kernel", "CogOS kernel stopped")

    def run(self, task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self._running:
            self.start()
        self._logger.info("kernel", f"Running task: {task}")
        hook_ctx = HookContext(task=task, context=context or {})
        hook_ctx = self._run_module_hooks("pre_execute", hook_ctx)

        if self._config.dry_run:
            return self._run_dry(task, context)

        self._init_agent(task)
        assert self._agent is not None
        agent_result = self._agent.run(task, context)

        plan = self._planner.create_plan(task, context)
        plan.status = "completed" if agent_result.success else "failed"
        self._store_task(task, plan, agent_result)
        self._store_conversation_memory(task, agent_result)

        hook_ctx.result = {
            "success": agent_result.success,
            "output": agent_result.output,
            "iterations": agent_result.iterations,
        }
        hook_ctx = self._run_module_hooks("post_execute", hook_ctx)

        summary = {
            "task": task,
            "success": agent_result.success,
            "output": agent_result.output,
            "iterations": agent_result.iterations,
            "total_tokens": agent_result.total_tokens,
            "cost_estimate": agent_result.cost_estimate,
            "steps": [
                {
                    "iteration": s.iteration,
                    "thought": s.thought[:200] if s.thought else None,
                    "tool": s.tool_call.name if s.tool_call else None,
                    "result": (s.tool_result or "")[:200] if s.tool_result else None,
                    "error": s.tool_error,
                    "retries": s.retries,
                    "approved": s.approved,
                }
                for s in agent_result.steps
            ],
        }
        self._logger.info(
            "kernel",
            f"Task complete: success={agent_result.success}, tokens={agent_result.total_tokens}, cost=${agent_result.cost_estimate:.4f}",
        )
        return summary

    def _store_conversation_memory(self, task: str, result: AgentResult) -> None:
        if self._memory is None:
            return
        try:
            if isinstance(self._memory, Mem0MemoryBackend):
                messages = [{"role": "user", "content": task}]
                if result.output:
                    messages.append({"role": "assistant", "content": result.output})
                self._memory.store_conversation(
                    messages,
                    metadata={
                        "success": result.success,
                        "iterations": result.iterations,
                        "tokens": result.total_tokens,
                    },
                )
            else:
                entry = MemoryEntry(
                    id="",
                    memory_type=MemoryType.EPISODIC,
                    content=f"Task: {task}\nResult: {result.output[:500]}",
                    metadata={
                        "success": result.success,
                        "iterations": result.iterations,
                    },
                    tags=["task", "auto-stored"],
                )
                self._memory.store(entry)
        except Exception as e:
            self._logger.warning("kernel", f"Failed to store conversation memory: {e}")

    def _run_dry(
        self, task: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        plan = self._planner.create_plan(task, context)
        self._logger.info(
            "kernel", f"[DRY RUN] Created plan with {len(plan.steps)} steps"
        )
        results: list[dict[str, Any]] = []
        for step in plan.steps:
            step.status = "running"
            step_result = self._execute_step_dry(step, context)
            step.result = step_result
            results.append(step_result)
            step.status = "completed"
        plan.status = "completed"
        return {
            "task": task,
            "plan": plan.summary(),
            "dry_run": True,
            "steps_completed": len(plan.steps),
            "steps_total": len(plan.steps),
            "success": True,
            "results": results,
        }

    def _execute_step_dry(
        self, step: PlanStep, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        route = self._router.route_step(step.action, step.description)
        step.module = route.module
        return {
            "step": step.step_number,
            "action": step.action,
            "dry_run": True,
            "success": True,
            "output": f"[DRY RUN] Would execute: {step.description}",
        }

    def chat(self, message: str) -> dict[str, Any]:
        if not self._running:
            self.start()
        self._init_agent(message)
        assert self._agent is not None

        messages = self._agent.get_conversation()
        messages.append(LLMMessage(role=MessageRole.USER, content=message))

        if self._stream_cb:
            response = self._provider.complete_stream(
                messages=messages,
                tools=None,
                temperature=0.1,
                max_tokens=4096,
                system=self._agent._config.system_prompt,
                on_chunk=self._stream_cb,
            )
        else:
            response = self._provider.complete(
                messages=messages,
                tools=None,
                temperature=0.1,
                max_tokens=4096,
                system=self._agent._config.system_prompt,
            )

        self._agent._conversation.append(
            LLMMessage(role=MessageRole.USER, content=message)
        )
        self._agent._conversation.append(
            LLMMessage(role=MessageRole.ASSISTANT, content=response.content)
        )

        return {
            "content": response.content,
            "model": response.model,
            "tool_calls": [
                {"name": tc.name, "arguments": tc.arguments}
                for tc in response.tool_calls
            ],
        }

    def _store_task(
        self, task: str, plan: Plan, agent_result: AgentResult | None = None
    ) -> None:
        if self._memory is None:
            return
        if isinstance(self._memory, Mem0MemoryBackend):
            return
        metadata: dict[str, Any] = {"steps": len(plan.steps)}
        if agent_result:
            metadata["iterations"] = agent_result.iterations
            metadata["tokens"] = agent_result.total_tokens
        entry = MemoryEntry(
            id="",
            memory_type=MemoryType.TASK,
            content=task,
            metadata=metadata,
            tags=["task"],
        )
        self._memory.store(entry)

    def register_tool(self, tool: Tool) -> None:
        self._tools[tool.name] = tool
        if self._agent:
            self._agent = None

    def search_memory(self, query: str, limit: int = 5) -> list[MemoryEntry]:
        if self._memory is None:
            return []
        return self._memory.search(query, limit=limit)

    @property
    def logger(self) -> CogLogger:
        return self._logger

    @property
    def modules(self) -> ModuleLoader:
        return self._module_loader

    @property
    def router(self) -> CapabilityRouter:
        return self._router

    @property
    def planner(self) -> Planner:
        return self._planner

    @property
    def registry(self) -> Registry:
        return self._registry

    @property
    def verification(self) -> VerificationLayer:
        return self._verification

    @property
    def memory(self) -> MemoryBackend | None:
        return self._memory

    @property
    def tools(self) -> dict[str, Tool]:
        return dict(self._tools)

    @property
    def config(self) -> KernelConfig:
        return self._config

    @property
    def provider(self) -> LLMProvider | None:
        return self._provider

    def set_provider(self, provider: LLMProvider) -> None:
        """Set a pre-built LLM provider (pass-through mode).

        Use this when the host tool (Claude Code, Codex CLI, etc.)
        has already constructed its own provider and wants to hand it
        to CogOS directly, bypassing any config-based initialization.
        """
        self._provider = provider
        self._logger.info(
            "kernel",
            f"Provider set externally: {provider.get_model_name()}",
        )

    @property
    def agent(self) -> Agent | None:
        return self._agent
