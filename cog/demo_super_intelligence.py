#!/usr/bin/env python3
"""
CogOS Super-Intelligence Demo

This demonstrates the superior capabilities of CogOS over single-pass LLMs like Claude.

The demo shows:
1. Multi-agent collaborative problem solving
2. Hierarchical task planning
3. Self-reflection and improvement
4. Research-backed decision making
5. Collaborative document writing
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cog.cogos import create_cogos, CogOSConfig
from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache
from cog.document_writer import DocumentType


async def demo_multi_agent_collaboration():
    """Demo 1: Multi-agent collaborative problem solving"""
    print("\n" + "="*80)
    print("DEMO 1: Multi-Agent Collaborative Problem Solving")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache, enable_all=True)

    # Complex problem that benefits from multiple perspectives
    problem = """
    Design a scalable microservices architecture for a real-time collaboration platform
    similar to Google Docs. The system must support:
    - Real-time document editing with multiple users
    - Conflict resolution and operational transformation
    - Low-latency updates (<100ms)
    - Support for 10,000+ concurrent users per document
    - Automatic saving and versioning
    - Offline support with sync
    """

    print(f"\nProblem: Design real-time collaboration platform")
    print(f"Approach: Multi-agent collaboration (Planner, Architect, Coder, Critic, Optimizer)")

    # Solve using multi-agent collaboration
    result = await cogos.solve_complex_problem(
        problem=problem,
        approach="collaborative"
    )

    print("\n--- Result ---")
    if result.get("success"):
        print(f"✓ Solved successfully!")
        print(f"\nSolution Summary:")
        solution = result.get("solution", "")
        if len(solution) > 500:
            print(solution[:500] + "...")
        else:
            print(solution)

        # Show collaboration stages
        print(f"\nCollaboration Stages: {len(result.get('stages', []))}")
        for i, stage in enumerate(result.get("stages", []), 1):
            print(f"  {i}. {stage.get('stage', 'unknown')}")
    else:
        print(f"✗ Failed: {result.get('error')}")


async def demo_hierarchical_planning():
    """Demo 2: Hierarchical task planning"""
    print("\n" + "="*80)
    print("DEMO 2: Hierarchical Task Planning")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache, enable_all=True)

    # Complex implementation task
    task = """
    Implement a complete authentication and authorization system for a web application
    """

    print(f"\nTask: {task.strip()}")
    print(f"Approach: Hierarchical planning with execution")

    # Solve using hierarchical planning
    result = await cogos.solve_complex_problem(
        problem=task,
        approach="planned"
    )

    print("\n--- Result ---")
    if result.get("success"):
        print(f"✓ Planned and executed successfully!")

        # Show plan structure
        for stage in result.get("stages", []):
            if "plan" in stage:
                plan = stage["plan"]
                print(f"\nPlan Structure:")
                print(f"  Title: {plan.get('title', 'N/A')}")
                print(f"  Subtasks: {len(plan.get('subtasks', []))}")

                for i, subtask in enumerate(plan.get("subtasks", [])[:3], 1):
                    print(f"    {i}. {subtask.get('title', 'N/A')}")
    else:
        print(f"✗ Failed: {result.get('error')}")


async def demo_research_backed_solving():
    """Demo 3: Research-backed problem solving"""
    print("\n" + "="*80)
    print("DEMO 3: Research-Backed Problem Solving")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache, enable_all=True)

    # Question that requires research
    question = """
    What are the best practices for implementing WebSocket authentication
    in a Node.js application with JWT tokens?
    """

    print(f"\nQuestion: {question.strip()}")
    print(f"Approach: Research-backed solving")

    # Solve using research
    result = await cogos.solve_complex_problem(
        problem=question,
        approach="researched"
    )

    print("\n--- Result ---")
    if result.get("success"):
        print(f"✓ Researched and answered successfully!")

        # Show research was conducted
        for stage in result.get("stages", []):
            if stage.get("stage") == "researched_solving":
                print(f"\nResearch conducted:")
                if "synthesis" in stage:
                    print(f"  Synthesis: {stage['synthesis'][:200]}...")
    else:
        print(f"✗ Failed: {result.get('error')}")


async def demo_collaborative_writing():
    """Demo 4: Collaborative document writing"""
    print("\n" + "="*80)
    print("DEMO 4: Collaborative Document Writing")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache, enable_all=True)

    # Technical documentation task
    print(f"\nTask: Write comprehensive API documentation")
    print(f"Topic: RESTful API design best practices")
    print(f"Approach: Collaborative writing with multiple reviewers")

    # Write document collaboratively
    result = await cogos.write_comprehensive_document(
        title="RESTful API Design Best Practices",
        topic="RESTful API design principles, patterns, and best practices for modern web applications",
        doc_type=DocumentType.TECHNICAL_REPORT,
        context="Target audience: Senior backend developers",
        collaborative=True
    )

    print("\n--- Result ---")
    if result.get("success"):
        print(f"✓ Document written successfully!")
        print(f"\nDocument Structure:")

        document = result.get("document", {})
        sections = document.get("sections", [])
        print(f"  Total sections: {len(sections)}")

        for i, section in enumerate(sections[:5], 1):
            print(f"    {i}. {section.get('title', 'N/A')}")
            if len(sections) > 5:
                print(f"    ... and {len(sections) - 5} more sections")

        # Show markdown preview
        markdown = result.get("markdown", "")
        print(f"\nMarkdown Preview (first 500 chars):")
        print(markdown[:500] + "...")
    else:
        print(f"✗ Failed: {result.get('error')}")


async def demo_self_reflection():
    """Demo 5: Self-reflection and improvement"""
    print("\n" + "="*80)
    print("DEMO 5: Self-Reflection and Continuous Improvement")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache, enable_all=True)

    # Task that will generate reflection data
    task = "Implement a caching layer for a database"

    print(f"\nTask: {task}")
    print(f"Approach: Comprehensive (with reflection and improvement)")

    # Solve with reflection
    result = await cogos.solve_complex_problem(
        problem=task,
        approach="comprehensive"
    )

    print("\n--- Result ---")
    if result.get("success"):
        print(f"✓ Solved with reflection!")

        # Show reflection stage
        for stage in result.get("stages", []):
            if stage.get("stage") == "reflection_and_improvement":
                print(f"\nReflection conducted:")
                reflection = stage.get("reflection", {})
                print(f"  Type: {reflection.get('reflection_type', 'N/A')}")
                print(f"  Confidence: {reflection.get('confidence', 0):.2f}")

                improvements = stage.get("improvements", [])
                print(f"  Improvements generated: {len(improvements)}")
    else:
        print(f"✗ Failed: {result.get('error')}")


async def demo_comprehensive_approach():
    """Demo 6: Comprehensive approach using all capabilities"""
    print("\n" + "="*80)
    print("DEMO 6: Comprehensive Approach (All Systems)")
    print("="*80)

    # Create CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache, enable_all=True)

    # Very complex problem
    problem = """
    Design and plan the implementation of a distributed task queue system
    that can handle millions of jobs per hour with the following requirements:
    - Fault tolerance and retry logic
    - Priority queues
    - Scheduled jobs (cron-like)
    - Job dependencies and workflows
    - Real-time monitoring and metrics
    - Horizontal scalability
    - Multiple worker types (CPU, I/O, GPU)
    """

    print(f"\nProblem: Distributed task queue system")
    print(f"Approach: Comprehensive (uses ALL capabilities)")
    print(f"\nThis will:")
    print(f"  1. Research existing solutions")
    print(f"  2. Plan hierarchical implementation")
    print(f"  3. Collaborate with multiple agents")
    print(f"  4. Reflect on the solution")
    print(f"  5. Validate the approach")

    # Solve comprehensively
    result = await cogos.solve_complex_problem(
        problem=problem,
        approach="comprehensive"
    )

    print("\n--- Result ---")
    if result.get("success"):
        print(f"✓ Comprehensive solution generated!")
        print(f"\nExecution Summary:")

        for i, stage in enumerate(result.get("stages", []), 1):
            stage_name = stage.get("stage", "unknown")
            status = "✓" if "error" not in stage else "✗"
            print(f"  {i}. [{status}] {stage_name}")

        print(f"\nValidation: {result.get('validation', {})}")

        # Show final solution
        solution = result.get("solution", "")
        if solution and len(solution) > 300:
            print(f"\nSolution Preview (first 300 chars):")
            print(solution[:300] + "...")
    else:
        print(f"✗ Failed: {result.get('error')}")


async def main():
    """Run all demos"""
    print("\n" + "="*80)
    print("CogOS Super-Intelligence Demo")
    print("Demonstrating capabilities far beyond single-pass LLMs")
    print("="*80)

    demos = [
        ("Multi-Agent Collaboration", demo_multi_agent_collaboration),
        ("Hierarchical Planning", demo_hierarchical_planning),
        ("Research-Backed Solving", demo_research_backed_solving),
        ("Collaborative Writing", demo_collaborative_writing),
        ("Self-Reflection", demo_self_reflection),
        ("Comprehensive Approach", demo_comprehensive_approach),
    ]

    print("\nAvailable Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")

    print("\nRunning all demos...")

    for name, demo_func in demos:
        try:
            await demo_func()
            await asyncio.sleep(1)  # Brief pause between demos
        except Exception as e:
            print(f"\n✗ Demo '{name}' failed: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*80)
    print("Demo Complete!")
    print("="*80)
    print("\nKey Takeaways:")
    print("  1. Multi-agent collaboration produces better solutions than single LLMs")
    print("  2. Hierarchical planning breaks down complex problems effectively")
    print("  3. Research-backed solving ensures informed decisions")
    print("  4. Collaborative writing creates higher-quality documents")
    print("  5. Self-reflection enables continuous improvement")
    print("  6. Comprehensive approach combines all strengths")
    print("\nThis is what makes CogOS superior to Claude and other single-pass systems!")
    print("\nTo use CogOS in your projects:")
    print("  from cog.cogos import create_cogos")
    print("  cogos = create_cogos(llm, memory, cache)")
    print("  result = await cogos.solve_complex_problem(your_problem)")
    print()


if __name__ == "__main__":
    asyncio.run(main())
