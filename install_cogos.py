#!/usr/bin/env python3
"""
CogOS Installer: One-command installation for any project

Run this in ANY project directory to install CogOS:
    curl -sSL https://raw.githubusercontent.com/your-repo/cogos/main/install.py | python3

Or download and run:
    python install_cogos.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def install_cagos():
    """Install CogOS into current project"""

    print("🚀 CogOS Installer")
    print("="*80)
    print()

    # Get current directory (project root)
    project_root = Path.cwd()
    print(f"📁 Project directory: {project_root}")
    print()

    # Create CogOS directory structure
    print("📦 Installing CogOS...")

    # 1. Create .cogos directory
    cogos_dir = project_root / ".cogos"
    cogos_dir.mkdir(exist_ok=True)
    print(f"   ✓ Created .cogos/ directory")

    # 2. Create config file
    config = """
# CogOS Configuration
# This file tells AI agents that CogOS is available in this project

version: "2.0"
auto_detect: true
auto_integrate: true

# AI agents will automatically use CogOS for:
# - Complex problem solving
# - System design
# - Code architecture
# - Documentation
# - Research and analysis

# To disable: set auto_integrate: false
"""

    (cogos_dir / "config.yaml").write_text(config)
    print(f"   ✓ Created .cogos/config.yaml")

    # 3. Create usage guide for AI agents
    usage_guide = """# CogOS Usage Guide for AI Agents

## What is CogOS?

CogOS is a super-intelligent cognitive operating system that provides:
- Multi-agent collaboration (8 specialized agents)
- Hierarchical task planning
- Self-reflection and learning
- Research capabilities
- Document generation
- Code analysis and optimization

## When to Use CogOS

AI agents should use CogOS for:
- Complex system design
- Multi-step implementation tasks
- Architecture decisions
- Code refactoring
- Performance optimization
- Security analysis
- Documentation generation
- Research and analysis

## How to Use CogOS

### For Code Analysis:
```python
from cogos import analyze_codebase
result = analyze_codebase(path=".")
```

### For System Design:
```python
from cogos import design_system
result = design_system(requirements="...")
```

### For Documentation:
```python
from cogos import generate_docs
result = generate_docs(path=".")
```

### For Problem Solving:
```python
from cogos import solve
result = solve(problem="...")
```

## Integration

CogOS automatically integrates with the project's AI workflow.
"""

    (cogos_dir / "USAGE.md").write_text(usage_guide)
    print(f"   ✓ Created .cogos/USAGE.md")

    # 4. Create Python API wrapper
    api_wrapper = '''"""
CogOS Python API

Import this to use CogOS in your project:
    from cogos import solve, analyze, design, document
"""

import asyncio
import sys
from pathlib import Path

# Add CogOS to path
cogos_path = Path(__file__).parent / "cogos"
if str(cogos_path) not in sys.path:
    sys.path.insert(0, str(cogos_path))

try:
    from cogos_auto import CogOSAutoIntegrator
    COGOS_AVAILABLE = True
except ImportError:
    COGOS_AVAILABLE = False
    print("Warning: CogOS not installed. Run: pip install cogos")


# Singleton instance
_cogos_instance = None


def get_cogos():
    """Get or create CogOS instance"""
    global _cogos_instance
    if _cogos_instance is None:
        if COGOS_AVAILABLE:
            _cogos_instance = CogOSAutoIntegrator()
        else:
            raise RuntimeError("CogOS not available")
    return _cogos_instance


async def solve(problem: str, context: str = "") -> dict:
    """
    Solve a complex problem using CogOS multi-agent system

    Args:
        problem: Problem description
        context: Additional context

    Returns:
        Solution with confidence score
    """
    cogos = get_cogos()
    return await cogos.solve_complex_problem(problem, context=context)


async def analyze_codebase(path: str = ".", focus: str = "") -> dict:
    """
    Analyze codebase using CogOS

    Args:
        path: Path to codebase
        focus: Area to focus on

    Returns:
        Analysis results
    """
    cogos = get_cogos()

    problem = f"Analyze this codebase: {path}"
    if focus:
        problem += f"\\nFocus on: {focus}"

    return await cogos.solve_complex_problem(
        problem=problem,
        approach="collaborative"
    )


async def design_system(requirements: str) -> dict:
    """
    Design a system using CogOS multi-agent collaboration

    Args:
        requirements: System requirements

    Returns:
        System design with architecture
    """
    cogos = get_cogos()

    return await cogos.solve_complex_problem(
        problem=f"Design a system with these requirements:\\n{requirements}",
        approach="collaborative"
    )


async def generate_docs(path: str = ".", doc_type: str = "readme") -> str:
    """
    Generate documentation using CogOS

    Args:
        path: Path to document
        doc_type: Type of documentation

    Returns:
        Generated documentation
    """
    cogos = get_cogos()

    from cog.document_writer import DocumentType

    doc_types = {
        "readme": DocumentType.DOCUMENTATION,
        "api": DocumentType.API_REFERENCE,
        "guide": DocumentType.GUIDE,
        "tutorial": DocumentType.TUTORIAL
    }

    result = await cogos.write_comprehensive_document(
        title=f"{doc_type.upper()} for {path}",
        topic=f"Documentation for {path}",
        doc_type=doc_types.get(doc_type, DocumentType.DOCUMENTATION),
        collaborative=True
    )

    return result.get("markdown", "")


async def optimize_code(code: str, language: str = "") -> dict:
    """
    Optimize code using CogOS

    Args:
        code: Code to optimize
        language: Programming language

    Returns:
        Optimized code with explanations
    """
    cogos = get_cogos()

    problem = f"Optimize this {language} code:\\n{code}"

    return await cogos.solve_complex_problem(
        problem=problem,
        approach="collaborative"
    )


async def debug(issue_description: str) -> dict:
    """
    Debug an issue using CogOS research and analysis

    Args:
        issue_description: Description of the issue

    Returns:
        Analysis and solutions
    """
    cogos = get_cogos()

    return await cogos.solve_complex_problem(
        problem=f"Debug this issue:\\n{issue_description}",
        approach="researched"
    )


# Convenience function for direct use
async def ask_cogos(question: str) -> str:
    """
    Ask CogOS a question and get a response

    This is the simplest way to use CogOS:
        result = await ask_cogos("Design a REST API")
        print(result)

    Args:
        question: Your question or problem

    Returns:
        Response from CogOS
    """
    cogos = get_cogos()
    result = await cogos.generate(question)

    return result


__all__ = [
    "solve",
    "analyze_codebase",
    "design_system",
    "generate_docs",
    "optimize_code",
    "debug",
    "ask_cogos"
]
'''

    (cogos_dir / "__init__.py").write_text(api_wrapper)
    print(f"   ✓ Created .cogos/__init__.py")

    # 5. Create example usage file
    example_usage = '''"""
Example: How to use CogOS in your project
"""

import asyncio
from cogos import ask_cogos, solve, design_system


async def main():
    # Simple usage
    response = await ask_cogos("Design a scalable API")
    print(response)

    # Advanced usage
    result = await solve(
        "Implement a caching layer",
        context="Using Redis, Python, Flask"
    )

    if result['success']:
        print(f"Solution: {result['solution']}")
        print(f"Confidence: {result['validation']['confidence']}")


if __name__ == "__main__":
    asyncio.run(main())
'''

    (cogos_dir / "example.py").write_text(example_usage)
    print(f"   ✓ Created .cogos/example.py")

    # 6. Create .gitignore entry
    gitignore = project_root / ".gitignore"
    existing = gitignore.read_text() if gitignore.exists() else ""

    if ".cogos/" not in existing and "cogos" not in existing:
        with open(gitignore, "a") as f:
            f.write("\n# CogOS\n.cogos/\n")
        print(f"   ✓ Updated .gitignore")

    # 7. Create or update README
    readme = project_root / "README.md"
    readme_content = f"""# Project with CogOS

This project uses [CogOS](https://github.com/your-repo/cogos) for AI-enhanced development.

## What is CogOS?

CogOS is a super-intelligent cognitive operating system that provides:
- Multi-agent collaboration
- Hierarchical task planning
- Self-reflection and learning
- Research capabilities
- Document generation

## Usage

### Quick Start
```python
from cogos import ask_cogos

response = await ask_cogos("Design a REST API")
print(response)
```

### Advanced Usage
```python
from cogos import solve, design_system, analyze_codebase

# Solve complex problems
result = await solve("Implement a caching layer")

# Design systems
architecture = await design_system(requirements)

# Analyze codebase
analysis = await analyze_codebase(path=".")
```

## Installation

CogOS is already installed in this project! See `.cogos/` directory.

## AI Integration

When AI agents (Claude, OpenCode, etc.) analyze this project, they will automatically recognize CogOS and can use it for:
- System design
- Code analysis
- Documentation
- Problem solving
"""

    if not readme.exists():
        readme.write_text(readme_content)
        print(f"   ✓ Created README.md")
    else:
        # Append to existing README
        existing_content = readme.read_text()
        if "CogOS" not in existing_content:
            with open(readme, "a") as f:
                f.write("\n\n---\n\n" + readme_content)
            print(f"   ✓ Updated README.md")

    # 8. Create requirements.txt entry
    requirements = project_root / "requirements.txt"
    if requirements.exists():
        req_content = requirements.read_text()
        if "cogos" not in req_content:
            with open(requirements, "a") as f:
                f.write("\n# CogOS\ncogos>=2.0.0\n")
            print(f"   ✓ Updated requirements.txt")
    else:
        requirements.write_text("# CogOS\ncogos>=2.0.0\n")
        print(f"   ✓ Created requirements.txt")

    # 9. Create pyproject.toml entry
    pyproject = project_root / "pyproject.toml"
    if not pyproject.exists():
        pyproject_content = """[project]
name = "my-project"
version = "0.1.0"
dependencies = [
    "cogos>=2.0.0",
]

[tool.cogos]
enabled = true
auto_detect = true
"""
        pyproject.write_text(pyproject_content)
        print(f"   ✓ Created pyproject.toml")
    else:
        print(f"   ℹ pyproject.toml exists (not modifying)")

    print()
    print("="*80)
    print("✅ CogOS installed successfully!")
    print("="*80)
    print()
    print("📁 Created files:")
    print("   .cogos/")
    print("   ├── config.yaml       (AI agent configuration)")
    print("   ├── USAGE.md          (Usage guide for AI agents)")
    print("   ├── __init__.py       (Python API)")
    print("   └── example.py        (Example usage)")
    print()
    print("📝 Updated files:")
    print("   README.md             (Added CogOS section)")
    print("   requirements.txt      (Added cogos dependency)")
    print("   .gitignore            (Added .cogos/)")
    print()
    print("🚀 Next steps:")
    print("   1. Install CogOS: pip install cogos")
    print("   2. Use in code: from cogos import ask_cogos")
    print("   3. AI agents will now automatically use CogOS!")
    print()
    print("💡 When AI agents scan your project, they will see:")
    print("   → .cogos/ directory")
    print("   → config.yaml (tells them CogOS is available)")
    print("   → USAGE.md (shows them how to use it)")
    print("   → __init__.py (Python API they can call)")
    print("   → README.md (mentions CogOS)")
    print()
    print("✨ Your project is now CogOS-enabled!")
    print()


if __name__ == "__main__":
    try:
        install_cagos()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
