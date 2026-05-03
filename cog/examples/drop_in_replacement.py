#!/usr/bin/env python3
"""
Example: Drop-in Replacement for Any AI System

This shows how to automatically upgrade ANY AI system to use CogOS
with ZERO code changes to the original system.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cogos_auto import CogOSAutoIntegrator, patch_openai, auto_cogos


# ========== EXAMPLE 1: Simple Replacement ==========

# BEFORE: Your original code
async def original_ai_system(prompt: str) -> str:
    """Your existing AI system - NO changes needed!"""
    from cog.llm.provider import LLMProvider

    llm = LLMProvider()

    messages = [
        {"role": "system", "content": "You are a helpful AI."},
        {"role": "user", "content": prompt}
    ]

    response = await llm.generate(
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )

    return response.content


# AFTER: Just replace one line!
async def upgraded_ai_system(prompt: str) -> str:
    """Your AI system upgraded with CogOS - ONLY ONE LINE CHANGED!"""

    # OLD: llm = LLMProvider()
    # NEW: Use CogOS Auto-Integrator
    ai = CogOSAutoIntegrator()  # ← ONE LINE CHANGE!

    # Everything else stays exactly the same
    return await ai.generate(prompt)


# ========== EXAMPLE 2: Decorator Approach ==========

@auto_cogos  # ← Just add this decorator!
async def my_ai_function(prompt: str) -> str:
    """Your AI function - just add @auto_cogs decorator!"""
    from cog.llm.provider import LLMProvider

    llm = LLMProvider()
    messages = [
        {"role": "system", "content": "You are a helpful AI."},
        {"role": "user", "content": prompt}
    ]

    response = await llm.generate(
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )

    return response.content


# ========== EXAMPLE 3: Automatic OpenAI Patch ==========

def example_openai_patch():
    """
    Example: Patch OpenAI to automatically use CogOS
    """
    print("\n" + "="*80)
    print("🔧 Example 3: Automatic OpenAI Patch")
    print("="*80 + "\n")

    # Just call this once at the start of your project
    patch_openai()

    # Now use OpenAI normally - it will automatically use CogOS for complex tasks!
    print("""
    import openai

    # This will now automatically use CogOS for complex prompts!
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Design a complex microservices architecture"}]
    )

    print(response.choices[0].message.content)
    """)


# ========== DEMO ==========

async def demo_drop_in_replacement():
    """Demo showing drop-in replacement"""

    print("\n" + "="*80)
    print("🚀 DEMO: Drop-in Replacement for Any AI System")
    print("="*80 + "\n")

    # Create upgraded AI
    ai = CogOSAutoIntegrator()

    print("Your AI system is now upgraded with CogOS super-intelligence!")
    print("\nIt will automatically:")
    print("  → Use CogOS for complex tasks")
    print("  → Use direct LLM for simple tasks")
    print("  → Cache responses for speed")
    print("  → Track statistics")
    print("\nNo code changes needed - just replace your LLM call!\n")

    # Test cases
    test_cases = [
        ("Simple question", "What is the capital of France?"),
        ("System design", "Design a scalable real-time collaboration platform with 10k concurrent users"),
        ("Code optimization", "Optimize this database query that times out under load"),
        ("Simple fact", "Who wrote the novel '1984'?"),
        ("Complex architecture", "Design a microservices architecture for a global e-commerce platform"),
    ]

    for i, (label, prompt) in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}: {label}")
        print(f"{'='*80}")
        print(f"Prompt: {prompt[:80]}...")
        print(f"\nAI is thinking...")

        # Use the upgraded AI
        response = await ai.generate(prompt)

        # Show which method was used
        if "CogOS" in response:
            method = "🧠 CogOS (multi-agent)"
        else:
            method = "⚡ Direct LLM"

        print(f"\nMethod: {method}")
        print(f"\nResponse (first 300 chars):\n{response[:300]}...")

    # Show final statistics
    print(f"\n{'='*80}")
    print("📊 Final Statistics")
    print(f"{'='*80}")

    stats = ai.get_stats()
    print(f"\nTotal requests: {stats['total_requests']}")
    print(f"CogOS used: {stats['cogos_used']} ({stats['cogos_percentage']:.1f}%)")
    print(f"Direct LLM: {stats['direct_llm']}")
    print(f"Cache hits: {stats['cache_hits']} ({stats['cache_hit_rate']:.1f}%)")

    print(f"\n💡 Your AI automatically used CogOS for {stats['cogos_percentage']:.1f}% of requests!")
    print(f"   Complex tasks got multi-agent collaboration")
    print(f"   Simple tasks were handled directly (faster)")
    print(f"   Duplicates were served from cache (even faster)")


async def demo_decorator_approach():
    """Demo showing decorator approach"""

    print("\n" + "="*80)
    print("🎨 DEMO: Decorator Approach")
    print("="*80 + "\n")

    print("Just add @auto_cogos decorator to any function!")
    print("\nExample:")
    print("""
    @auto_cogos  # ← Add this!
    async def my_ai(prompt: str) -> str:
        # Your existing code
        return response
    """)

    # Test the decorated function
    print("\nTesting decorated function:\n")

    simple_prompt = "What is 2+2?"
    complex_prompt = "Design a distributed system architecture"

    print(f"Simple prompt: {simple_prompt}")
    response1 = await my_ai_function(simple_prompt)
    print(f"Response: {response1[:100]}...\n")

    print(f"Complex prompt: {complex_prompt[:60]}...")
    response2 = await my_ai_function(complex_prompt)
    print(f"Response: {response2[:100]}...")


async def main():
    """Run all demos"""

    # Demo 1: Drop-in replacement
    await demo_drop_in_replacement()

    await asyncio.sleep(1)

    # Demo 2: Decorator approach
    await demo_decorator_approach()

    await asyncio.sleep(1)

    # Demo 3: OpenAI patch
    example_openai_patch()

    print("\n" + "="*80)
    print("✅ ALL DEMOS COMPLETE!")
    print("="*80)

    print("\n📚 Summary: Three Ways to Auto-Integrate")
    print("\n1. Drop-in Replacement:")
    print("   ai = CogOSAutoIntegrator()")
    print("   response = await ai.generate(prompt)")
    print("\n2. Decorator:")
    print("   @auto_cogos")
    print("   async def my_ai(prompt): ...")
    print("\n3. OpenAI Patch:")
    print("   patch_openai()")
    print("   # Use OpenAI normally")
    print("\n✨ All automatic - zero code changes to your AI logic!")


if __name__ == "__main__":
    asyncio.run(main())
