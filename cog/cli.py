#!/usr/bin/env python3
"""
CogOS CLI - Complete with Phase 1 & 2 Features
All commands for AI-focused development
"""

import click
import json
import os
from pathlib import Path
from typing import Dict, Any

# Import CogOS systems
import sys
sys.path.insert(0, str(Path(__file__).parent))

from cog.codebase_intelligence.intel import get_codebase_intelligence
from cog.autonomous_fixer.fixer import get_autonomous_fixer
from cog.test_generator.generator import get_test_generator
from cog.predictive_analytics.analytics import get_predictive_analytics
from cog.smart_refactor.refactor import get_smart_refactor
from cog.living_docs.docs import get_living_documentation

@click.group()
@click.version_option(version="1.2.0")
def cli():
    """CogOS v1.2 - Cognitive Operating System with AI Superpowers"""
    pass

# ========== PHASE 1 & 2 COMMANDS ==========

@cli.command()
@click.argument("question")
@click.option("--depth", "-d", type=int, default=3, help="Detail level (1-5)")
def explain(question, depth):
    """Get CogOS explanations about codebase"""
    
    click.echo(f"🧠 Analyzing: {question}\n")
    
    # Use codebase intelligence
    intel = get_codebase_intelligence()
    
    if "structure" in question.lower() or "architecture" in question.lower():
        analysis = intel.analyze_structure()
        click.echo(intel.get_code_summary())
    
    elif "dependencies" in question.lower():
        graph = intel.generate_dependency_graph()
        click.echo("📊 Dependency Graph:\n")
        for file, deps in graph.items():
            if deps:
                click.echo(f"  {file} →")
                for dep in deps:
                    click.echo(f"    • {dep}")
    
    elif "patterns" in question.lower():
        analysis = intel.analyze_structure()
        patterns = analysis.get("patterns", [])
        click.echo("🔍 Architectural Patterns:\n")
        for pattern in patterns:
            click.echo(f"  • {pattern['name']}: {pattern['description']}")
    
    else:
        click.echo(intel.get_code_summary())

@cli.command()
@click.argument("file_path")
def trace(file_path):
    """Trace data flow through the system"""
    
    click.echo(f"🔍 Tracing data flow: {file_path}\n")
    
    intel = get_codebase_intelligence()
    flow = intel.trace_data_flow(file_path)
    
    click.echo("Data Flow Trace:\n")
    for step in flow:
        click.echo(f"  [{step['depth']}] {step['file']}")
        if step.get("dependencies"):
            for dep in step["dependencies"][:3]:
                click.echo(f"    → {dep}")
        click.echo("")

@cli.command()
@click.argument("pattern")
def impact(pattern):
    """Show impact of changing code"""
    
    click.echo(f"💥 Impact Analysis: {pattern}\n")
    
    intel = get_codebase_intelligence()
    related = intel.find_related_code(pattern)
    
    if related:
        click.echo("📊 Related Code:\n")
        click.echo(f"  Imports: {', '.join(related.get('imports', []))}\n")
        
        if related.get("imported_by"):
            click.echo(f"  Imported by: {len(related['imported_by'])} files")
            for file in related['imported_by'][:5]:
                click.echo(f"    • {file}")
    else:
        click.echo("No related code found")

@cli.command()
@click.option("--all", is_flag=True, help="Fix all bugs")
@click.option("--auto", is_flag=True, help="Auto-deploy fixes")
def fix(all, auto):
    """Detect and fix bugs automatically"""
    
    click.echo("🤖 Autonomous Bug Fixing\n")
    
    fixer = get_autonomous_fixer()
    
    if all:
        click.echo("🔍 Scanning for bugs...")
        results = fixer.fix_all(auto_deploy=auto)
        
        click.echo(f"\n📊 Results:")
        click.echo(f"  Bugs found: {results['bugs_found']}")
        click.echo(f"  Bugs fixed: {results['bugs_fixed']}")
        click.echo(f"  Fixes failed: {results['bugs_failed']}")
        click.echo(f"  Tests generated: {results['tests_generated']}")
    else:
        # Detect bugs
        bugs = fixer.detect_bugs()
        click.echo(f"Found {len(bugs)} bugs\n")
        
        # Show high severity bugs
        high_severity = [b for b in bugs if b.get('severity') == 'high']
        for bug in high_severity[:5]:
            click.echo(f"  🔴 {bug['type']}: {bug['description']}")
            click.echo(f"     {bug['file']}:{bug['line']}")
            click.echo(f"     Fix: {bug['suggestion']}\n")

@cli.command()
@click.option("--coverage-target", type=int, default=90, help="Target coverage percentage")
@click.option("--file", "-f", help="Generate tests for specific file")
def test_gen(coverage_target, file):
    """Generate intelligent tests"""
    
    click.echo("🧪 Intelligent Test Generation\n")
    
    generator = get_test_generator()
    
    if file:
        click.echo(f"Generating tests for: {file}\n")
        
        file_path = Path(file)
        test_content = generator.generate_unit_tests(file_path)
        
        click.echo(test_content)
    else:
        click.echo(f"Generating tests to reach {coverage_target}% coverage...\n")
        
        results = generator.generate_tests_for_coverage(coverage_target)
        
        click.echo(f"\n📊 Results:")
        click.echo(f"  Current coverage: {results['current_coverage']:.1f}%")
        click.echo(f"  Target coverage: {results['target_coverage']}%")
        click.echo(f"  Tests generated: {results['tests_generated']}")

@cli.command()
@click.option("--timeframe", default="2 weeks", help="Prediction timeframe")
@click.option("--scenario", type=click.Choice(["double_traffic", "10x_users"]), help="Scalability scenario")
def predict(timeframe, scenario):
    """Predict bugs and performance issues"""
    
    click.echo("🔮 Predictive Analytics\n")
    
    analytics = get_predictive_analytics()
    
    # Bug predictions
    click.echo("🐛 Bug Predictions:")
    bug_preds = analytics.predict_bugs(timeframe)
    
    if bug_preds:
        for pred in bug_preds[:5]:
            severity_icon = {"high": "🔴", "medium": "⚠️", "low": "💡"}[pred.get('severity', 'low')]
            click.echo(f"  {severity_icon} [{pred['confidence']:.0%}] {pred['prediction']}")
            click.echo(f"     {pred.get('suggestion', '')}")
    else:
        click.echo("  No bugs predicted ✅")
    
    click.echo()
    
    # Performance predictions
    click.echo("⚡ Performance Predictions:")
    perf_preds = analytics.predict_performance(timeframe)
    
    if perf_preds:
        for pred in perf_preds[:5]:
            severity_icon = {"high": "🔴", "medium": "⚠️", "low": "💡"}[pred.get('severity', 'low')]
            click.echo(f"  {severity_icon} [{pred['confidence']:.0%}] {pred['prediction']}")
            click.echo(f"     {pred.get('suggestion', '')}")
    else:
        click.echo("  No performance issues predicted ✅")
    
    click.echo()
    
    # Scalability prediction
    if scenario:
        click.echo(f"📈 Scalability Prediction: {scenario}")
        scale_pred = analytics.predict_scalability(scenario)
        
        click.echo(f"  Confidence: {scale_pred['confidence']:.0%}\n")
        
        for pred in scale_pred.get('predictions', []):
            click.echo(f"  {pred['severity'].upper()}: {pred['issue']}")
            click.echo(f"  Reason: {pred['reason']}")
            click.echo()
        
        click.echo("💡 Recommendations:")
        for rec in scale_pred.get('recommendations', []):
            click.echo(f"  • {rec}")

@cli.command()
@click.argument("target", type=click.Choice(["modernize", "debt"]))
@click.option("--dry-run", "-n", is_flag=True, help="Show plan without executing")
def refactor(target, dry_run):
    """Smart refactoring with guaranteed correctness"""
    
    click.echo(f"🔀 Smart Refactoring: {target}\n")
    
    refactor = get_smart_refactor()
    
    # Analyze opportunities
    opportunities = refactor.analyze_refactoring_opportunity()
    
    click.echo(f"Found {len(opportunities)} refactoring opportunities:\n")
    
    for opp in opportunities[:10]:
        severity_icon = {"high": "🔴", "medium": "⚠️", "low": "💡"}[opp.get('severity', 'low')]
        click.echo(f"  {severity_icon} {opp['type']}: {opp['description']}")
        click.echo(f"     {opp.get('file', 'N/A')}")
        click.echo(f"     {opp['suggestion']}\n")
    
    if dry_run:
        click.echo("(Dry run - no changes made)")
    else:
        # Execute refactoring
        results = refactor.refactor_codebase(target)
        
        if results.get("success"):
            click.echo(f"\n✅ Refactoring complete!")
            click.echo(f"Changes made: {results.get('files_updated', 0)}")
        else:
            click.echo(f"\n❌ Refactoring failed: {results.get('error', 'Unknown error')}")

@cli.command()
@click.option("--output", "-o", help="Output directory")
def docs(output):
    """Generate living documentation"""
    
    click.echo("📝 Living Documentation Generation\n")
    
    docs = get_living_documentation()
    
    # Generate all documentation
    click.echo("Generating API documentation...")
    api_file = docs.generate_api_docs(output)
    click.echo(f"  ✓ {api_file}")
    
    click.echo("\nGenerating architecture diagrams...")
    arch_file = docs.generate_architecture_diagrams()
    click.echo(f"  ✓ {arch_file}")
    
    click.echo("\nGenerating runbooks...")
    runbook_file = docs.generate_runbooks()
    click.echo(f"  ✓ {runbook_file}")
    
    click.echo("\nGenerating onboarding guide...")
    onboarding_file = docs.generate_onboarding()
    click.echo(f"  ✓ {onboarding_file}")
    
    click.echo("\n✅ Documentation complete!")
    click.echo(docs.get_docs_summary())

# ========== KEEP EXISTING COMMANDS ==========

@cli.command()
@click.argument("project_name")
@click.option("--profile", "-p", type=click.Choice(["web-fullstack", "data-science", "devops", "mobile", "minimal"]), default="minimal")
def init(project_name, profile):
    """Initialize a new CogOS project"""
    click.echo(f"🚀 Initializing CogOS project: {project_name}")
    
    project_path = Path(project_name)
    if project_path.exists():
        click.echo(f"❌ Directory {project_name} already exists")
        return
    
    project_path.mkdir()
    
    # Create .cogos directory
    cogos_dir = project_path / ".cogos"
    cogos_dir.mkdir()
    
    # Configuration
    config = {
        "project": {"name": project_name, "profile": profile},
        "modules": [],
        "settings": {"cache_enabled": True, "auto_improve": True}
    }
    
    import json
    (cogos_dir / "config.json").write_text(json.dumps(config, indent=2))
    
    click.echo("✅ Project initialized!")

@cli.command()
@click.argument("task")
@click.option("--dry-run", "-n", is_flag=True)
def run(task, dry_run):
    """Run a task with CogOS"""
    click.echo(f"🧠 Running task: {task}")
    
    if dry_run:
        click.echo("🔍 Dry run mode - showing plan")
    else:
        click.echo("⚙️ Executing task...")
        click.echo("✅ Task complete")

@cli.command()
def version():
    """Show CogOS version"""
    click.echo("CogOS v1.2.0")
    click.echo("🧠 Cognitive + ⚙️ Mechanical + 🔮 Predictive = Super-Intelligent")

if __name__ == "__main__":
    cli()
