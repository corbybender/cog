"""
Hierarchical Task Planning and Execution System

This system breaks down complex tasks into manageable subtasks,
coordinates their execution, and handles dependencies.

This is crucial for solving problems that are too complex for
a single reasoning pass.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
from pathlib import Path

from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1  # Must complete first
    HIGH = 2
    MEDIUM = 3
    LOW = 4


@dataclass
class Task:
    """A task in the hierarchical plan"""
    task_id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: List[str] = field(default_factory=list)
    subtasks: List['Task'] = field(default_factory=list)
    parent_task: Optional[str] = None
    assigned_to: Optional[str] = None
    estimated_effort: int = 1  # In complexity points
    actual_effort: int = 0
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "dependencies": self.dependencies,
            "subtasks": [t.to_dict() for t in self.subtasks],
            "parent_task": self.parent_task,
            "assigned_to": self.assigned_to,
            "estimated_effort": self.estimated_effort,
            "actual_effort": self.actual_effort,
            "result": str(self.result) if self.result else None,
            "error": self.error,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary"""
        subtasks = [cls.from_dict(t) for t in data.get("subtasks", [])]
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            description=data["description"],
            status=TaskStatus(data.get("status", "pending")),
            priority=TaskPriority(data.get("priority", 3)),
            dependencies=data.get("dependencies", []),
            subtasks=subtasks,
            parent_task=data.get("parent_task"),
            assigned_to=data.get("assigned_to"),
            estimated_effort=data.get("estimated_effort", 1),
            actual_effort=data.get("actual_effort", 0),
            error=data.get("error"),
            metadata=data.get("metadata", {}),
        )


class TaskPlanner:
    """
    Plans complex tasks by breaking them down hierarchically

    Uses LLM to understand requirements and create execution plans.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        memory: MemoryBackend,
        cache: SmartCache
    ):
        self.llm = llm_provider
        self.memory = memory
        self.cache = cache
        self.planning_cache = {}  # Cache plans

    async def plan_task(
        self,
        goal: str,
        context: str = "",
        max_depth: int = 3
    ) -> Task:
        """
        Create a hierarchical plan for achieving a goal

        This is where we break down complex problems into manageable pieces.
        """
        # Check cache
        cache_key = f"plan:{hash(goal + context)}"
        if cache_key in self.planning_cache:
            return self.planning_cache[cache_key]

        # Use LLM to create plan
        planning_prompt = f"""You are a Task Planning Agent. Create a detailed execution plan for:

GOAL: {goal}

CONTEXT: {context}

Create a hierarchical task breakdown:
1. Break down the goal into 3-7 major tasks
2. For each task, identify dependencies
3. Set priorities (CRITICAL, HIGH, MEDIUM, LOW)
4. Estimate complexity (1-10)
5. If a task is complex, break it down further

Return your plan as JSON following this structure:
{{
  "task_id": "root",
  "title": "Main Goal",
  "description": "Description",
  "priority": "HIGH",
  "subtasks": [
    {{
      "task_id": "task-1",
      "title": "Subtask 1",
      "description": "Description",
      "priority": "CRITICAL",
      "dependencies": [],
      "estimated_effort": 3,
      "subtasks": []
    }}
  ]
}}

Be thorough but pragmatic. Focus on actionable tasks."""

        messages = [
            {"role": "system", "content": "You are an expert task planner. Return valid JSON only."},
            {"role": "user", "content": planning_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.3,
            max_tokens=3000
        )

        # Parse JSON response
        try:
            plan_data = json.loads(response.content)
            root_task = Task.from_dict(plan_data)
        except json.JSONDecodeError:
            # Fallback: create simple plan
            root_task = Task(
                task_id="root",
                title=goal,
                description=goal,
                priority=TaskPriority.HIGH,
                estimated_effort=5
            )

        # Cache plan
        self.planning_cache[cache_key] = root_task

        return root_task

    async def refine_plan(
        self,
        plan: Task,
        feedback: str
    ) -> Task:
        """Refine a plan based on feedback"""
        refinement_prompt = f"""You are a Task Refinement Agent. Refine this plan based on feedback:

CURRENT PLAN:
{json.dumps(plan.to_dict(), indent=2)}

FEEDBACK:
{feedback}

Update the plan to address the feedback. Return the updated plan as JSON."""

        messages = [
            {"role": "system", "content": "You are an expert task planner. Return valid JSON only."},
            {"role": "user", "content": refinement_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.3,
            max_tokens=3000
        )

        try:
            refined_data = json.loads(response.content)
            return Task.from_dict(refined_data)
        except json.JSONDecodeError:
            return plan  # Return original if parsing fails


class TaskExecutor:
    """
    Executes hierarchical task plans

    Coordinates task execution, handles dependencies,
    and manages failures.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        memory: MemoryBackend,
        cache: SmartCache
    ):
        self.llm = llm_provider
        self.memory = memory
        self.cache = cache
        self.execution_history: List[Dict[str, Any]] = []

    async def execute_plan(
        self,
        plan: Task,
        context: str = "",
        execution_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Execute a hierarchical task plan

        This is where the plan becomes action.
        """
        result = {
            "plan_id": plan.task_id,
            "tasks_executed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "total_effort": 0,
            "result": None,
            "errors": []
        }

        # Execute tasks in dependency order
        execution_order = self._get_execution_order(plan)

        for task_id in execution_order:
            task = self._find_task(plan, task_id)
            if not task:
                continue

            # Check if dependencies are met
            if not self._dependencies_met(task, plan):
                task.status = TaskStatus.BLOCKED
                continue

            # Execute task
            try:
                task_result = await self._execute_task(task, context, execution_callback)
                task.result = task_result
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                result["tasks_succeeded"] += 1
                result["tasks_executed"] += 1
                result["total_effort"] += task.actual_effort

                if task_id == plan.task_id:
                    result["result"] = task_result

            except Exception as e:
                task.error = str(e)
                task.status = TaskStatus.FAILED
                result["tasks_failed"] += 1
                result["errors"].append({
                    "task_id": task_id,
                    "error": str(e)
                })

        # Store execution history
        self.execution_history.append({
            "plan_id": plan.task_id,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })

        return result

    def _get_execution_order(self, plan: Task) -> List[str]:
        """Get topological sort of tasks based on dependencies"""
        tasks = self._flatten_tasks(plan)
        order = []
        visited = set()

        def visit(task_id: str):
            if task_id in visited:
                return
            visited.add(task_id)

            task = self._find_task(plan, task_id)
            if task:
                for dep in task.dependencies:
                    visit(dep)

            order.append(task_id)

        for task in tasks:
            visit(task.task_id)

        return order

    def _flatten_tasks(self, plan: Task) -> List[Task]:
        """Flatten hierarchical tasks into a list"""
        tasks = []

        def collect(task: Task):
            tasks.append(task)
            for subtask in task.subtasks:
                collect(subtask)

        collect(plan)
        return tasks

    def _find_task(self, plan: Task, task_id: str) -> Optional[Task]:
        """Find a task by ID in the hierarchy"""
        if plan.task_id == task_id:
            return plan

        for subtask in plan.subtasks:
            found = self._find_task(subtask, task_id)
            if found:
                return found

        return None

    def _dependencies_met(self, task: Task, plan: Task) -> bool:
        """Check if task dependencies are satisfied"""
        for dep_id in task.dependencies:
            dep_task = self._find_task(plan, dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        return True

    async def _execute_task(
        self,
        task: Task,
        context: str,
        execution_callback: Optional[Callable] = None
    ) -> Any:
        """Execute a single task"""
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()

        # If task has subtasks, execute them first
        if task.subtasks:
            subtask_results = []
            for subtask in task.subtasks:
                result = await self._execute_task(subtask, context, execution_callback)
                subtask_results.append(result)

            task.actual_effort = sum(st.actual_effort for st in task.subtasks)
            return subtask_results

        # Use callback if provided
        if execution_callback:
            result = await execution_callback(task, context)
            task.actual_effort = task.estimated_effort
            return result

        # Default: use LLM to execute
        execution_prompt = f"""You are a Task Execution Agent. Execute this task:

TASK: {task.title}
DESCRIPTION: {task.description}

CONTEXT: {context}

Execute the task and provide a detailed result. Be specific and actionable."""

        messages = [
            {"role": "system", "content": "You are a task execution agent."},
            {"role": "user", "content": execution_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.5,
            max_tokens=2000
        )

        task.actual_effort = task.estimated_effort
        return response.content


class HierarchicalPlanner:
    """
    Main interface for hierarchical planning and execution

    Combines planning and execution into a unified system.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        memory: MemoryBackend,
        cache: SmartCache
    ):
        self.planner = TaskPlanner(llm_provider, memory, cache)
        self.executor = TaskExecutor(llm_provider, memory, cache)
        self.llm = llm_provider
        self.memory = memory
        self.cache = cache

    async def solve(
        self,
        goal: str,
        context: str = "",
        execution_callback: Optional[Callable] = None,
        iterations: int = 1
    ) -> Dict[str, Any]:
        """
        Solve a complex goal using hierarchical planning

        This is the main entry point for solving complex problems.
        """
        # Create initial plan
        plan = await self.planner.plan_task(goal, context)

        # Refine plan if needed
        for i in range(iterations - 1):
            # Get feedback on plan
            feedback = await self._get_plan_feedback(plan, context)
            if feedback:
                plan = await self.planner.refine_plan(plan, feedback)

        # Execute plan
        result = await self.executor.execute_plan(plan, context, execution_callback)

        return {
            "goal": goal,
            "plan": plan.to_dict(),
            "execution": result,
            "success": result["tasks_failed"] == 0
        }

    async def _get_plan_feedback(self, plan: Task, context: str) -> Optional[str]:
        """Get feedback on a plan"""
        feedback_prompt = f"""You are a Plan Review Agent. Review this plan:

PLAN:
{json.dumps(plan.to_dict(), indent=2)}

CONTEXT: {context}

Provide feedback on:
1. Are there missing tasks?
2. Are dependencies correct?
3. Are priorities appropriate?
4. What could be improved?

Provide specific, actionable feedback. If the plan looks good, say "PLAN_APPROVED"."""

        messages = [
            {"role": "system", "content": "You are a plan reviewer."},
            {"role": "user", "content": feedback_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.3,
            max_tokens=1000
        )

        feedback = response.content.strip()
        if "PLAN_APPROVED" in feedback:
            return None
        return feedback
