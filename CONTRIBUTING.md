# Contributing to CogOS

First off, thank you for considering contributing to CogOS! It's people like you that make CogOS such a great tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Adding Modules](#adding-modules)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

---

## Code of Conduct

Please be respectful and constructive in all interactions. We're all here to build something great together.

---

## How Can I Contribute?

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Include:
   - Clear title and description
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details
   - Screenshots if applicable

### Suggesting Enhancements

1. Check existing feature requests
2. Use the feature request template
3. Explain the use case
4. Provide examples if possible

### Contributing Code

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

---

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- Git
- Virtual environment (recommended)

### Setup Steps

```bash
# 1. Fork and clone the repository
git clone https://github.com/your-username/cog.git
cd cog

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install development dependencies
pip install -e ".[dev]"

# 4. Install pre-commit hooks
pre-commit install

# 5. Run tests
pytest

# 6. Start hacking!
```

### Project Structure

```
cog/
├── cog/                    # Main package
│   ├── modules/           # Expert modules
│   ├── agents/            # Multi-agent system
│   ├── cache/             # Caching system
│   └── safety/            # Safety & security
├── tests/                 # Test suite
├── docs/                  # Documentation
├── examples/              # Example code
└── scripts/               # Utility scripts
```

---

## Pull Request Process

### Before Submitting

1. **Update Documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update API documentation

2. **Add Tests**
   - Write unit tests for new features
   - Ensure all tests pass: `pytest`
   - Check coverage: `pytest --cov=cog`

3. **Code Quality**
   - Run linter: `ruff check`
   - Run formatter: `ruff format`
   - Fix any issues

4. **Commit Messages**
   - Use clear, descriptive messages
   - Follow commit message conventions
   - Reference issues if applicable

### Submitting PR

1. Push to your fork
2. Create pull request from your branch to `main`
3. Fill out the PR template
4. Wait for review
5. Address feedback
6. Get merged! 🎉

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated

## Related Issues
Fixes #123
```

---

## Coding Standards

### Python Style Guide

Follow PEP 8 and use these conventions:

```python
# Good
def process_data(data: List[Dict]) -> Dict:
    """Process data and return results."""
    results = {}
    for item in data:
        results[item['id']] = item
    return results

# Bad
def processData(d):
    r={}
    for i in d:
        r[i['id']]=i
    return r
```

### Type Hints

Always use type hints:

```python
from typing import List, Dict, Optional

def fetch_data(url: str, timeout: int = 30) -> Optional[Dict]:
    """Fetch data from URL."""
    ...
```

### Docstrings

Use Google style docstrings:

```python
def create_module(name: str, tools: List[Tool]) -> Module:
    """Create a new CogOS module.

    Args:
        name: The module name
        tools: List of tools to include

    Returns:
        The created module

    Raises:
        ValueError: If module name is invalid
    """
    ...
```

### Error Handling

```python
# Good
try:
    result = process_data(data)
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

# Bad
try:
    result = process_data(data)
except:
    pass
```

### Testing

```python
def test_process_data():
    """Test data processing."""
    data = [{"id": 1, "name": "Test"}]
    result = process_data(data)
    assert result == {1: {"id": 1, "name": "Test"}}
```

---

## Commit Messages

Follow Conventional Commits:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Good
feat(multi-agent): add debate voting mechanism
fix(caching): resolve cache key collision issue
docs(api): update Python API reference

# Bad
added stuff
fixed bug
update docs
```

---

## Adding Modules

### Module Structure

```
cog/modules/my-module/
├── manifest.json       # Module metadata
├── module.py          # Module implementation
├── tools/             # Tool definitions
│   ├── tool1.json
│   └── tool2.json
└── README.md          # Module documentation
```

### Module Manifest

```json
{
  "name": "my-module",
  "description": "My custom module",
  "version": "1.0.0",
  "categories": ["web", "framework"],
  "tools": [
    {
      "name": "create-component",
      "description": "Create a component",
      "prompt": "Create a {type} component"
    }
  ]
}
```

### Module Checklist

- [ ] Follow module structure
- [ ] Include manifest.json
- [ ] Add module implementation
- [ ] Include at least 5 tools
- [ ] Add comprehensive tests
- [ ] Write documentation
- [ ] Update module list
- [ ] Run integration tests

---

## Reporting Bugs

### Bug Report Template

```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.9.0]
- CogOS: [e.g., 1.0.0]
- LLM: [e.g., Claude 3.5 Sonnet]

## Logs
Error messages or logs

## Additional Context
Screenshots, code examples, etc.
```

---

## Suggesting Enhancements

### Feature Request Template

```markdown
## Description
Feature description

## Problem Statement
What problem does this solve?

## Proposed Solution
How should it work?

## Alternatives
What other approaches did you consider?

## Additional Context
Examples, mockups, etc.
```

---

## Development Workflow

### 1. Choose an Issue

```bash
# List open issues
gh issue list

# Start working on an issue
gh issue checkout 123
```

### 2. Create Branch

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or fix branch
git checkout -b fix/your-bug-fix
```

### 3. Make Changes

```bash
# Make your changes
vim cog/module.py

# Run tests
pytest

# Run linter
ruff check
ruff format

# Check coverage
pytest --cov=cog
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with conventional message
git commit -m "feat(module): add new feature"
```

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request
gh pr create --title "Add new feature" --body "Description of changes"
```

---

## Code Review Process

### As a Reviewer

1. **Be Constructive**
   - Provide specific feedback
   - Suggest improvements
   - Acknowledge good work

2. **Checklist**
   - [ ] Code follows standards
   - [ ] Tests are comprehensive
   - [ ] Documentation is updated
   - [ ] No breaking changes (or documented)
   - [ ] Performance impact considered

### As an Author

1. **Respond to Feedback**
   - Address all comments
   - Explain your decisions
   - Update as needed

2. **Revise and Resubmit**
   - Make requested changes
   - Re-run tests
   - Update PR description

---

## Getting Help

### Resources

- [Documentation](../docs/)
- [GitHub Issues](https://github.com/corbybender/cog/issues)
- [Discussions](https://github.com/corbybender/cog/discussions)

### Asking Questions

1. Check existing issues and docs
2. Create a discussion for questions
3. Be specific and provide context
4. Share error messages and logs

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Celebrated in our community! 🎉

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to CogOS! 🙏**

*Together we're building the future of AI-assisted development*
