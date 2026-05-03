"""
Self-Reflection and Improvement System

This system enables CogOS to:
1. Reflect on its own performance
2. Identify mistakes and areas for improvement
3. Learn from experience
4. Continuously improve its capabilities

This is a key differentiator from static LLMs.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime, timedelta

from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache


class ReflectionType(Enum):
    """Types of reflection"""
    PERFORMANCE = "performance"  # How well did I do?
    ERROR = "error"  # What went wrong?
    STRATEGY = "strategy"  # Should I change approach?
    LEARNING = "learning"  # What did I learn?


@dataclass
class Reflection:
    """A reflection on performance or outcome"""
    reflection_id: str
    reflection_type: ReflectionType
    context: str
    outcome: str
    analysis: str
    insights: List[str]
    improvements: List[str]
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)
    applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reflection_id": self.reflection_id,
            "reflection_type": self.reflection_type.value,
            "context": self.context,
            "outcome": self.outcome,
            "analysis": self.analysis,
            "insights": self.insights,
            "improvements": self.improvements,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat(),
            "applied": self.applied
        }


@dataclass
class Learning:
    """Something learned from experience"""
    learning_id: str
    pattern: str
    lesson: str
    examples: List[str]
    success_rate: float
    last_used: datetime
    usage_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "learning_id": self.learning_id,
            "pattern": self.pattern,
            "lesson": self.lesson,
            "examples": self.examples,
            "success_rate": self.success_rate,
            "last_used": self.last_used.isoformat(),
            "usage_count": self.usage_count
        }


class SelfReflector:
    """
    Reflects on performance and generates insights

    This is the "consciousness" of CogOS - it thinks about its own thinking.
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
        self.reflections: List[Reflection] = []
        self.learnings: List[Learning] = []

    async def reflect_on_performance(
        self,
        task: str,
        approach: str,
        outcome: str,
        context: str = ""
    ) -> Reflection:
        """Reflect on how well a task was performed"""
        reflection_prompt = f"""You are a Self-Reflection Agent. Analyze this performance:

TASK: {task}
APPROACH: {approach}
OUTCOME: {outcome}
CONTEXT: {context}

Provide:
1. ANALYSIS: What worked well? What didn't?
2. INSIGHTS: 3-5 key insights about the performance
3. IMPROVEMENTS: 3-5 specific improvements for next time
4. CONFIDENCE: How confident are you in this analysis? (0-1)

Be honest and constructive. Focus on actionable improvements."""

        messages = [
            {"role": "system", "content": "You are a self-reflection agent. Be analytical and constructive."},
            {"role": "user", "content": reflection_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.5,
            max_tokens=1500
        )

        # Parse reflection
        reflection = Reflection(
            reflection_id=f"ref_{len(self.reflections)}",
            reflection_type=ReflectionType.PERFORMANCE,
            context=context,
            outcome=outcome,
            analysis=response.content,
            insights=[],
            improvements=[],
            confidence=0.7
        )

        self.reflections.append(reflection)
        await self._store_reflection(reflection)

        return reflection

    async def reflect_on_error(
        self,
        task: str,
        error: str,
        context: str = ""
    ) -> Reflection:
        """Reflect on what went wrong"""
        reflection_prompt = f"""You are an Error Analysis Agent. Analyze this error:

TASK: {task}
ERROR: {error}
CONTEXT: {context}

Provide:
1. ROOT CAUSE: Why did this error occur?
2. PREVENTION: How could this have been prevented?
3. RECOVERY: How should this be handled in the future?
4. LEARNING: What should be learned from this?

Be thorough and specific. Focus on prevention and recovery."""

        messages = [
            {"role": "system", "content": "You are an error analysis agent."},
            {"role": "user", "content": reflection_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.3,
            max_tokens=1500
        )

        reflection = Reflection(
            reflection_id=f"err_{len(self.reflections)}",
            reflection_type=ReflectionType.ERROR,
            context=context,
            outcome=error,
            analysis=response.content,
            insights=[],
            improvements=[],
            confidence=0.8
        )

        self.reflections.append(reflection)
        await self._store_reflection(reflection)

        return reflection

    async def extract_learning(
        self,
        reflection: Reflection
    ) -> Optional[Learning]:
        """Extract learnings from reflection"""
        learning_prompt = f"""You are a Learning Extraction Agent. Extract learnings from this reflection:

REFLECTION:
{reflection.analysis}

Extract:
1. PATTERN: What is the general pattern or situation?
2. LESSON: What is the key lesson to remember?
3. EXAMPLES: 2-3 concrete examples of when this applies

Return as JSON:
{{
  "pattern": "...",
  "lesson": "...",
  "examples": ["...", "..."]
}}"""

        messages = [
            {"role": "system", "content": "You are a learning extraction agent. Return valid JSON only."},
            {"role": "user", "content": learning_prompt}
        ]

        try:
            response = await self.llm.generate(
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )

            learning_data = json.loads(response.content)
            learning = Learning(
                learning_id=f"learn_{len(self.learnings)}",
                pattern=learning_data.get("pattern", ""),
                lesson=learning_data.get("lesson", ""),
                examples=learning_data.get("examples", []),
                success_rate=0.0,
                last_used=datetime.now()
            )

            self.learnings.append(learning)
            await self._store_learning(learning)

            return learning

        except (json.JSONDecodeError, Exception):
            return None

    async def get_relevant_learnings(
        self,
        context: str
    ) -> List[Learning]:
        """Get learnings relevant to current context"""
        # Simple similarity matching
        # In production, would use embeddings
        relevant = []

        for learning in self.learnings:
            # Check if pattern matches context
            if learning.pattern.lower() in context.lower():
                relevant.append(learning)
                learning.usage_count += 1
                learning.last_used = datetime.now()

        return relevant

    async def should_change_strategy(
        self,
        task: str,
        current_approach: str,
        outcomes: List[str],
        context: str = ""
    ) -> Dict[str, Any]:
        """Decide if strategy should be changed"""
        strategy_prompt = f"""You are a Strategy Evaluation Agent. Evaluate this approach:

TASK: {task}
CURRENT APPROACH: {current_approach}
OUTCOMES: {json.dumps(outcomes)}
CONTEXT: {context}

Provide:
1. ANALYSIS: Is the current approach working?
2. ALTERNATIVE: What would be a better approach?
3. CONFIDENCE: How confident are you? (0-1)
4. CHANGE: Should we change approach? (yes/no)

Return as JSON:
{{
  "analysis": "...",
  "alternative": "...",
  "confidence": 0.8,
  "change": "yes"
}}"""

        messages = [
            {"role": "system", "content": "You are a strategy evaluation agent. Return valid JSON only."},
            {"role": "user", "content": strategy_prompt}
        ]

        try:
            response = await self.llm.generate(
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )

            return json.loads(response.content)

        except (json.JSONDecodeError, Exception):
            return {
                "analysis": "Unable to evaluate",
                "alternative": None,
                "confidence": 0.0,
                "change": "no"
            }

    async def _store_reflection(self, reflection: Reflection):
        """Store reflection in memory"""
        await self.memory.store(
            key=f"reflection:{reflection.reflection_id}",
            value=reflection.to_dict(),
            metadata={
                "type": "reflection",
                "timestamp": reflection.timestamp.isoformat()
            }
        )

    async def _store_learning(self, learning: Learning):
        """Store learning in memory"""
        await self.memory.store(
            key=f"learning:{learning.learning_id}",
            value=learning.to_dict(),
            metadata={
                "type": "learning",
                "pattern": learning.pattern,
                "usage_count": learning.usage_count
            }
        )

    async def load_learnings(self):
        """Load learnings from memory"""
        # In production, would load from persistent storage
        pass


class ContinuousImprover:
    """
    Continuously improves system based on reflections

    This is the "self-improvement" engine of CogOS.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        memory: MemoryBackend,
        cache: SmartCache,
        reflector: SelfReflector
    ):
        self.llm = llm_provider
        self.memory = memory
        self.cache = cache
        self.reflector = reflector
        self.improvement_history: List[Dict[str, Any]] = []

    async def improve_from_reflection(
        self,
        reflection: Reflection
    ) -> List[str]:
        """Generate improvements from reflection"""
        improvement_prompt = f"""You are a System Improvement Agent. Generate improvements from this reflection:

REFLECTION:
{reflection.analysis}

INSIGHTS: {reflection.insights}
SUGGESTED IMPROVEMENTS: {reflection.improvements}

Generate 3-5 concrete, actionable improvements to the system.
Each improvement should be:
1. Specific (what exactly to change)
2. Actionable (how to implement)
3. Measurable (how to verify it works)

Format as:
1. [IMPROVEMENT TYPE] Description
   Implementation: ...
   Verification: ...

Be practical and focused."""

        messages = [
            {"role": "system", "content": "You are a system improvement agent."},
            {"role": "user", "content": improvement_prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.5,
            max_tokens=1500
        )

        improvements = self._parse_improvements(response.content)

        self.improvement_history.append({
            "reflection_id": reflection.reflection_id,
            "timestamp": datetime.now().isoformat(),
            "improvements": improvements
        })

        return improvements

    def _parse_improvements(self, text: str) -> List[str]:
        """Parse improvements from text"""
        improvements = []
        lines = text.split("\n")

        current_improvement = []
        for line in lines:
            line = line.strip()
            if line and line[0].isdigit():
                if current_improvement:
                    improvements.append("\n".join(current_improvement))
                current_improvement = [line]
            elif current_improvement:
                current_improvement.append(line)

        if current_improvement:
            improvements.append("\n".join(current_improvement))

        return improvements

    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of system performance and improvements"""
        # Calculate metrics
        total_reflections = len(self.reflector.reflections)
        total_learnings = len(self.reflector.learnings)
        total_improvements = len(self.improvement_history)

        # Get recent reflections
        recent_reflections = [
            r for r in self.reflector.reflections
            if r.timestamp > datetime.now() - timedelta(days=7)
        ]

        # Get top learnings by usage
        top_learnings = sorted(
            self.reflector.learnings,
            key=lambda l: l.usage_count,
            reverse=True
        )[:10]

        return {
            "total_reflections": total_reflections,
            "total_learnings": total_learnings,
            "total_improvements": total_improvements,
            "recent_reflections": len(recent_reflections),
            "top_learnings": [l.to_dict() for l in top_learnings],
            "improvement_rate": total_improvements / max(total_reflections, 1)
        }
