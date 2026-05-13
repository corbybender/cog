#!/usr/bin/env python3
"""
Complete Working Example: Integrating CogOS into Your Project

This is a copy-paste example showing how to add CogOS to any project.
"""

import asyncio
import sys
from pathlib import Path

# This is how you import CogOS after installing it
from cog.cogos import create_cogos
from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache


class MyProjectAI:
    """
    Your project's AI assistant using CogOS

    This class wraps CogOS and provides easy-to-use methods
    for your specific project needs.
    """

    def __init__(self):
        """Initialize CogOS once for your entire project"""
        print("🚀 Initializing CogOS for My Project...")

        # Initialize CogOS components
        self.llm = LLMProvider()
        self.memory = MemoryBackend(db_path="my_project_memory.db")
        self.cache = SmartCache(max_size=1000, ttl_seconds=3600)

        # Create CogOS instance
        self.cogos = create_cogos(
            self.llm,
            self.memory,
            self.cache,
            enable_all=True  # Enable all super-intelligence features
        )

        print("✅ CogOS Ready!\n")

    # ========== YOUR CUSTOM METHODS ==========

    async def design_feature(self, feature_description: str) -> dict:
        """Design a new feature using CogOS multi-agent collaboration"""

        print(f"🎨 Designing feature: {feature_description}")

        result = await self.cogos.solve_complex_problem(
            problem=f"""
            Design a feature with these requirements:
            {feature_description}

            Provide:
            1. Architecture design
            2. Implementation steps
            3. Potential challenges
            4. Testing strategy
            """,
            approach="collaborative"  # Multiple agents collaborate
        )

        if result['success']:
            print(f"✅ Design complete (confidence: {result['validation']['confidence']:.1%})")
            return result
        else:
            print(f"❌ Design failed: {result['error']}")
            return result

    async def debug_problem(self, problem_description: str) -> dict:
        """Debug a problem using CogOS research and analysis"""

        print(f"🔍 Debugging: {problem_description}")

        result = await self.cogos.solve_complex_problem(
            problem=f"""
            Debug this issue:
            {problem_description}

            Analyze:
            1. Root cause
            2. Potential solutions
            3. Prevention strategies
            """,
            approach="researched"  # Research-backed approach
        )

        if result['success']:
            print(f"✅ Analysis complete")
            return result
        else:
            print(f"❌ Analysis failed: {result['error']}")
            return result

    async def write_documentation(self, title: str, content: str) -> str:
        """Write documentation using CogOS collaborative writing"""

        print(f"📝 Writing documentation: {title}")

        from cog.document_writer import DocumentType

        result = await self.cogos.write_comprehensive_document(
            title=title,
            topic=content,
            doc_type=DocumentType.DOCUMENTATION,
            collaborative=True  # Multiple agents write and review
        )

        if result['success']:
            doc = result['document']
            print(f"✅ Documentation written ({len(doc['sections'])} sections)")
            return result['markdown']
        else:
            print(f"❌ Documentation failed: {result['error']}")
            return ""

    async def create_implementation_plan(self, goal: str) -> dict:
        """Create an implementation plan using CogOS hierarchical planning"""

        print(f"📋 Creating plan: {goal}")

        result = await self.cogos.solve_complex_problem(
            problem=goal,
            approach="planned"  # Hierarchical planning
        )

        if result['success']:
            # Find the plan in the result
            for stage in result['stages']:
                if 'plan' in stage:
                    plan = stage['plan']
                    print(f"✅ Plan created with {len(plan['subtasks'])} tasks")
                    return plan

        print(f"❌ Planning failed: {result['error']}")
        return {}

    async def optimize_code(self, code: str, context: str = "") -> dict:
        """Optimize code using CogOS"""

        print(f"⚡ Optimizing code...")

        result = await self.cogos.solve_complex_problem(
            problem=f"""
            Optimize this code:
            {code}

            Context: {context}

            Provide:
            1. Optimized version
            2. Performance improvements
            3. Trade-offs
            """,
            approach="collaborative"  # Multiple perspectives
        )

        if result['success']:
            print(f"✅ Optimization complete")
            return result
        else:
            print(f"❌ Optimization failed: {result['error']}")
            return result


# ========== USAGE EXAMPLES ==========

async def example_1_design_feature():
    """Example 1: Design a new feature"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Design a Feature")
    print("="*80 + "\n")

    ai = MyProjectAI()

    result = await ai.design_feature(
        """
        Feature: Real-time notifications
        - Should support 100k+ concurrent users
        - Low latency (<100ms)
        - Reliable (no lost messages)
        - Scalable architecture
        """
    )

    if result['success']:
        print("\n📄 Design Solution:")
        print(result['solution'][:500] + "...")
        print(f"\n📊 Confidence: {result['validation']['confidence']:.1%}")


async def example_2_debug_issue():
    """Example 2: Debug a problem"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Debug a Problem")
    print("="*80 + "\n")

    ai = MyProjectAI()

    result = await ai.debug_problem(
        """
        Database queries are timing out after 30 seconds
        under heavy load (1000+ concurrent requests).
        Database: PostgreSQL 13
        Pool size: 20
        """
    )

    if result['success']:
        print("\n🔍 Analysis:")
        print(result['solution'][:500] + "...")


async def example_3_write_docs():
    """Example 3: Write documentation"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Write Documentation")
    print("="*80 + "\n")

    ai = MyProjectAI()

    markdown = await ai.write_documentation(
        title="API Authentication Guide",
        content="""
        Complete guide to implementing authentication in our REST API.

        Topics:
        - JWT token-based authentication
        - OAuth2 flows
        - API key management
        - Rate limiting
        - Security best practices
        """
    )

    if markdown:
        print("\n📝 Documentation Preview:")
        print(markdown[:500] + "...")
        print(f"\n📊 Total length: {len(markdown)} characters")


async def example_4_create_plan():
    """Example 4: Create implementation plan"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Create Implementation Plan")
    print("="*80 + "\n")

    ai = MyProjectAI()

    plan = await ai.create_implementation_plan(
        """
        Implement a caching layer for the application

        Requirements:
        - Reduce database load by 80%
        - Cache invalidation strategy
        - Distributed caching support
        - Fallback mechanisms
        """
    )

    if plan:
        print("\n📋 Implementation Plan:")
        print(f"Goal: {plan.get('title', 'N/A')}")
        print(f"Subtasks: {len(plan.get('subtasks', []))}\n")

        for i, task in enumerate(plan.get('subtasks', [])[:5], 1):
            print(f"  {i}. {task.get('title', 'N/A')}")


async def example_5_optimize_code():
    """Example 5: Optimize code"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Optimize Code")
    print("="*80 + "\n")

    ai = MyProjectAI()

    code = """
    def process_users(users):
        result = []
        for user in users:
            for order in user.orders:
                if order.status == 'pending':
                    result.append({
                        'user_id': user.id,
                        'order_id': order.id,
                        'total': order.total
                    })
        return result
    """

    result = await ai.optimize_code(
        code,
        context="Processing 1M+ user records"
    )

    if result['success']:
        print("\n⚡ Optimization:")
        print(result['solution'][:500] + "...")


# ========== MAIN ==========

async def main():
    """Run all examples"""

    print("\n" + "="*80)
    print("🚀 COGNOS INTEGRATION EXAMPLES")
    print("Complete working examples for your project")
    print("="*80)

    try:
        # Run examples
        await example_1_design_feature()
        await asyncio.sleep(1)

        await example_2_debug_issue()
        await asyncio.sleep(1)

        await example_3_write_docs()
        await asyncio.sleep(1)

        await example_4_create_plan()
        await asyncio.sleep(1)

        await example_5_optimize_code()

        print("\n" + "="*80)
        print("✅ ALL EXAMPLES COMPLETE!")
        print("="*80)

        print("\n📚 Next Steps:")
        print("  1. Copy the MyProjectAI class to your project")
        print("  2. Customize the methods for your needs")
        print("  3. Add more methods as needed")
        print("  4. Use in your codebase")
        print("\n💡 Tip: Initialize once, use everywhere!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check if user wants to run specific example
    if len(sys.argv) > 1:
        example_num = sys.argv[1]

        examples = {
            "1": example_1_design_feature,
            "2": example_2_debug_issue,
            "3": example_3_write_docs,
            "4": example_4_create_plan,
            "5": example_5_optimize_code,
        }

        if example_num in examples:
            asyncio.run(examples[example_num]())
        else:
            print(f"Unknown example: {example_num}")
            print("Available examples: 1, 2, 3, 4, 5")
    else:
        # Run all examples
        asyncio.run(main())
