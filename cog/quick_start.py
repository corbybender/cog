#!/usr/bin/env python3
"""
Quick Start Guide for CogOS 2.0 Super-Intelligence

This script shows you how to use CogOS to solve complex problems
that would be difficult or impossible for single-pass LLMs like Claude.
"""

import asyncio
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cog.cogos import create_cogos
from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache
from cog.document_writer import DocumentType


async def example_1_simple_problem():
    """Example 1: Solve a simple problem"""
    print("\n" + "="*80)
    print("Example 1: Simple Problem Solving")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache)

    # Solve a problem
    result = await cogos.solve_complex_problem(
        problem="What are the key differences between PostgreSQL and MySQL?",
        approach="researched"  # Research-backed approach
    )

    if result.get("success"):
        print("\n✓ Solved!")
        print("\nSolution:")
        print(result.get("solution", "")[:500])
        print("\nValidation:")
        print(f"  Valid: {result.get('validation', {}).get('is_valid', False)}")
        print(f"  Confidence: {result.get('validation', {}).get('confidence', 0):.2f}")


async def example_2_complex_problem():
    """Example 2: Solve a complex problem with collaboration"""
    print("\n" + "="*80)
    print("Example 2: Complex Problem with Multi-Agent Collaboration")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache)

    # Solve a complex problem
    result = await cogos.solve_complex_problem(
        problem="Design a caching strategy for a high-traffic web application",
        approach="collaborative"  # Multi-agent collaboration
    )

    if result.get("success"):
        print("\n✓ Solved with collaboration!")
        print("\nCollaboration Stages:")
        for i, stage in enumerate(result.get("stages", []), 1):
            print(f"  {i}. {stage.get('stage', 'unknown')}")

        print("\nSolution Preview:")
        solution = result.get("solution", "")
        print(solution[:300] if len(solution) > 300 else solution)


async def example_3_task_planning():
    """Example 3: Create an execution plan"""
    print("\n" + "="*80)
    print("Example 3: Hierarchical Task Planning")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache)

    # Create a plan
    result = await cogos.solve_complex_problem(
        problem="Implement a user authentication system with JWT tokens",
        approach="planned"  # Hierarchical planning
    )

    if result.get("success"):
        print("\n✓ Plan created!")

        # Show plan structure
        for stage in result.get("stages", []):
            if "plan" in stage:
                plan = stage["plan"]
                print(f"\nPlan: {plan.get('title', 'N/A')}")
                print(f"Subtasks: {len(plan.get('subtasks', []))}")

                for i, subtask in enumerate(plan.get("subtasks", [])[:5], 1):
                    print(f"  {i}. {subtask.get('title', 'N/A')}")


async def example_4_document_writing():
    """Example 4: Write a document"""
    print("\n" + "="*80)
    print("Example 4: Collaborative Document Writing")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache)

    # Write a document
    result = await cogos.write_comprehensive_document(
        title="API Security Best Practices",
        topic="Security considerations for RESTful API design",
        doc_type=DocumentType.TECHNICAL_REPORT,
        collaborative=True
    )

    if result.get("success"):
        print("\n✓ Document written!")

        document = result.get("document", {})
        sections = document.get("sections", [])
        print(f"\nSections: {len(sections)}")

        for i, section in enumerate(sections[:5], 1):
            print(f"  {i}. {section.get('title', 'N/A')}")

        markdown = result.get("markdown", "")
        print(f"\nMarkdown length: {len(markdown)} characters")
        print(f"Preview:\n{markdown[:200]}...")


async def example_5_comprehensive():
    """Example 5: Use all capabilities (comprehensive approach)"""
    print("\n" + "="*80)
    print("Example 5: Comprehensive Approach (All Capabilities)")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache)

    # Solve comprehensively
    result = await cogos.solve_complex_problem(
        problem="Design a scalable real-time notification system",
        approach="comprehensive"  # Uses ALL capabilities
    )

    if result.get("success"):
        print("\n✓ Comprehensive solution!")

        print("\nExecution Pipeline:")
        for i, stage in enumerate(result.get("stages", []), 1):
            stage_name = stage.get("stage", "unknown")
            has_error = "error" in stage
            status = "✗" if has_error else "✓"
            print(f"  {status} {i}. {stage_name}")

        print("\nValidation:")
        validation = result.get("validation", {})
        print(f"  Valid: {validation.get('is_valid', False)}")
        print(f"  Confidence: {validation.get('confidence', 0):.2f}")


async def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("CogOS 2.0 Quick Start Guide")
    print("Learn how to use super-intelligence to solve complex problems")
    print("="*80)

    print("\nThese examples show how CogOS 2.0 goes beyond single-pass LLMs:")
    print("  1. Simple problem solving with research")
    print("  2. Complex problem with multi-agent collaboration")
    print("  3. Hierarchical task planning")
    print("  4. Collaborative document writing")
    print("  5. Comprehensive approach using all capabilities")

    try:
        # Run examples
        await example_1_simple_problem()
        await asyncio.sleep(1)

        await example_2_complex_problem()
        await asyncio.sleep(1)

        await example_3_task_planning()
        await asyncio.sleep(1)

        await example_4_document_writing()
        await asyncio.sleep(1)

        await example_5_comprehensive()

        print("\n" + "="*80)
        print("Quick Start Complete!")
        print("="*80)

        print("\nNext Steps:")
        print("  1. Try your own problems:")
        print("     cogos solve 'your problem' --approach comprehensive")
        print()
        print("  2. Write documents:")
        print("     cogos write 'Title' 'Topic' --collaborative --output doc.md")
        print()
        print("  3. Run the full demo:")
        print("     python demo_super_intelligence.py")
        print()
        print("  4. Use in your code:")
        print("     from cog.cogos import create_cogos")
        print("     cogos = create_cogos(llm, memory, cache)")
        print("     result = await cogos.solve_complex_problem(your_problem)")
        print()

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
