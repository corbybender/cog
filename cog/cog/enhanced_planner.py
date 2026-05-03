from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from cog.llm import LLMProvider, LLMMessage, MessageRole
from cog.logging import get_logger
from cog.planner import Plan, PlanStep


class TaskComplexity(str, Enum):
    SIMPLE = "simple"  # Single tool call
    MODERATE = "moderate"  # 2-5 related operations
    COMPLEX = "complex"  # Multi-step, requires planning
    VERY_COMPLEX = "very_complex"  # Requires decomposition


@dataclass
class TaskAnalysis:
    task: str
    complexity: TaskComplexity
    estimated_steps: int
    tools_required: list[str]
    modules_required: list[str]
    risks: list[str]
    can_decompose: bool = True
    reasoning: str = ""


@dataclass
class ExecutionPreview:
    steps: list[dict[str, Any]]
    estimated_tokens: int
    estimated_time: int
    risk_level: str
    requires_approval: bool = False
    approval_points: list[str] = field(default_factory=list)


class EnhancedPlanner:
    """Enhanced planning system with multi-step reasoning."""

    def __init__(self, provider: LLMProvider | None = None) -> None:
        self._provider = provider
        self._logger = get_logger()
        self._complexity_cache: dict[str, TaskAnalysis] = {}

    def analyze_task(self, task: str, context: dict[str, Any] | None = None) -> TaskAnalysis:
        """Analyze task complexity and requirements."""
        # Check cache
        if task in self._complexity_cache:
            return self._complexity_cache[task]

        # Quick complexity assessment
        complexity = self._assess_complexity(task)
        tools_required = self._identify_tools(task)
        modules_required = self._identify_modules(task)
        risks = self._assess_risks(task, tools_required)
        estimated_steps = self._estimate_steps(task, complexity)

        analysis = TaskAnalysis(
            task=task,
            complexity=complexity,
            estimated_steps=estimated_steps,
            tools_required=tools_required,
            modules_required=modules_required,
            risks=risks,
            can_decompose=complexity != TaskComplexity.SIMPLE,
            reasoning=self._generate_reasoning(task, complexity),
        )

        self._complexity_cache[task] = analysis
        return analysis

    def _assess_complexity(self, task: str) -> TaskComplexity:
        """Quick complexity assessment."""
        task_lower = task.lower()

        # Simple tasks - single operation
        if any(word in task_lower for word in ["read", "list", "show", "get", "check"]):
            if task_lower.count(" and ") < 2:
                return TaskComplexity.SIMPLE

        # Complex indicators
        complexity_indicators = [
            ("analyze", 1),
            ("improve", 2),
            ("implement", 2),
            ("refactor", 3),
            ("create", 2),
            ("build", 3),
            ("design", 2),
            ("optimize", 2),
            ("debug", 2),
            ("test", 1),
        ]

        score = 0
        for indicator, weight in complexity_indicators:
            if indicator in task_lower:
                score += weight

        # Check for multi-step keywords
        if "then" in task_lower or "after" in task_lower or "finally" in task_lower:
            score += 2

        if score <= 1:
            return TaskComplexity.SIMPLE
        elif score <= 3:
            return TaskComplexity.MODERATE
        elif score <= 5:
            return TaskComplexity.COMPLEX
        else:
            return TaskComplexity.VERY_COMPLEX

    def _identify_tools(self, task: str) -> list[str]:
        """Identify required tools based on task."""
        task_lower = task.lower()
        tools = []

        tool_keywords = {
            "filesystem.read": ["read", "show", "view", "cat", "display"],
            "filesystem.write": ["write", "save", "create", "modify"],
            "shell.execute": ["run", "execute", "command", "test"],
            "git.log": ["git", "history", "commits"],
            "python.test": ["test", "pytest"],
            "python.lint": ["lint", "ruff", "flake8"],
            "web.fetch": ["fetch", "download", "url"],
        }

        for tool, keywords in tool_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                tools.append(tool)

        return tools or ["filesystem.read"]  # Default tool

    def _identify_modules(self, task: str) -> list[str]:
        """Identify required modules."""
        task_lower = task.lower()

        if "python" in task_lower:
            return ["code-core", "language-core", "cog-code-python"]
        elif "git" in task_lower:
            return ["tool-core", "cog-git"]
        elif "file" in task_lower or "code" in task_lower:
            return ["code-core", "language-core"]

        return ["tool-core"]

    def _assess_risks(self, task: str, tools: list[str]) -> list[str]:
        """Assess potential risks."""
        risks = []

        if "filesystem.write" in tools or "shell.execute" in tools:
            risks.append("Modifies files or system state")

        if "delete" in task.lower() or "remove" in task.lower():
            risks.append("Destructive operations")

        if "shell.execute" in tools:
            risks.append("Command execution")

        return risks or ["Low risk operation"]

    def _estimate_steps(self, task: str, complexity: TaskComplexity) -> int:
        """Estimate number of execution steps."""
        if complexity == TaskComplexity.SIMPLE:
            return 1
        elif complexity == TaskComplexity.MODERATE:
            return 3
        elif complexity == TaskComplexity.COMPLEX:
            return 7
        else:
            return 12

    def _generate_reasoning(self, task: str, complexity: TaskComplexity) -> str:
        """Generate reasoning for complexity assessment."""
        return f"Task classified as {complexity.value} based on keywords and structure"

    def decompose_task(
        self, task: str, analysis: TaskAnalysis
    ) -> list[dict[str, Any]]:
        """Decompose complex task into steps."""
        if analysis.complexity == TaskComplexity.SIMPLE:
            return [{
                "step": 1,
                "action": "execute_task",
                "description": task,
                "tools": analysis.tools_required,
            }]

        # For complex tasks, use LLM to decompose
        if self._provider:
            return self._llm_decompose(task, analysis)

        # Fallback: rule-based decomposition
        return self._rule_based_decompose(task, analysis)

    def _llm_decompose(
        self, task: str, analysis: TaskAnalysis
    ) -> list[dict[str, Any]]:
        """Use LLM to decompose complex task."""
        if not self._provider:
            return []

        prompt = f"""Break down this task into clear steps:

Task: {task}

Available tools: {', '.join(analysis.tools_required)}
Available modules: {', '.join(analysis.modules_required)}

Return a JSON array of steps with:
- step: number
- action: what to do
- tools: which tools to use
- description: clear description

Focus on safe, verifiable steps."""

        try:
            response = self._provider.complete(
                messages=[LLMMessage(role=MessageRole.USER, content=prompt)],
                temperature=0.3,
                max_tokens=1000,
            )

            steps_data = json.loads(response.content or "[]")
            return steps_data

        except Exception as e:
            self._logger.warning("planner", f"LLM decomposition failed: {e}")
            return self._rule_based_decompose(task, analysis)

    def _rule_based_decompose(
        self, task: str, analysis: TaskAnalysis
    ) -> list[dict[str, Any]]:
        """Rule-based task decomposition."""
        steps = []
        task_lower = task.lower()

        # Common patterns
        if "analyze" in task_lower and "improve" in task_lower:
            steps.append({"step": 1, "action": "analyze", "description": f"Analyze: {task}", "tools": ["filesystem.read"]})
            steps.append({"step": 2, "action": "identify", "description": "Identify improvements", "tools": []})
            steps.append({"step": 3, "action": "implement", "description": "Implement top improvement", "tools": ["filesystem.write"]})
            steps.append({"step": 4, "action": "verify", "description": "Run tests", "tools": ["python.test"]})

        elif "create" in task_lower or "build" in task_lower:
            steps.append({"step": 1, "action": "plan", "description": "Plan structure", "tools": []})
            steps.append({"step": 2, "action": "create", "description": "Create files", "tools": ["filesystem.write"]})
            steps.append({"step": 3, "action": "verify", "description": "Verify creation", "tools": ["filesystem.list"]})

        else:
            # Generic decomposition
            steps.append({"step": 1, "action": "understand", "description": "Understand requirements", "tools": analysis.tools_required[:1]})
            steps.append({"step": 2, "action": "execute", "description": task, "tools": analysis.tools_required})
            steps.append({"step": 3, "action": "verify", "description": "Verify results", "tools": []})

        return steps

    def create_preview(
        self, task: str, analysis: TaskAnalysis, steps: list[dict[str, Any]]
    ) -> ExecutionPreview:
        """Create execution preview."""
        estimated_tokens = len(steps) * 2000  # Rough estimate
        estimated_time = len(steps) * 15  # 15 seconds per step

        # Determine risk level
        if analysis.complexity == TaskComplexity.VERY_COMPLEX:
            risk_level = "HIGH"
        elif any("destructive" in r.lower() for r in analysis.risks):
            risk_level = "HIGH"
        elif len(analysis.risks) > 2:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Identify approval points
        approval_points = []
        for step in steps:
            if any(tool in step.get("tools", []) for tool in ["filesystem.write", "shell.execute"]):
                approval_points.append(step.get("description", ""))

        return ExecutionPreview(
            steps=steps,
            estimated_tokens=estimated_tokens,
            estimated_time=estimated_time,
            risk_level=risk_level,
            requires_approval=risk_level != "LOW",
            approval_points=approval_points,
        )

    def format_preview(self, preview: ExecutionPreview) -> str:
        """Format preview for display."""
        lines = [
            "📋 Execution Preview",
            f"  Steps: {len(preview.steps)}",
            f"  Estimated time: {preview.estimated_time}s",
            f"  Risk level: {preview.risk_level}",
            "",
            "Steps:",
        ]

        for step in preview.steps:
            lines.append(f"  {step.get('step')}. {step.get('description')}")

        if preview.approval_points:
            lines.append("")
            lines.append("⚠️  Requires approval at:")
            for point in preview.approval_points:
                lines.append(f"  - {point}")

        return "\n".join(lines)
