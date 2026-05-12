"""
CogOS Super-Intelligence Integration Layer

This is the main brain that orchestrates all advanced systems:
1. Multi-Agent Orchestration
2. Hierarchical Task Planning
3. Self-Reflection and Improvement
4. Research and Context Gathering
5. Document Generation
6. Execution and Validation

This is what makes CogOS dramatically superior to single-pass LLMs like Claude.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
import asyncio
from datetime import datetime
from pathlib import Path

from cog.providers.base import LLMProvider
from cog.memory.base import MemoryBackend
from cog.cache import SmartCache
from cog.multi_agent import (
    MultiAgentOrchestrator,
    Agent,
    AgentRole,
    create_orchestrator
)
from cog.hierarchical_planner import (
    HierarchicalPlanner,
    TaskPlanner,
    TaskExecutor
)
from cog.self_reflection import (
    SelfReflector,
    ContinuousImprover
)
from cog.research import (
    Researcher,
    ContextGatherer
)
from cog.document_writer import (
    DocumentWriter,
    CollaborativeWriter,
    DocumentType
)


@dataclass
class CogOSConfig:
    """Configuration for CogOS"""
    llm_provider: LLMProvider
    memory: MemoryBackend
    cache: SmartCache
    enable_multi_agent: bool = True
    enable_self_reflection: bool = True
    enable_research: bool = True
    enable_collaboration: bool = True
    max_iterations: int = 3
    confidence_threshold: float = 0.7


class CogOSSuperIntelligence:
    """
    Main orchestrator for CogOS super-intelligence

    This is the entry point for using all advanced capabilities.
    """

    def __init__(self, config: CogOSConfig):
        self.config = config
        self.llm = config.llm_provider
        self.memory = config.memory
        self.cache = config.cache

        # Initialize subsystems
        self.orchestrator: Optional[MultiAgentOrchestrator] = None
        self.planner: Optional[HierarchicalPlanner] = None
        self.reflector: Optional[SelfReflector] = None
        self.improver: Optional[ContinuousImprover] = None
        self.researcher: Optional[Researcher] = None
        self.context_gatherer: Optional[ContextGatherer] = None
        self.document_writer: Optional[DocumentWriter] = None
        self.collaborative_writer: Optional[CollaborativeWriter] = None

        self._initialize_subsystems()

    def _initialize_subsystems(self):
        """Initialize all subsystems"""
        # Multi-agent system
        if self.config.enable_multi_agent:
            self.orchestrator = create_orchestrator(
                self.llm,
                self.memory,
                self.cache
            )

        # Hierarchical planning
        self.planner = HierarchicalPlanner(
            self.llm,
            self.memory,
            self.cache
        )

        # Self-reflection
        if self.config.enable_self_reflection:
            self.reflector = SelfReflector(
                self.llm,
                self.memory,
                self.cache
            )
            self.improver = ContinuousImprover(
                self.llm,
                self.memory,
                self.cache,
                self.reflector
            )

        # Research
        if self.config.enable_research:
            self.researcher = Researcher(
                self.llm,
                self.memory,
                self.cache
            )
            self.context_gatherer = ContextGatherer(
                self.llm,
                self.memory,
                self.cache,
                self.researcher
            )

        # Document writing
        self.document_writer = DocumentWriter(
            self.llm,
            self.memory,
            self.cache
        )

        if self.config.enable_collaboration:
            self.collaborative_writer = CollaborativeWriter(
                self.llm,
                self.memory,
                self.cache,
                self.document_writer
            )

    async def solve_complex_problem(
        self,
        problem: str,
        context: str = "",
        approach: str = "auto"
    ) -> Dict[str, Any]:
        """
        Solve a complex problem using all available intelligence

        This is the main entry point for super-intelligent problem solving.

        Approach options:
        - "auto": Automatically choose best approach
        - "collaborative": Use multi-agent collaboration
        - "planned": Use hierarchical planning
        - "researched": Use research-backed solving
        - "comprehensive": Use all approaches (slowest but best)
        """
        result = {
            "problem": problem,
            "approach": approach,
            "start_time": datetime.now().isoformat(),
            "stages": []
        }

        try:
            # Stage 1: Gather context
            if self.context_gatherer:
                context_stage = await self._gather_context(problem, context)
                result["stages"].append(context_stage)
                enhanced_context = context_stage.get("enhanced_context", context)
            else:
                enhanced_context = context

            # Stage 2: Choose and execute approach
            if approach == "auto":
                approach = await self._choose_approach(problem, enhanced_context)

            if approach == "collaborative" or approach == "comprehensive":
                collaborative_result = await self._collaborative_solve(
                    problem,
                    enhanced_context
                )
                result["stages"].append(collaborative_result)
                result["solution"] = collaborative_result.get("final_solution")

            elif approach == "planned" or approach == "comprehensive":
                planned_result = await self._planned_solve(
                    problem,
                    enhanced_context
                )
                result["stages"].append(planned_result)
                result["solution"] = planned_result.get("result")

            elif approach == "researched":
                researched_result = await self._researched_solve(
                    problem,
                    enhanced_context
                )
                result["stages"].append(researched_result)
                result["solution"] = researched_result.get("solution")

            # Stage 3: Reflect and improve
            if self.reflector and result.get("solution"):
                reflection_stage = await self._reflect_and_improve(
                    problem,
                    result["solution"],
                    enhanced_context
                )
                result["stages"].append(reflection_stage)

            # Stage 4: Final validation
            validation = await self._validate_solution(
                problem,
                result.get("solution", ""),
                enhanced_context
            )
            result["validation"] = validation

            result["success"] = validation.get("is_valid", False)
            result["end_time"] = datetime.now().isoformat()

        except Exception as e:
            result["error"] = str(e)
            result["success"] = False

        return result

    async def _gather_context(
        self,
        problem: str,
        context: str
    ) -> Dict[str, Any]:
        """Gather comprehensive context"""
        stage = {
            "stage": "context_gathering",
            "start_time": datetime.now().isoformat()
        }

        try:
            if self.context_gatherer:
                context_data = await self.context_gatherer.gather_context(
                    problem,
                    context
                )
                stage["context_data"] = context_data
                stage["enhanced_context"] = self._format_context(context_data)

        except Exception as e:
            stage["error"] = str(e)
            stage["enhanced_context"] = context

        stage["end_time"] = datetime.now().isoformat()
        return stage

    async def _collaborative_solve(
        self,
        problem: str,
        context: str
    ) -> Dict[str, Any]:
        """Solve using multi-agent collaboration"""
        if not self.orchestrator:
            return {"error": "Multi-agent system not enabled"}

        stage = {
            "stage": "collaborative_solving",
            "start_time": datetime.now().isoformat()
        }

        try:
            result = await self.orchestrator.collaborative_solve(
                problem=problem,
                context=context,
                iterations=self.config.max_iterations
            )
            stage["result"] = result

        except Exception as e:
            stage["error"] = str(e)

        stage["end_time"] = datetime.now().isoformat()
        return stage

    async def _planned_solve(
        self,
        problem: str,
        context: str
    ) -> Dict[str, Any]:
        """Solve using hierarchical planning"""
        stage = {
            "stage": "planned_solving",
            "start_time": datetime.now().isoformat()
        }

        try:
            result = await self.planner.solve(
                goal=problem,
                context=context,
                iterations=self.config.max_iterations
            )
            stage["result"] = result

        except Exception as e:
            stage["error"] = str(e)

        stage["end_time"] = datetime.now().isoformat()
        return stage

    async def _researched_solve(
        self,
        problem: str,
        context: str
    ) -> Dict[str, Any]:
        """Solve using research-backed approach"""
        stage = {
            "stage": "researched_solving",
            "start_time": datetime.now().isoformat()
        }

        try:
            # Research the problem
            research = await self.researcher.research(
                question=problem,
                context=context
            )

            # Synthesize findings
            synthesis = await self.researcher.synthesize_findings(research)

            # Use research to inform solution
            solution_prompt = f"""Based on this research, provide a solution:

PROBLEM: {problem}
CONTEXT: {context}
RESEARCH SYNTHESIS: {synthesis}

Provide a comprehensive solution:"""

            messages = [
                {"role": "system", "content": "You are a problem solver."},
                {"role": "user", "content": solution_prompt}
            ]

            response = await self.llm.generate(
                messages=messages,
                temperature=0.5,
                max_tokens=3000
            )

            stage["research"] = research.to_dict() if hasattr(research, 'to_dict') else str(research)
            stage["synthesis"] = synthesis
            stage["solution"] = response.content

        except Exception as e:
            stage["error"] = str(e)

        stage["end_time"] = datetime.now().isoformat()
        return stage

    async def _reflect_and_improve(
        self,
        problem: str,
        solution: str,
        context: str
    ) -> Dict[str, Any]:
        """Reflect on solution and improve"""
        stage = {
            "stage": "reflection_and_improvement",
            "start_time": datetime.now().isoformat()
        }

        try:
            # Reflect on performance
            reflection = await self.reflector.reflect_on_performance(
                task=problem,
                approach=solution,
                outcome=solution,  # Self-assessment
                context=context
            )

            stage["reflection"] = reflection.to_dict()

            # Extract learnings
            learning = await self.reflector.extract_learning(reflection)
            if learning:
                stage["learning"] = learning.to_dict()

            # Generate improvements
            improvements = await self.improver.improve_from_reflection(reflection)
            stage["improvements"] = improvements

        except Exception as e:
            stage["error"] = str(e)

        stage["end_time"] = datetime.now().isoformat()
        return stage

    async def _validate_solution(
        self,
        problem: str,
        solution: str,
        context: str
    ) -> Dict[str, Any]:
        """Validate the solution"""
        validation_prompt = f"""Validate this solution:

PROBLEM: {problem}
SOLUTION: {solution}
CONTEXT: {context}

Evaluate:
1. Does the solution actually solve the problem?
2. Is it complete and correct?
3. Are there any issues or risks?
4. What is the confidence level (0-1)?

Return as JSON:
{{
  "is_valid": true/false,
  "confidence": 0.8,
  "issues": ["..."],
  "suggestions": ["..."]
}}"""

        messages = [
            {"role": "system", "content": "You are a solution validator. Return valid JSON only."},
            {"role": "user", "content": validation_prompt}
        ]

        try:
            response = await self.llm.generate(
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )

            import json
            return json.loads(response.content)

        except Exception as e:
            return {
                "is_valid": False,
                "confidence": 0.0,
                "error": str(e)
            }

    async def write_comprehensive_document(
        self,
        title: str,
        topic: str,
        doc_type: DocumentType,
        context: str = "",
        collaborative: bool = True
    ) -> Dict[str, Any]:
        """
        Write a comprehensive document

        Uses collaborative writing for better quality.
        """
        result = {
            "title": title,
            "topic": topic,
            "type": doc_type.value,
            "start_time": datetime.now().isoformat()
        }

        try:
            # Research the topic first
            if self.researcher:
                research = await self.researcher.research(
                    question=f"Documentation for: {topic}",
                    context=context
                )
                synthesis = await self.researcher.synthesize_findings(research)
                research_findings = [synthesis]
            else:
                research_findings = []

            # Write document
            if collaborative and self.collaborative_writer:
                document = await self.collaborative_writer.collaborative_write(
                    title=title,
                    topic=topic,
                    doc_type=doc_type,
                    context=context,
                    research_findings=research_findings,
                    iterations=self.config.max_iterations
                )
            else:
                document = await self.document_writer.write_document(
                    title=title,
                    topic=topic,
                    doc_type=doc_type,
                    context=context,
                    research_findings=research_findings
                )

            result["document"] = document.to_dict()
            result["markdown"] = document.to_markdown()
            result["success"] = True

        except Exception as e:
            result["error"] = str(e)
            result["success"] = False

        result["end_time"] = datetime.now().isoformat()
        return result

    async def _choose_approach(
        self,
        problem: str,
        context: str
    ) -> str:
        """Automatically choose best approach"""
        # Simple heuristic-based choice
        # In production, would use ML model

        problem_lower = problem.lower()

        # Complex problems benefit from collaboration
        if any(word in problem_lower for word in ["design", "architecture", "system", "complex"]):
            return "collaborative"

        # Multi-step problems benefit from planning
        if any(word in problem_lower for word in ["implement", "build", "create", "step"]):
            return "planned"

        # Information-seeking problems benefit from research
        if any(word in problem_lower for word in ["what", "how", "why", "explain", "describe"]):
            return "researched"

        # Default to comprehensive for best quality
        return "comprehensive"

    def _format_context(self, context_data: Dict[str, Any]) -> str:
        """Format context data into string"""
        formatted = []

        if "research_synthesis" in context_data:
            formatted.append(f"Research: {context_data['research_synthesis']}")

        if "codebase_context" in context_data:
            code_context = context_data.get("codebase_context", [])
            if code_context:
                formatted.append(f"Codebase: Found {len(code_context)} relevant items")

        if "memory_context" in context_data:
            mem_context = context_data.get("memory_context", [])
            if mem_context:
                formatted.append(f"Memory: Found {len(mem_context)} relevant memories")

        return "\n\n".join(formatted)

    async def get_capabilities_summary(self) -> Dict[str, Any]:
        """Get summary of all capabilities"""
        return {
            "multi_agent": self.orchestrator is not None,
            "hierarchical_planning": self.planner is not None,
            "self_reflection": self.reflector is not None,
            "continuous_improvement": self.improver is not None,
            "research": self.researcher is not None,
            "context_gathering": self.context_gatherer is not None,
            "document_writing": self.document_writer is not None,
            "collaborative_writing": self.collaborative_writer is not None,
            "max_iterations": self.config.max_iterations,
            "confidence_threshold": self.config.confidence_threshold
        }


def create_cogos(
    llm_provider: LLMProvider,
    memory: MemoryBackend,
    cache: SmartCache,
    enable_all: bool = True
) -> CogOSSuperIntelligence:
    """
    Create a fully-featured CogOS super-intelligence system

    This is the recommended way to create CogOS instances.
    """
    config = CogOSConfig(
        llm_provider=llm_provider,
        memory=memory,
        cache=cache,
        enable_multi_agent=enable_all,
        enable_self_reflection=enable_all,
        enable_research=enable_all,
        enable_collaboration=enable_all,
        max_iterations=3,
        confidence_threshold=0.7
    )

    return CogOSSuperIntelligence(config)
