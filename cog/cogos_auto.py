#!/usr/bin/env python3
"""
CogOS Auto-Integrator: Automatic AI Augmentation

This system automatically integrates CogOS into ANY AI project
without requiring manual code changes.

The AI will automatically use CogOS when it detects complex tasks.
"""

import sys
import asyncio
from pathlib import Path
from typing import Any, Callable, Optional, Dict
from functools import wraps

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cog.cogos import create_cogos
from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache


class CogOSAutoIntegrator:
    """
    Automatically integrate CogOS into any AI system

    Usage:
        # Just wrap your LLM and it automatically uses CogOS!
        ai = CogOSAutoIntegrator()
        response = await ai.generate("your prompt")
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern - one CogOS instance for entire project"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        auto_detect_complexity: bool = True,
        complexity_threshold: float = 0.5,
        enable_caching: bool = True
    ):
        """Initialize auto-integrator"""

        # Only initialize once
        if self._initialized:
            return

        print("🚀 CogOS Auto-Integrator: Initializing...")

        # Initialize CogOS
        self.llm = LLMProvider()
        self.memory = MemoryBackend(db_path=":memory:")
        self.cache = SmartCache(max_size=1000, ttl_seconds=3600)
        self.cogos = create_cogos(self.llm, self.memory, self.cache, enable_all=True)

        # Settings
        self.auto_detect_complexity = auto_detect_complexity
        self.complexity_threshold = complexity_threshold
        self.enable_caching = enable_caching

        # Stats
        self.stats = {
            "total_requests": 0,
            "cogos_used": 0,
            "direct_llm": 0,
            "cache_hits": 0
        }

        print("✅ CogOS Auto-Integrator: Ready!")
        print("   → AI will automatically use CogOS for complex tasks\n")

        self._initialized = True

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        force_cogos: bool = False,
        **kwargs
    ) -> str:
        """
        Generate response - automatically uses CogOS if needed

        This is the main method - just replace your LLM calls with this!
        """

        self.stats["total_requests"] += 1

        # Check cache first
        if self.enable_caching:
            cached = await self._check_cache(prompt)
            if cached:
                self.stats["cache_hits"] += 1
                return cached

        # Decide whether to use CogOS
        use_cogos = force_cogos

        if self.auto_detect_complexity and not force_cogos:
            complexity = await self._detect_complexity(prompt)
            use_cogos = complexity > self.complexity_threshold

        # Use appropriate method
        if use_cogos:
            self.stats["cogos_used"] += 1
            response = await self._use_cogos(prompt, **kwargs)
        else:
            self.stats["direct_llm"] += 1
            response = await self._use_llm(prompt, temperature, max_tokens, **kwargs)

        # Cache response
        if self.enable_caching:
            await self._cache_response(prompt, response)

        return response

    async def _detect_complexity(self, prompt: str) -> float:
        """Detect if prompt is complex (0-1 scale)"""

        # Simple heuristic-based detection
        prompt_lower = prompt.lower()

        # Complexity indicators
        complex_indicators = {
            "design": 0.8,
            "architecture": 0.9,
            "implement": 0.7,
            "build": 0.6,
            "create": 0.5,
            "optimize": 0.7,
            "refactor": 0.6,
            "debug": 0.6,
            "solve": 0.5,
            "plan": 0.7,
            "research": 0.6,
            "analyze": 0.5,
            "review": 0.5,
            "multiple steps": 0.8,
            "step by step": 0.7,
        }

        # Check for indicators
        max_score = 0.0
        for indicator, score in complex_indicators.items():
            if indicator in prompt_lower:
                max_score = max(max_score, score)

        # Length factor (longer prompts = more complex)
        length_factor = min(len(prompt) / 1000, 0.3)

        # Question marks (questions = less complex)
        question_factor = prompt.count("?") * -0.05

        # Calculate final complexity
        complexity = max_score + length_factor + question_factor
        complexity = max(0.0, min(1.0, complexity))

        return complexity

    async def _use_cogos(self, prompt: str, **kwargs) -> str:
        """Use CogOS for complex tasks"""

        # Select best approach
        approach = await self._select_approach(prompt)

        # Use CogOS
        result = await self.cogos.solve_complex_problem(
            problem=prompt,
            approach=approach
        )

        if result.get('success'):
            # Format response
            parts = []

            if result.get('solution'):
                parts.append(result['solution'])

            # Add confidence info
            validation = result.get('validation', {})
            if validation and validation.get('confidence', 0) < 0.8:
                parts.append(f"\n\n(Confidence: {validation['confidence']:.1%})")

            response = "\n".join(parts)

            # Add metadata
            response += "\n\n_[Powered by CogOS multi-agent system]_"

            return response
        else:
            # Fallback to LLM
            return await self._use_llm(prompt, **kwargs)

    async def _select_approach(self, prompt: str) -> str:
        """Select best CogOS approach"""

        prompt_lower = prompt.lower()

        if "design" in prompt_lower or "architecture" in prompt_lower:
            return "collaborative"
        elif "implement" in prompt_lower or "build" in prompt_lower:
            return "planned"
        elif "research" in prompt_lower or "find" in prompt_lower:
            return "researched"
        else:
            return "auto"

    async def _use_llm(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Use LLM directly for simple tasks"""

        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.content

    async def _check_cache(self, prompt: str) -> Optional[str]:
        """Check cache for previous response"""
        # Simple in-memory cache
        if hasattr(self, '_response_cache'):
            return self._response_cache.get(prompt)
        return None

    async def _cache_response(self, prompt: str, response: str):
        """Cache response"""
        if not hasattr(self, '_response_cache'):
            self._response_cache = {}

        # Limit cache size
        if len(self._response_cache) > 100:
            # Remove oldest entry
            oldest = next(iter(self._response_cache))
            del self._response_cache[oldest]

        self._response_cache[prompt] = response

    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        total = self.stats["total_requests"]
        return {
            **self.stats,
            "cogos_percentage": (self.stats["cogos_used"] / total * 100) if total > 0 else 0,
            "cache_hit_rate": (self.stats["cache_hits"] / total * 100) if total > 0 else 0
        }


# ========== AUTOMATIC DECORATORS ==========

def auto_cogos(func: Callable) -> Callable:
    """
    Decorator to automatically use CogOS for any LLM function

    Usage:
        @auto_cogos
        async def my_llm_function(prompt: str) -> str:
            # Your regular LLM code
            return response

        # Now it automatically uses CogOS when needed!
    """

    @wraps(func)
    async def wrapper(prompt: str, *args, **kwargs):
        # Get integrator
        integrator = CogOSAutoIntegrator()

        # Check complexity
        if integrator.auto_detect_complexity:
            complexity = await integrator._detect_complexity(prompt)

            if complexity > integrator.complexity_threshold:
                # Use CogOS
                return await integrator._use_cogos(prompt, **kwargs)

        # Use original function
        return await func(prompt, *args, **kwargs)

    return wrapper


# ========== AUTOMATIC IMPORT HOOK ==========

def patch_openai():
    """
    Automatically patch OpenAI to use CogOS

    Call this once at the start of your project:
        import cogos_auto
        cogos_auto.patch_openai()

    Now all OpenAI calls automatically use CogOS when appropriate!
    """

    try:
        import openai

        # Store original completion method
        original_completion = openai.Completion.create
        original_chat_completion = openai.ChatCompletion.create

        # Patch completion
        def patched_completion(*args, **kwargs):
            prompt = kwargs.get('prompt', '')

            # Check if should use CogOS
            integrator = CogOSAutoIntegrator()

            async def _check():
                complexity = await integrator._detect_complexity(prompt)
                return complexity > integrator.complexity_threshold

            # Run async check
            complexity_check = asyncio.run(_check())

            if complexity_check:
                # Use CogOS (run in sync wrapper)
                async def _use_cogos():
                    return await integrator._use_cogos(prompt)

                result = asyncio.run(_use_cogos())
                # Return in OpenAI format
                return type('obj', (object,), {'choices': [{'text': result}]})()
            else:
                # Use original OpenAI
                return original_completion(*args, **kwargs)

        # Patch chat completion
        def patched_chat_completion(*args, **kwargs):
            messages = kwargs.get('messages', [])
            prompt = messages[-1].get('content', '') if messages else ''

            # Check if should use CogOS
            integrator = CogOSAutoIntegrator()

            async def _check():
                complexity = await integrator._detect_complexity(prompt)
                return complexity > integrator.complexity_threshold

            complexity_check = asyncio.run(_check())

            if complexity_check:
                # Use CogOS
                async def _use_cogos():
                    return await integrator._use_cogos(prompt)

                result = asyncio.run(_use_cogos())
                # Return in OpenAI format
                return type('obj', (object,), {'choices': [{'message': {'content': result}}]})()
            else:
                # Use original OpenAI
                return original_chat_completion(*args, **kwargs)

        # Apply patches
        openai.Completion.create = patched_completion
        openai.ChatCompletion.create = patched_chat_completion

        print("✅ OpenAI patched - will automatically use CogOS for complex tasks!")

    except ImportError:
        print("⚠️  OpenAI not installed - skipping OpenAI patch")


# ========== SIMPLE USAGE ==========

async def demo_auto_integration():
    """Demo of automatic integration"""

    print("\n" + "="*80)
    print("🤖 CogOS Auto-Integration Demo")
    print("="*80 + "\n")

    # Create auto-integrator
    ai = CogOSAutoIntegrator()

    # Test prompts with different complexity
    test_prompts = [
        ("Simple", "What is Python?"),
        ("Complex", "Design a scalable microservices architecture for an e-commerce platform that handles 100k concurrent users"),
        ("Medium", "How do I optimize database queries?"),
        ("Very Complex", "Implement a real-time collaboration system similar to Google Docs with operational transformation and conflict resolution"),
        ("Simple", "What is the capital of France?"),
    ]

    for label, prompt in test_prompts:
        print(f"\n{'='*80}")
        print(f"{label} Question")
        print(f"{'='*80}")
        print(f"Prompt: {prompt[:80]}...")
        print(f"\nThinking...")

        response = await ai.generate(prompt)

        print(f"\nResponse (first 300 chars):\n{response[:300]}...")

    # Show stats
    print(f"\n{'='*80}")
    print("📊 Statistics")
    print(f"{'='*80}")
    stats = ai.get_stats()
    print(f"Total requests: {stats['total_requests']}")
    print(f"CogOS used: {stats['cogos_used']} ({stats['cogos_percentage']:.1f}%)")
    print(f"Direct LLM: {stats['direct_llm']}")
    print(f"Cache hits: {stats['cache_hits']}")


if __name__ == "__main__":
    # Demo auto integration
    asyncio.run(demo_auto_integration())

    # Show how to patch OpenAI
    print("\n" + "="*80)
    print("🔧 Automatic OpenAI Patch")
    print("="*80 + "\n")

    print("To automatically patch OpenAI in your project:")
    print("""
    import cogos_auto
    cogos_auto.patch_openai()

    # Now use OpenAI normally - it will automatically use CogOS when needed!
    import openai
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Design a complex system"}]
    )
    """)
