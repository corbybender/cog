from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from cog.providers.base import LLMProvider, LLMMessage, MessageRole


@dataclass
class PlanStep:
    step_number: int
    action: str
    module: str | None = None
    args: dict[str, Any] = field(default_factory=dict)
    description: str = ""
    status: str = "pending"
    result: Any = None


@dataclass
class Plan:
    task: str
    steps: list[PlanStep] = field(default_factory=list)
    status: str = "pending"

    def add_step(
        self,
        action: str,
        module: str | None = None,
        args: dict[str, Any] | None = None,
        description: str = "",
    ) -> PlanStep:
        step = PlanStep(
            step_number=len(self.steps) + 1,
            action=action,
            module=module,
            args=args or {},
            description=description,
        )
        self.steps.append(step)
        return step

    def current_step(self) -> PlanStep | None:
        for step in self.steps:
            if step.status == "pending":
                return step
        return None

    def advance(self) -> PlanStep | None:
        current = self.current_step()
        if current:
            current.status = "completed"
        return self.current_step()

    def fail_current(self, error: str) -> None:
        current = self.current_step()
        if current:
            current.status = "failed"
            current.result = error

    def is_complete(self) -> bool:
        return all(s.status in ("completed", "skipped") for s in self.steps)

    def has_failures(self) -> bool:
        return any(s.status == "failed" for s in self.steps)

    def summary(self) -> str:
        lines = [f"Plan: {self.task}", f"Status: {self.status}", ""]
        for step in self.steps:
            marker = {
                "pending": "[ ]",
                "completed": "[x]",
                "failed": "[!]",
                "skipped": "[-]",
            }
            lines.append(
                f"  {marker.get(step.status, '[?]')} {step.step_number}. {step.action}"
                + (f" → {step.module}" if step.module else "")
            )
        return "\n".join(lines)


class Planner:
    def __init__(self, provider: LLMProvider | None = None) -> None:
        self._provider = provider

    def create_plan(self, task: str, context: dict[str, Any] | None = None) -> Plan:
        plan = Plan(task=task)
        normalized = task.lower().strip()

        if self._provider:
            try:
                return self._create_llm_plan(task, context)
            except Exception:
                pass

        if self._matches_repo_task(normalized):
            self._build_repo_plan(plan, normalized)
        elif self._matches_code_task(normalized):
            self._build_code_plan(plan, normalized)
        elif self._matches_research_task(normalized):
            self._build_research_plan(plan, normalized)
        else:
            self._build_generic_plan(plan, normalized)

        plan.status = "ready"
        return plan

    def _create_llm_plan(
        self, task: str, context: dict[str, Any] | None = None
    ) -> Plan:
        assert self._provider is not None
        prompt = (
            "You are a task planner for an AI agent. Decompose the following task into 3-7 clear, "
            "actionable steps. Each step should be a short verb phrase (e.g. 'read config files', "
            "'run tests', 'write summary report'). "
            "Respond with ONLY a JSON array of strings, no other text.\n\n"
            f"Task: {task}"
        )
        response = self._provider.complete(
            messages=[LLMMessage(role=MessageRole.USER, content=prompt)],
            temperature=0.3,
            max_tokens=500,
        )
        content = response.content or "[]"
        content = content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[-1].rsplit("```", 1)[0]
        try:
            steps_raw = json.loads(content)
        except json.JSONDecodeError:
            steps_raw = [s.strip("- ") for s in content.split("\n") if s.strip()]

        plan = Plan(task=task)
        for i, step_str in enumerate(steps_raw):
            if isinstance(step_str, str) and step_str.strip():
                plan.add_step(
                    action=step_str.strip().split()[0]
                    if step_str.strip()
                    else f"step_{i}",
                    description=step_str.strip(),
                )
        if not plan.steps:
            self._build_generic_plan(plan, task)
        plan.status = "ready"
        return plan

    def _matches_repo_task(self, task: str) -> bool:
        keywords = [
            "inspect",
            "repository",
            "repo",
            "summarize architecture",
            "task plan",
        ]
        return any(k in task for k in keywords)

    def _matches_code_task(self, task: str) -> bool:
        keywords = ["fix", "implement", "write code", "debug", "refactor", "test"]
        return any(k in task for k in keywords)

    def _matches_research_task(self, task: str) -> bool:
        keywords = ["research", "search", "find", "analyze", "explain"]
        return any(k in task for k in keywords)

    def _build_repo_plan(self, plan: Plan, task: str) -> None:
        plan.add_step("inspect", description="Inspect repository structure")
        plan.add_step("analyze", description="Analyze codebase architecture")
        plan.add_step("summarize", description="Summarize findings")
        plan.add_step("plan", description="Create improvement task plan")
        plan.add_step("implement", description="Make one safe improvement")
        plan.add_step("verify", description="Run tests and verify")
        plan.add_step("report", description="Report results")

    def _build_code_plan(self, plan: Plan, task: str) -> None:
        plan.add_step("read", description="Read relevant code")
        plan.add_step("analyze", description="Analyze the issue")
        plan.add_step("implement", description="Implement changes")
        plan.add_step("verify", description="Verify changes")
        plan.add_step("report", description="Report results")

    def _build_research_plan(self, plan: Plan, task: str) -> None:
        plan.add_step("search", description="Search for information")
        plan.add_step("analyze", description="Analyze findings")
        plan.add_step("report", description="Report results")

    def _build_generic_plan(self, plan: Plan, task: str) -> None:
        plan.add_step("analyze", description="Analyze the task")
        plan.add_step("plan", description="Create execution plan")
        plan.add_step("execute", description="Execute the plan")
        plan.add_step("verify", description="Verify results")
        plan.add_step("report", description="Report results")
