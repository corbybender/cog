# CogOS Python API Reference

Complete reference for the CogOS Python API.

## Table of Contents

- [CogOS Class](#cogos-class)
- [Multi-Agent System](#multi-agent-system)
- [Modules](#modules)
- [Configuration](#configuration)
- [Results](#results)
- [Caching](#caching)
- [Safety](#safety)

---

## CogOS Class

The main CogOS class for multi-agent AI tasks.

### Initialization

```python
from cogos import CogOS

# Basic initialization
cogos = CogOS()

# With specific LLM
cogos = CogOS(llm="claude-3.5-sonnet")

# With configuration
cogos = CogOS(
    llm="claude-3.5-sonnet",
    cache_enabled=True,
    cache_ttl=3600,
    safety_level="STANDARD",
    verbose=True
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `llm` | str | `"claude-3.5-sonnet"` | LLM model to use |
| `cache_enabled` | bool | `True` | Enable response caching |
| `cache_ttl` | int | `3600` | Cache TTL in seconds |
| `safety_level` | str | `"STANDARD"` | Safety level (SAFE/STANDARD/ADVANCED/EXPERT/CRITICAL) |
| `verbose` | bool | `False` | Enable verbose logging |
| `max_iterations` | int | `3` | Max agent iterations |
| `timeout` | int | `300` | Task timeout in seconds |

### Methods

#### `think()`

Execute a multi-agent task.

```python
result = cogos.think(
    "Build a REST API with FastAPI and PostgreSQL",
    modules=["python", "postgresql"],
    context={"previous_result": previous},
    safety_level="STANDARD"
)
```

**Parameters:**
- `task` (str): The task to execute
- `modules` (List[str], optional): Specific modules to use
- `context` (dict, optional): Context from previous tasks
- `safety_level` (str, optional): Override safety level
- `max_iterations` (int, optional): Override max iterations

**Returns:** `CogOSResult` object

#### `plan()`

Create a hierarchical plan for complex tasks.

```python
plan = cogos.plan("Build an e-commerce platform")

# Access the plan
for step in plan.steps:
    print(f"{step.id}: {step.description}")
    print(f"  Modules: {step.modules}")
    print(f"  Dependencies: {step.dependencies}")
```

**Returns:** `Plan` object with steps, dependencies, and modules

#### `research()`

Execute multi-source research.

```python
research = cogos.research("Best practices for microservices with Node.js")

# Access results
print(research.summary)
print(research.sources)      # Web, docs, codebase
print(research.findings)     # Key findings
print(research.code_examples) # Relevant code examples
```

**Returns:** `ResearchResult` object

#### `validate()`

Validate code or requirements.

```python
validation = cogos.validate(
    code=code_string,
    requirements=requirements_list
)

# Check validation
print(validation.passed)      # True/False
print(validation.issues)      # List of issues
print(validation.suggestions) # Improvement suggestions
```

**Returns:** `ValidationResult` object

#### `optimize()`

Optimize code for performance or cost.

```python
optimized = cogos.optimize(
    code=code_string,
    objective="performance"  # or "cost", "memory", etc.
)

print(optimized.code)        # Optimized code
print(optimized.improvements) # List of improvements
print(optimized.benchmarks)   # Performance data
```

**Returns:** `OptimizationResult` object

---

## Multi-Agent System

### Agent Types

CogOS uses 10 specialized agents:

#### Research Agent

```python
from cogos.agents import ResearchAgent

agent = ResearchAgent()
result = agent.research("Docker best practices for Node.js")
```

#### Code Agent

```python
from cogos.agents import CodeAgent

agent = CodeAgent()
result = agent.write_code("Create a REST API with Express")
```

#### Test Agent

```python
from cogos.agents import TestAgent

agent = TestAgent()
result = agent.generate_tests(code_string)
```

#### Document Agent

```python
from cogos.agents import DocumentAgent

agent = DocumentAgent()
result = agent.generate_docs(code_string)
```

#### Architect Agent

```python
from cogos.agents import ArchitectAgent

agent = ArchitectAgent()
result = agent.design_architecture("Microservices for e-commerce")
```

#### Critique Agent

```python
from cogos.agents import CritiqueAgent

agent = CritiqueAgent()
result = agent.critique(code_string)
```

#### Validate Agent

```python
from cogos.agents import ValidateAgent

agent = ValidateAgent()
result = agent.validate(code_string, requirements)
```

#### Optimize Agent

```python
from cogos.agents import OptimizeAgent

agent = OptimizeAgent()
result = agent.optimize(code_string, objective="performance")
```

### Custom Agent Workflows

```python
from cogos import AgentWorkflow

# Define custom workflow
workflow = AgentWorkflow()
workflow.add_agent("research", ResearchAgent())
workflow.add_agent("code", CodeAgent(), dependencies=["research"])
workflow.add_agent("test", TestAgent(), dependencies=["code"])
workflow.add_agent("critique", CritiqueAgent(), dependencies=["code"])

# Execute workflow
result = workflow.execute("Build a REST API")
```

---

## Modules

### Using Modules

```python
# Auto-detection
result = cogos.think("Build a React app with TypeScript")

# Manual selection
result = cogos.think(
    "Build a web application",
    modules=["javascript", "react", "mongodb"]
)

# Get available modules
modules = cogos.list_modules()
for module in modules:
    print(f"{module.name}: {module.description}")
```

### Module Information

```python
from cogos import get_module

module = get_module("python")
print(module.name)         # "python"
print(module.description)  # "Python development"
print(module.tools)        # List of tools
print(module.prompts)      # Number of prompt extensions
```

### Creating Custom Modules

```python
from cogos import Module

module = Module(
    name="my-framework",
    description="My custom framework",
    version="1.0.0"
)

# Add tools
module.add_tool(
    name="create-component",
    description="Create a component",
    prompt="Create a {type} component with {props}"
)

# Register module
module.register()
```

---

## Configuration

### Environment Variables

```bash
# LLM API Keys
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

# CogOS Configuration
export COGOS_CACHE_ENABLED="true"
export COGOS_CACHE_TTL="3600"
export COGOS_SAFETY_LEVEL="STANDARD"
export COGOS_VERBOSE="false"
```

### Configuration File

Create `.cogos/config.yaml`:

```yaml
llm: "claude-3.5-sonnet"
cache:
  enabled: true
  ttl: 3600
  max_size: 1000
safety:
  level: "STANDARD"
  sandbox: true
  approval_required: true
agents:
  max_iterations: 3
  timeout: 300
verbose: false
```

### Programmatic Configuration

```python
from cogos import configure

configure({
    "llm": "claude-3.5-sonnet",
    "cache_enabled": True,
    "cache_ttl": 3600,
    "safety_level": "STANDARD",
    "verbose": True
})
```

---

## Results

### CogOSResult

```python
result = cogos.think("Build a REST API")

# Access result properties
print(result.summary)     # High-level summary
print(result.code)        # Generated code
print(result.tests)       # Test suite
print(result.docs)        # Documentation
print(result.metadata)    # Metadata (agents used, iterations, etc.)

# Export result
result.export("output/")
result.to_json("result.json")
result.to_markdown("result.md")
```

### Result Metadata

```python
print(result.metadata.agents_used)    # ["research", "code", "test", ...]
print(result.metadata.iterations)     # 3
print(result.metadata.tokens_used)    # 12345
print(result.metadata.duration)       # 45.6 (seconds)
print(result.metadata.modules)        # ["python", "postgresql"]
```

---

## Caching

### Enable Caching

```python
# Global caching
cogos = CogOS(cache_enabled=True)

# Per-task caching
result = cogos.think(
    "Build a REST API",
    use_cache=True
)
```

### Cache Configuration

```python
from cogos.cache import SmartCache

cache = SmartCache(
    ttl=3600,          # Time-to-live in seconds
    max_size=1000,     # Max cache entries
    eviction="lru"     # Eviction policy (lru, lfu, fifo)
)

# Use custom cache
cogos = CogOS(cache=cache)
```

### Cache Management

```python
# Clear cache
cogos.cache.clear()

# Get cache stats
stats = cogos.cache.stats()
print(f"Hit rate: {stats.hit_rate}")
print(f"Entries: {stats.entries}")

# Inspect cache
for key, value in cogos.cache.items():
    print(f"{key}: {value}")
```

---

## Safety

### Safety Levels

```python
# SAFE - No dangerous operations
cogos.think("Create a Hello World app", safety_level="SAFE")

# STANDARD - Requires approval for dangerous ops
cogos.think("Deploy to AWS", safety_level="STANDARD")

# ADVANCED - More freedom with warnings
cogos.think("Configure Kubernetes", safety_level="ADVANCED")

# EXPERT - Full access
cogos.think("Root system operations", safety_level="EXPERT")

# CRITICAL - Dangerous operations, explicit approval
cogos.think("Format hard drive", safety_level="CRITICAL")
```

### Permission System

```python
from cogos.safety import Permission

# Check if operation is allowed
permission = Permission.check("write_file", "/etc/passwd")
print(permission.allowed)    # False
print(permission.reason)     # "System file modification"

# Request approval
if permission.requires_approval:
    approved = permission.request_approval()
    if approved:
        # Execute operation
        pass
```

### Sandbox

```python
from cogos.safety import Sandbox

# Run code in sandbox
sandbox = Sandbox()
result = sandbox.execute(code_string)

# Sandbox is isolated and safe
# - No network access
# - No file system access
# - Limited resources
# - Timeboxed execution
```

---

## Examples

### Complete Workflow

```python
from cogos import CogOS

# Initialize
cogos = CogOS(
    llm="claude-3.5-sonnet",
    cache_enabled=True,
    safety_level="STANDARD"
)

# Plan complex task
plan = cogos.plan("Build an e-commerce platform")

# Execute plan step by step
for step in plan.steps:
    result = cogos.think(
        step.description,
        modules=step.modules
    )
    print(f"✅ {step.description}")

# Validate final result
validation = cogos.validate(result.code, plan.requirements)
if validation.passed:
    print("✅ All requirements met!")
else:
    print(f"❌ Issues: {validation.issues}")
```

### Custom Agent Workflow

```python
from cogos import CogOS, AgentWorkflow
from cogos.agents import ResearchAgent, CodeAgent, TestAgent

# Create custom workflow
workflow = AgentWorkflow()
workflow.add_agent("research", ResearchAgent())
workflow.add_agent("code", CodeAgent(), dependencies=["research"])
workflow.add_agent("test", TestAgent(), dependencies=["code"])

# Execute with workflow
result = cogos.think(
    "Build a REST API",
    workflow=workflow
)
```

---

## Type Hints

```python
from cogos import CogOS, CogOSResult, Plan, ResearchResult
from typing import List, Dict, Optional

def process_task(
    task: str,
    modules: Optional[List[str]] = None
) -> CogOSResult:
    """Process a task with CogOS."""
    cogos = CogOS()
    return cogos.think(task, modules=modules)

def create_plan(task: str) -> Plan:
    """Create a plan for a complex task."""
    cogos = CogOS()
    return cogos.plan(task)

def research_topic(topic: str) -> ResearchResult:
    """Research a topic."""
    cogos = CogOS()
    return cogos.research(topic)
```

---

## Error Handling

```python
from cogos import CogOS, CogOSError, SafetyError, TimeoutError

try:
    cogos = CogOS()
    result = cogos.think("Build a REST API")
except CogOSError as e:
    print(f"CogOS error: {e}")
except SafetyError as e:
    print(f"Safety violation: {e}")
except TimeoutError as e:
    print(f"Task timed out: {e}")
```

---

**Next:** [CLI Reference](cli.md)
