# CogOS CLI Reference

Complete reference for the CogOS command-line interface.

## Installation

```bash
pip install cogos
```

## Basic Usage

```bash
# Interactive mode (default)
cogos

# Execute task directly
cogos "Create a REST API with FastAPI"

# Use specific modules
cogos --modules python,postgresql "Build a database application"

# Save output to file
cogos "Create a React component" > output.md
```

---

## Commands

### `cogos` (Interactive Mode)

Start interactive chat with CogOS.

```bash
cogos
```

**Features:**
- Multi-turn conversations
- Context preservation
- Real-time collaboration
- History tracking

**Example:**
```
$ cogos
🤖 CogOS v1.0.0 - Ready to help!

You: Create a Python function to fetch data from an API
🤖: [Generates code with tests and docs]

You: Now add Redis caching
🤖: [Adds Redis integration]
```

---

### `cogos chat`

Alias for interactive mode.

```bash
cogos chat
```

---

### `cogos think`

Execute a single task and exit.

```bash
cogos think "Build a REST API"
```

**Options:**
- `--modules, -m`: Specify modules to use
- `--output, -o`: Save output to file
- `--format, -f`: Output format (markdown, json, code)
- `--safety-level`: Set safety level
- `--no-cache`: Disable caching
- `--verbose, -v`: Verbose output

**Examples:**
```bash
# Basic task
cogos think "Create a React component"

# With specific modules
cogos think "Deploy to AWS" --modules aws,docker

# Save to file
cogos think "Build a microservice" --output result.md

# JSON output
cogos think "Create API" --format json --output result.json

# Verbose mode
cogos think "Debug this code" --verbose
```

---

### `cogos plan`

Create a hierarchical plan for complex tasks.

```bash
cogos plan "Build an e-commerce platform"
```

**Options:**
- `--output, -o`: Save plan to file
- `--format, -f`: Output format (markdown, json)
- `--modules, -m`: Specify modules

**Examples:**
```bash
# Create plan
cogos plan "Build microservices architecture"

# Save plan
cogos plan "Build SaaS platform" --output plan.md

# JSON format
cogos plan "Build API" --format json --output plan.json
```

---

### `cogos research`

Execute multi-source research.

```bash
cogos research "Docker best practices for Node.js"
```

**Options:**
- `--sources`: Specify sources (web, docs, codebase)
- `--output, -o`: Save to file
- `--format, -f`: Output format

**Examples:**
```bash
# Research with all sources
cogos research "Kubernetes deployment strategies"

# Specific sources
cogos research "React performance" --sources web,docs

# Save research
cogos research "AWS cost optimization" --output research.md
```

---

### `cogos modules`

List all available modules.

```bash
cogos modules
```

**Output:**
```
Available Modules:
==================
🌐 Web
  - css: CSS styling and animations
  - html: HTML markup and structure

⚙️ Languages
  - javascript: JavaScript and Node.js
  - python: Python development
  - java: Java enterprise development
  ...

Use --info <module> for more details
```

**Options:**
- `--info, -i`: Get detailed info about a module
- `--category`: Filter by category
- `--tools`: List tools in each module

**Examples:**
```bash
# List all modules
cogos modules

# Get module info
cogos modules --info python

# Filter by category
cogos modules --category database

# Show tools
cogos modules --tools
```

---

### `cogos install`

Install CogOS into current project (auto-integration).

```bash
cogos install
```

**Creates:**
- `.cogos/` directory
- `.cogos/config.yaml` - Configuration
- `.cogos/USAGE.md` - Usage guide
- `.cogos/__init__.py` - Integration code

**Options:**
- `--force`: Overwrite existing installation
- `--config`: Custom configuration file

**Examples:**
```bash
# Install in current directory
cd /path/to/project
cogos install

# Force reinstall
cogos install --force

# Custom config
cogos install --config custom-config.yaml
```

---

### `cogos validate`

Validate code or requirements.

```bash
cogos validate <file>
```

**Options:**
- `--requirements, -r`: Requirements file
- `--output, -o`: Save validation report
- `--format, -f`: Output format

**Examples:**
```bash
# Validate Python file
cogos validate app.py

# With requirements
cogos validate app.py --requirements requirements.txt

# Save report
cogos validate app.py --output validation.md
```

---

### `cogos optimize`

Optimize code for performance or cost.

```bash
cogos optimize <file>
```

**Options:**
- `--objective`: Optimization target (performance, cost, memory)
- `--output, -o`: Save optimized code
- `--benchmark`: Run benchmarks

**Examples:**
```bash
# Optimize for performance
cogos optimize app.py --objective performance

# Optimize for cost
cogos optimize app.py --objective cost

# Run benchmarks
cogos optimize app.py --benchmark
```

---

### `cogos test`

Generate tests for code.

```bash
cogos test <file>
```

**Options:**
- `--framework`: Test framework (pytest, jest, etc.)
- `--coverage`: Generate coverage report
- `--output, -o`: Save tests

**Examples:**
```bash
# Generate tests
cogos test app.py

# Specific framework
cogos test app.py --framework pytest

# With coverage
cogos test app.py --coverage
```

---

### `cogos document`

Generate documentation for code.

```bash
cogos document <file>
```

**Options:**
- `--format, -f`: Documentation format (markdown, html, docstring)
- `--output, -o`: Save documentation
- `--examples`: Include usage examples

**Examples:**
```bash
# Generate docs
cogos document app.py

# Markdown format
cogos document app.py --format markdown --output README.md

# With examples
cogos document app.py --examples
```

---

### `cogos cache`

Manage CogOS cache.

```bash
cogos cache <command>
```

**Commands:**
- `stats`: Show cache statistics
- `clear`: Clear cache
- `inspect`: Inspect cache entries

**Examples:**
```bash
# Show stats
cogos cache stats

# Clear cache
cogos cache clear

# Inspect cache
cogos cache inspect
```

---

### `cogos config`

Manage CogOS configuration.

```bash
cogos config <command>
```

**Commands:**
- `get`: Get configuration value
- `set`: Set configuration value
- `list`: List all configuration
- `reset`: Reset to defaults

**Examples:**
```bash
# Get value
cogos config get llm

# Set value
cogos config set llm claude-3.5-sonnet

# List all
cogos config list

# Reset
cogos config reset
```

---

### `cogos --version`

Show CogOS version.

```bash
cogos --version
# Output: CogOS v1.0.0
```

---

### `cogos --help`

Show help message.

```bash
cogos --help
cogos <command> --help
```

---

## Global Options

These options can be used with any command:

- `--llm <model>`: Specify LLM model
- `--api-key <key>`: Set API key
- `--config <file>`: Use custom config file
- `--verbose, -v`: Verbose output
- `--quiet, -q`: Quiet mode
- `--no-color`: Disable colors
- `--timeout <seconds>`: Set timeout

**Examples:**
```bash
# Use specific LLM
cogos --llm gpt-4 "Build a REST API"

# Custom config
cogos --config custom.yaml "Create a component"

# Verbose mode
cogos --verbose think "Debug this code"

# Quiet mode
cogos --quiet think "Simple task"

# Set timeout
cogos --timeout 600 "Complex task"
```

---

## Configuration Files

### `.cogos/config.yaml`

```yaml
# LLM Configuration
llm: claude-3.5-sonnet
api_key: ${ANTHROPIC_API_KEY}

# Cache Configuration
cache:
  enabled: true
  ttl: 3600
  max_size: 1000

# Safety Configuration
safety:
  level: STANDARD
  sandbox: true
  approval_required: true

# Agent Configuration
agents:
  max_iterations: 3
  timeout: 300

# Output Configuration
output:
  format: markdown
  include_metadata: true
  verbose: false
```

### Environment Variables

```bash
# LLM API Keys
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

# CogOS Configuration
export COGOS_LLM="claude-3.5-sonnet"
export COGOS_CACHE_ENABLED="true"
export COGOS_CACHE_TTL="3600"
export COGOS_SAFETY_LEVEL="STANDARD"
export COGOS_VERBOSE="false"
```

---

## Examples

### Complete Workflow

```bash
# 1. Install CogOS in project
cd /path/to/project
cogos install

# 2. Plan complex task
cogos plan "Build e-commerce platform" --output plan.md

# 3. Execute tasks
cogos think "Create user service" --modules python,postgresql
cogos think "Create product service" --modules python,mongodb
cogos think "Deploy to Kubernetes" --modules kubernetes,aws

# 4. Validate
cogos validate services/ --requirements requirements.txt

# 5. Generate tests
cogos test services/ --coverage

# 6. Generate docs
cogos document services/ --format markdown --output docs/
```

### Quick Tasks

```bash
# Create component
cogos "Create a React button component with TypeScript"

# Debug code
cogos debug "This function is throwing an error"

# Refactor
cogos refactor "Optimize this code for performance"

# Research
cogos research "Best practices for microservices"
```

### Automation

```bash
# Batch processing
for task in tasks/*.txt; do
    cogos think "$(cat $task)" --output "results/$(basename $task .txt).md"
done

# CI/CD integration
cogos validate src/ && cogos test src/ --coverage
```

---

## Output Formats

### Markdown (Default)

```bash
cogos "Create a REST API" --output api.md
```

### JSON

```bash
cogos "Create a REST API" --format json --output api.json
```

**Structure:**
```json
{
  "summary": "API created successfully",
  "code": "...",
  "tests": "...",
  "docs": "...",
  "metadata": {
    "agents_used": ["research", "code", "test", "document"],
    "iterations": 3,
    "tokens_used": 12345,
    "duration": 45.6
  }
}
```

### Code Only

```bash
cogos "Create a function" --format code > function.py
```

---

## Shell Completion

### Bash

Add to `~/.bashrc`:
```bash
eval "$(_COGOS_COMPLETE=bash_source cogos)"
```

### Zsh

Add to `~/.zshrc`:
```bash
eval "$(_COGOS_COMPLETE=zsh_source cogos)"
```

### Fish

Add to `~/.config/fish/completions/cogos.fish`:
```bash
_COGOS_COMPLETE=fish_source cogos
```

---

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid usage
- `3`: Network error
- `4`: API error
- `5`: Timeout
- `6`: Safety violation

---

**Next:** [Module API](modules.md)
