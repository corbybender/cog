# CogOS Setup & Usage Guide

## Quick Start (5 minutes)

### 1. Install CogOS
```bash
# Navigate to the cog directory
cd cog

# Install the package
pip install -e .

# Verify installation
cog --help
```

### 2. Configure CogOS
```bash
# Create config file (if it doesn't exist)
cog init --output cog.yaml

# Edit the config file with your API details
nano cog.yaml
```

**Minimum `cog.yaml` configuration:**
```yaml
provider: openai
model: gpt-4o  # or your preferred model
base_url: https://api.openai.com/v1  # or custom endpoint
api_key: your-api-key-here
memory_backend: sqlite
modules_path: modules
memory_path: cog_memory.db
max_agent_iterations: 20
```

### 3. Verify Installation
```bash
# Check system status
cog status

# Should show:
# - 8 modules active
# - 33 tools available
# - 7 verifiers ready
```

---

## Basic Usage

### Simple Task Execution
```bash
# Read a file
cog run "Read the file cog/tools/filesystem.py and summarize it"

# List files
cog run "List all Python files in the current directory"

# Run tests
cog run "Run the test suite and report any failures"
```

### Interactive Chat Mode
```bash
# Start interactive chat
cog chat

# Example conversation:
you> What files are in the current directory?
cog> [Lists files with descriptions]

you> Read the agent.py file and tell me what it does
cog> [Analyzes and explains the code]
```

### Memory Management
```bash
# Search memory for past tasks
cog memory search "code improvements"

# Add memory manually
cog memory add --content "Remember: FileSearchTool needs path validation" --tags "bug,fix"

# List all memories
cog memory list
```

---

## Advanced Usage

### Module Management
```bash
# List available modules
cog modules

# Search for specific modules
cog search "rust"

# Install a module from registry
cog install cog-code-rust

# Publish your own module
cog publish ./my-custom-module
```

### Running with Options
```bash
# Dry run (preview without executing)
cog run "Fix all Python files" --dry-run

# JSON output for automation
cog run "Analyze codebase" --json

# Disable streaming
cog run "Long task" --no-stream

# Specify working directory
cog run "Test this project" --path /path/to/project
```

### Verification
```bash
# Verify Python syntax
cog verify python.syntax cog/agent.py

# Verify file exists
cog verify file.exists cog.yaml

# Run test verifier
cog verify test.runner "pytest tests/"
```

---

## Module-Specific Examples

### Python Development
```bash
# Lint Python code
cog run "Run ruff on all Python files in cog/"

# Run tests
cog run "Execute pytest with verbose output"

# Fix Python issues
cog run "Analyze Python code and fix common issues"
```

### Rust Development
```bash
# Build Rust project
cog run "Run cargo build in release mode"

# Run Rust tests
cog run "Execute cargo test with detailed output"

# Lint Rust code
cog run "Run clippy and fix warnings"
```

### Git Operations
```bash
# Check git status
cog run "Show git status and recent commits"

# Create branch
cog run "Create a new branch called feature/new-module"

# Analyze changes
cog run "Show git diff and summarize changes"
```

### Database Operations
```bash
# Query PostgreSQL
cog run "Connect to PostgreSQL and list all tables"

# Backup database
cog run "Dump PostgreSQL database to backup.sql"

# Analyze schema
cog run "Show the schema of the users table"
```

### Cloud Operations
```bash
# List S3 buckets
cog run "List all S3 buckets in my AWS account"

# Upload to S3
cog run "Upload file.txt to S3 bucket my-bucket"

# Start EC2 instance
cog run "Start EC2 instance i-1234567890"
```

---

## Configuration Options

### Basic Config
```yaml
# Provider settings
provider: openai  # or anthropic
model: gpt-4o
base_url: https://api.openai.com/v1
api_key: your-key

# Memory settings
memory_backend: sqlite  # or mem0
memory_path: cog_memory.db

# Module settings
modules_path: modules

# Agent limits
max_agent_iterations: 20
```

### Advanced Config
```yaml
# Memory backend options
memory_backend: mem0  # Requires mem0ai installed
mem0_config:
  api_key: mem0-api-key

# Permission system
require_approval: true

# Sandbox mode
sandbox_enabled: true
dry_run: false

# Performance tuning
max_total_tokens: 100000
log_level: DEBUG
```

---

## Troubleshooting

### Common Issues

**1. Module not discovered**
```bash
# Check module directory
ls modules/

# Verify manifest.json exists
cat modules/my-module/manifest.json

# Check module loading
cog modules
```

**2. API connection failed**
```bash
# Verify config
cat cog.yaml

# Test API key
cog run "Say hello"

# Check base_url matches your provider
```

**3. Tests failing**
```bash
# Run specific test
pytest tests/test_agent.py::TestAgent::test_agent_simple_task -v

# Clear cache
rm -rf .pytest_cache __pycache__

# Reinstall
pip install -e . --force-reinstall
```

**4. Memory issues**
```bash
# Check memory database
ls -la cog_memory.db

# Search memory
cog memory search "test"

# Clear memory (delete database)
rm cog_memory.db
```

---

## Performance Tips

### Speed Up Execution
```yaml
# Enable caching in cog.yaml
cache_enabled: true

# Reduce iterations for simple tasks
max_agent_iterations: 10

# Use faster model
model: gpt-4o-mini
```

### Reduce Costs
```yaml
# Limit total tokens
max_total_tokens: 50000

# Use cheaper model for analysis
model: gpt-4o-mini

# Enable dry-run for testing
dry_run: true
```

### Improve Accuracy
```yaml
# Allow more iterations
max_agent_iterations: 30

# Use best model
model: gpt-4o

# Disable streaming for better responses
stream: false
```

---

## Safety Features

### Permission System
```bash
# Interactive approval (default)
cog run "Delete all .pyc files"

# Auto-approve safe operations
cog run "List Python files"  # File reads are auto-approved

# High-risk operations require approval
cog run "Drop database table"  # Will prompt for approval
```

### Sandbox Mode
```yaml
# Enable in cog.yaml
sandbox_enabled: true
use_docker: true
network_isolated: true
```

### Dry Run
```bash
# Preview changes without executing
cog run "Refactor all Python files" --dry-run

# Safe way to test dangerous operations
cog run "Delete all test files" --dry-run
```

---

## Development Workflow

### 1. Development Mode
```bash
# Start with dry-run
cog run "Make code improvements" --dry-run

# Review the plan
# If satisfied, run without dry-run
cog run "Make code improvements"
```

### 2. Testing Mode
```bash
# Run tests after changes
cog run "Run pytest and fix any failures"

# Verify syntax
cog verify python.syntax cog/agent.py

# Check git status
cog run "Show git diff"
```

### 3. Deployment Mode
```bash
# Final verification
cog run "Run full test suite and generate report"

# Create commit
cog run "Create git commit with descriptive message"

# Push changes
cog run "Push commits to remote repository"
```

---

## Real-World Examples

### Code Refactoring
```bash
# Step 1: Analyze
cog run "Analyze cog/tools/ directory for code quality issues"

# Step 2: Plan
cog run "Create a plan to refactor the filesystem tools"

# Step 3: Execute
cog run "Implement the refactoring plan"

# Step 4: Verify
cog run "Run tests and verify everything still works"
```

### Database Migration
```bash
# Backup first
cog run "Dump PostgreSQL database to backup.sql"

# Analyze schema
cog run "Show current database schema"

# Create migration
cog run "Create SQL migration file to add user_preferences table"

# Test migration
cog run "Execute migration on test database"

# Apply to production
cog run "Execute migration on production database"
```

### Cloud Deployment
```bash
# Build application
cog run "Build Rust application in release mode"

# Upload to S3
cog run "Upload binary to S3 bucket my-app-bucket"

# Deploy to EC2
cog run "Deploy application to EC2 instances"

# Verify deployment
cog run "Check application health on all instances"
```

---

## Tips & Tricks

### 1. Use Specific Tasks
```bash
# Good
cog run "Read cog/agent.py and explain the main loop"

# Bad
cog run "Analyze the codebase"  # Too vague
```

### 2. Chain Operations
```bash
# First analyze
cog run "Find all Python files with TODO comments"

# Then fix
cog run "Read the files from previous task and implement the TODOs"
```

### 3. Use Memory Effectively
```bash
# Store important context
cog memory add --content "This project uses Python 3.14+ and requires pytest" --tags "project,requirements"

# Reference later
cog run "Check if the codebase meets the requirements I stored earlier"
```

### 4. Leverage Modules
```bash
# Use Rust expertise
cog run "Review this Rust code for ownership issues"

# Use database expertise
cog run "Optimize this SQL query for better performance"

# Use cloud expertise
cog run "Set up S3 lifecycle policies for cost optimization"
```

---

## Next Steps

1. **Start Simple**: Use basic commands first
2. **Explore Modules**: Try different specialist modules
3. **Build Custom Modules**: Create your own domain-specific tools
4. **Integrate into Workflow**: Use in daily development
5. **Scale Up**: Tackle more complex automation tasks

---

## Getting Help

```bash
# General help
cog --help

# Command-specific help
cog run --help
cog chat --help
cog memory --help

# Check system status
cog status

# View logs
tail -f cog.log  # If logging is enabled
```

---

**You're now ready to use CogOS! Start with simple tasks and gradually explore more advanced features.**
