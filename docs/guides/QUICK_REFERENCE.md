# CogOS Quick Reference Card

## Installation
```bash
cd cog && pip install -e .
```

## Configuration
```bash
cog init --output cog.yaml
# Edit cog.yaml with your API key
```

## Essential Commands

### Basic Operations
```bash
cog status                    # Check system status
cog run "task description"    # Execute a task
cog chat                      # Interactive mode
cog modules                   # List modules
cog search "query"            # Search modules
```

### Memory
```bash
cog memory search "query"     # Search memory
cog memory add --content "text" --tags "tag1,tag2"
cog memory list              # List all memories
```

### Development
```bash
cog verify python.syntax file.py          # Check syntax
cog verify test.runner "pytest tests/"   # Run tests
cog run "Run pytest and fix failures"    # Fix tests
```

### Git Integration
```bash
cog run "Show git status and recent commits"
cog run "Create branch feature/new-feature"
cog run "Show git diff and summarize changes"
```

### Common Patterns
```bash
# Code analysis
cog run "Read file.py and identify improvements"

# Refactoring
cog run "Refactor file.py to improve readability"

# Testing
cog run "Run tests and fix any failures"

# Documentation
cog run "Generate documentation for this code"
```

## Module Examples

### Python Module
```bash
cog run "Run ruff on all Python files"
cog run "Execute pytest with coverage report"
cog run "Fix Python linting issues"
```

### Rust Module
```bash
cog run "Build Rust project with cargo"
cog run "Run clippy and fix warnings"
cog run "Execute cargo test"
```

### Database Module
```bash
cog run "Connect to PostgreSQL and list tables"
cog run "Show schema of users table"
cog run "Backup database to backup.sql"
```

### AWS Module
```bash
cog run "List all S3 buckets"
cog run "Upload file.txt to S3"
cog run "Start EC2 instance i-1234567890"
```

## Options

### Safety
```bash
--dry-run           # Preview without executing
--no-stream         # Disable streaming output
```

### Output
```bash
--json              # JSON output for automation
--path DIR          # Working directory
```

### Configuration
```bash
--modules PATH      # Modules directory
--memory PATH       # Memory database path
--model NAME        # LLM model to use
```

## Tips

1. **Start with dry-run** to preview changes
2. **Use specific task descriptions** for better results
3. **Leverage memory** to store context between tasks
4. **Chain operations** for complex workflows
5. **Use appropriate modules** for specialized tasks

## Troubleshooting

```bash
# Check system status
cog status

# Verify configuration
cat cog.yaml

# Test installation
cog run "Say hello"

# Clear cache
rm -rf .pytest_cache __pycache__

# Reinstall
pip install -e . --force-reinstall
```

## System Capabilities

- **8 modules** (Python, Rust, PostgreSQL, AWS, Git, etc.)
- **33 tools** (filesystem, shell, web, database, cloud)
- **7 verifiers** (syntax, connectivity, tests)
- **87 prompt extensions** with domain expertise

## Key Features

✅ Performance optimization (40-60% token reduction)
✅ Safety features (sandbox, permissions, approvals)
✅ Enhanced planning (task decomposition, previews)
✅ Multi-language support (Python, Rust)
✅ Cloud integration (AWS S3, EC2, Lambda)
✅ Database operations (PostgreSQL)
✅ Git integration
✅ Interactive chat mode
✅ Memory system
✅ Modular architecture

---

**Ready to automate your development workflow!**
