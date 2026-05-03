#!/usr/bin/env python3
"""
CogOS Super-Intelligence CLI

Command-line interface for CogOS advanced capabilities.
"""

import asyncio
import sys
import click
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cog.cogos import create_cogos
from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache
from cog.document_writer import DocumentType


@click.group()
@click.version_option(version="2.0.0")
def cli():
    """CogOS Super-Intelligence CLI"""
    pass


@cli.command()
@click.argument('problem', type=str)
@click.option('--context', '-c', type=str, default='', help='Additional context')
@click.option('--approach', '-a', type=click.Choice(['auto', 'collaborative', 'planned', 'researched', 'comprehensive']),
              default='auto', help='Solution approach')
@click.option('--output', '-o', type=click.Path(), help='Save result to file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def solve(problem, context, approach, output, verbose):
    """Solve a complex problem using super-intelligence"""
    async def _solve():
        click.echo(click.style("🧠 CogOS Super-Intelligence", fg='blue', bold=True))
        click.echo(f"Problem: {problem[:100]}...")
        click.echo(f"Approach: {approach}")
        click.echo()

        # Initialize CogOS
        llm = LLMProvider()
        memory = MemoryBackend(db_path=":memory:")
        cache = SmartCache(max_size=1000, ttl_seconds=3600)
        cogos = create_cogos(llm, memory, cache, enable_all=True)

        # Solve
        with click.progressbar(length=100, label='Thinking') as bar:
            result = await cogos.solve_complex_problem(
                problem=problem,
                context=context,
                approach=approach
            )
            bar.update(100)

        # Display result
        if result.get('success'):
            click.echo(click.style("✓ Success!", fg='green', bold=True))
            click.echo()

            if verbose:
                # Show all stages
                for i, stage in enumerate(result.get('stages', []), 1):
                    stage_name = stage.get('stage', 'unknown')
                    click.echo(f"{i}. {stage_name}")

            # Show solution
            solution = result.get('solution', '')
            if solution:
                click.echo(click.style("Solution:", fg='blue', bold=True))
                click.echo(solution)

            # Show validation
            validation = result.get('validation', {})
            if validation:
                click.echo()
                click.echo(click.style("Validation:", fg='blue', bold=True))
                click.echo(f"  Valid: {validation.get('is_valid', False)}")
                click.echo(f"  Confidence: {validation.get('confidence', 0):.2f}")

                issues = validation.get('issues', [])
                if issues:
                    click.echo(f"  Issues: {len(issues)}")
                    for issue in issues:
                        click.echo(f"    - {issue}")

            # Save to file
            if output:
                with open(output, 'w') as f:
                    json.dump(result, f, indent=2)
                click.echo()
                click.echo(f"💾 Saved to {output}")

        else:
            click.echo(click.style("✗ Failed", fg='red', bold=True))
            error = result.get('error', 'Unknown error')
            click.echo(f"Error: {error}")

    asyncio.run(_solve())


@cli.command()
@click.argument('title', type=str)
@click.argument('topic', type=str)
@click.option('--type', '-t', type=click.Choice(['technical_report', 'documentation', 'tutorial', 'guide', 'design_doc']),
              default='technical_report', help='Document type')
@click.option('--context', '-c', type=str, default='', help='Additional context')
@click.option('--output', '-o', type=click.Path(), required=True, help='Output file')
@click.option('--collaborative', is_flag=True, help='Use collaborative writing (better quality, slower)')
@click.option('--target-audience', type=str, default='technical', help='Target audience')
def write(title, topic, type, context, output, collaborative, target_audience):
    """Write a comprehensive document"""
    async def _write():
        click.echo(click.style("📝 CogOS Document Writer", fg='blue', bold=True))
        click.echo(f"Title: {title}")
        click.echo(f"Topic: {topic[:100]}...")
        click.echo(f"Type: {type}")
        click.echo(f"Collaborative: {collaborative}")
        click.echo()

        # Initialize CogOS
        llm = LLMProvider()
        memory = MemoryBackend(db_path=":memory:")
        cache = SmartCache(max_size=1000, ttl_seconds=3600)
        cogos = create_cogos(llm, memory, cache, enable_all=True)

        # Map string to DocumentType
        doc_type_map = {
            'technical_report': DocumentType.TECHNICAL_REPORT,
            'documentation': DocumentType.DOCUMENTATION,
            'tutorial': DocumentType.TUTORIAL,
            'guide': DocumentType.GUIDE,
            'design_doc': DocumentType.DESIGN_DOC,
        }
        doc_type = doc_type_map.get(type, DocumentType.TECHNICAL_REPORT)

        # Write document
        with click.progressbar(length=100, label='Writing') as bar:
            result = await cogos.write_comprehensive_document(
                title=title,
                topic=topic,
                doc_type=doc_type,
                context=context,
                collaborative=collaborative
            )
            bar.update(100)

        # Display result
        if result.get('success'):
            click.echo(click.style("✓ Document written!", fg='green', bold=True))
            click.echo()

            # Show structure
            document = result.get('document', {})
            sections = document.get('sections', [])
            click.echo(f"Sections: {len(sections)}")

            for i, section in enumerate(sections[:10], 1):
                subsections = section.get('subsections', [])
                click.echo(f"  {i}. {section.get('title', 'N/A')} ({len(subsections)} subsections)")

            if len(sections) > 10:
                click.echo(f"  ... and {len(sections) - 10} more sections")

            # Save markdown
            markdown = result.get('markdown', '')
            output_path = Path(output)

            if output_path.suffix == '.json':
                # Save as JSON
                with open(output_path, 'w') as f:
                    json.dump(result, f, indent=2)
            else:
                # Save as markdown
                with open(output_path, 'w') as f:
                    f.write(markdown)

            click.echo()
            click.echo(f"💾 Saved to {output}")

        else:
            click.echo(click.style("✗ Failed", fg='red', bold=True))
            error = result.get('error', 'Unknown error')
            click.echo(f"Error: {error}")

    asyncio.run(_write())


@cli.command()
@click.argument('question', type=str)
@click.option('--sources', '-s', multiple=True,
              type=click.Choice(['memory', 'codebase', 'documentation', 'web', 'files']),
              default=['memory', 'codebase', 'web'], help='Research sources')
@click.option('--max-results', '-n', type=int, default=10, help='Maximum results')
@click.option('--output', '-o', type=click.Path(), help='Save result to file')
def research(question, sources, max_results, output):
    """Research a question from multiple sources"""
    async def _research():
        click.echo(click.style("🔍 CogOS Research Agent", fg='blue', bold=True))
        click.echo(f"Question: {question[:100]}...")
        click.echo(f"Sources: {', '.join(sources)}")
        click.echo()

        # Initialize CogOS
        llm = LLMProvider()
        memory = MemoryBackend(db_path=":memory:")
        cache = SmartCache(max_size=1000, ttl_seconds=3600)

        from cog.research import Researcher
        from cog.cogos import ResearchSource

        researcher = Researcher(llm, memory, cache)

        # Map strings to ResearchSource
        source_map = {
            'memory': ResearchSource.MEMORY,
            'codebase': ResearchSource.CODEBASE,
            'documentation': ResearchSource.DOCUMENTATION,
            'web': ResearchSource.WEB_SEARCH,
            'files': ResearchSource.FILES,
        }

        research_sources = [source_map.get(s, ResearchSource.MEMORY) for s in sources]

        # Research
        with click.progressbar(length=100, label='Researching') as bar:
            query = await researcher.research(
                question=question,
                sources=research_sources,
                max_results=max_results
            )
            bar.update(100)

        # Synthesize findings
        synthesis = await researcher.synthesize_findings(query)

        click.echo(click.style("✓ Research complete!", fg='green', bold=True))
        click.echo()

        click.echo(click.style("Findings:", fg='blue', bold=True))
        click.echo(synthesis)

        # Show top results
        click.echo()
        click.echo(click.style(f"Top Results ({min(5, len(query.results))}):", fg='blue', bold=True))

        for i, result in enumerate(query.results[:5], 1):
            click.echo(f"{i}. [{result.source.value}] {result.relevance:.2f}")
            content = result.content[:100]
            click.echo(f"   {content}...")

        # Save to file
        if output:
            with open(output, 'w') as f:
                json.dump({
                    "question": question,
                    "synthesis": synthesis,
                    "results": [
                        {
                            "source": r.source.value,
                            "content": r.content,
                            "relevance": r.relevance
                        }
                        for r in query.results
                    ]
                }, f, indent=2)
            click.echo()
            click.echo(f"💾 Saved to {output}")

    asyncio.run(_research())


@cli.command()
@click.argument('goal', type=str)
@click.option('--context', '-c', type=str, default='', help='Additional context')
@click.option('--output', '-o', type=click.Path(), help='Save plan to file')
def plan(goal, context, output):
    """Create a hierarchical execution plan"""
    async def _plan():
        click.echo(click.style("📋 CogOS Task Planner", fg='blue', bold=True))
        click.echo(f"Goal: {goal[:100]}...")
        click.echo()

        # Initialize CogOS
        llm = LLMProvider()
        memory = MemoryBackend(db_path=":memory:")
        cache = SmartCache(max_size=1000, ttl_seconds=3600)
        cogos = create_cogos(llm, memory, cache, enable_all=True)

        # Create plan
        with click.progressbar(length=100, label='Planning') as bar:
            result = await cogos.solve_complex_problem(
                problem=goal,
                context=context,
                approach='planned'
            )
            bar.update(100)

        # Display plan
        if result.get('success'):
            click.echo(click.style("✓ Plan created!", fg='green', bold=True))
            click.echo()

            # Find and display plan structure
            for stage in result.get('stages', []):
                if 'plan' in stage:
                    plan = stage['plan']
                    click.echo(click.style("Plan Structure:", fg='blue', bold=True))

                    def display_plan(task, level=0):
                        indent = "  " * level
                        status_icon = "✓" if task.get('status') == 'completed' else "○"
                        click.echo(f"{indent}{status_icon} {task.get('title', 'N/A')}")

                        for subtask in task.get('subtasks', []):
                            display_plan(subtask, level + 1)

                    display_plan(plan)

                    # Save to file
                    if output:
                        with open(output, 'w') as f:
                            json.dump(plan, f, indent=2)
                        click.echo()
                        click.echo(f"💾 Saved to {output}")

                    break
        else:
            click.echo(click.style("✗ Failed", fg='red', bold=True))
            error = result.get('error', 'Unknown error')
            click.echo(f"Error: {error}")

    asyncio.run(_plan())


@cli.command()
def capabilities():
    """Show CogOS capabilities"""
    async def _capabilities():
        click.echo(click.style("🚀 CogOS Capabilities", fg='blue', bold=True))
        click.echo()

        # Initialize CogOS
        llm = LLMProvider()
        memory = MemoryBackend(db_path=":memory:")
        cache = SmartCache(max_size=1000, ttl_seconds=3600)
        cogos = create_cogos(llm, memory, cache, enable_all=True)

        # Get capabilities
        caps = await cogos.get_capabilities_summary()

        click.echo("Super-Intelligence Features:")
        click.echo()

        features = [
            ("Multi-Agent Collaboration", caps.get('multi_agent', False)),
            ("Hierarchical Planning", caps.get('hierarchical_planning', False)),
            ("Self-Reflection", caps.get('self_reflection', False)),
            ("Continuous Improvement", caps.get('continuous_improvement', False)),
            ("Research Capabilities", caps.get('research', False)),
            ("Context Gathering", caps.get('context_gathering', False)),
            ("Document Writing", caps.get('document_writing', False)),
            ("Collaborative Writing", caps.get('collaborative_writing', False)),
        ]

        for feature, enabled in features:
            status = "✓" if enabled else "✗"
            color = "green" if enabled else "red"
            click.echo(f"  {click.style(status, fg=color)} {feature}")

        click.echo()
        click.echo(click.style("Configuration:", fg='blue', bold=True))
        click.echo(f"  Max Iterations: {caps.get('max_iterations', 0)}")
        click.echo(f"  Confidence Threshold: {caps.get('confidence_threshold', 0):.2f}")

        click.echo()
        click.echo(click.style("Why CogOS is Superior:", fg='blue', bold=True))
        click.echo()
        click.echo("  Unlike Claude and other single-pass LLMs, CogOS:")
        click.echo("    • Uses multiple specialized agents working in parallel")
        click.echo("    • Breaks down complex problems hierarchically")
        click.echo("    • Reflects on its own performance and improves")
        click.echo("    • Researches before making decisions")
        click.echo("    • Collaborates to produce better results")
        click.echo("    • Validates solutions before presenting them")
        click.echo()

    asyncio.run(_capabilities())


@cli.command()
def demo():
    """Run the super-intelligence demo"""
    import subprocess
    demo_path = Path(__file__).parent.parent / "demo_super_intelligence.py"
    subprocess.run([sys.executable, str(demo_path)])


if __name__ == '__main__':
    cli()
