# Module System Architecture

Deep dive into how CogOS modules work and how they're structured.

## Overview

CogOS modules are domain-specific expertise packs that contain:
- **Tools** - Specialized AI tools for specific technologies
- **Prompts** - Domain-specific prompt extensions
- **Best Practices** - Industry standards and patterns
- **Code Examples** - Real-world implementations

## Module Structure

### Directory Structure

```
cog/modules/my-module/
├── manifest.json       # Module metadata
├── module.py          # Module implementation
├── tools/             # Tool definitions
│   ├── tool1.json
│   └── tool2.json
└── README.md          # Module documentation
```

### Manifest File

```json
{
  "name": "my-module",
  "displayName": "My Module",
  "description": "Description of what this module does",
  "version": "1.0.0",
  "category": "language",
  "author": "Your Name",
  "license": "MIT",
  "cogos_version": ">=1.0.0",
  "tools": [
    {
      "name": "create-component",
      "description": "Create a component",
      "prompt": "Create a {type} component with {props} props",
      "examples": [
        "Create a button component",
        "Create a form component"
      ]
    }
  ],
  "dependencies": [],
  "keywords": ["my-module", "example"]
}
```

### Module Implementation

```python
from cogos.module import Module

class MyModule(Module):
    """My custom module."""

    def __init__(self):
        super().__init__(
            name="my-module",
            version="1.0.0"
        )

    def initialize(self):
        """Initialize the module."""
        # Load tools
        # Set up resources
        # Validate configuration
        pass

    def get_tools(self):
        """Return list of tools provided by this module."""
        return [
            {
                "name": "create-component",
                "description": "Create a component",
                "parameters": {
                    "type": "string",
                    "props": "object"
                }
            }
        ]
```

## Module Categories

### 1. Web

Modules for web development:
- `cog-web-css` - CSS styling and animations
- `cog-web-html` - HTML markup and structure

### 2. Languages

Modules for programming languages:
- `cog-lang-javascript` - JavaScript and Node.js
- `cog-lang-python` - Python development
- `cog-lang-java` - Java enterprise
- `cog-lang-csharp` - C# and .NET
- `cog-lang-ruby` - Ruby and Rails
- `cog-lang-php` - PHP frameworks
- `cog-lang-rust` - Rust systems programming

### 3. Backend

Modules for backend frameworks:
- `cog-backend-nodejs` - Node.js frameworks
- `cog-api-graphql` - GraphQL APIs

### 4. Databases

Modules for database systems:
- `cog-db-postgres` - PostgreSQL
- `cog-db-mysql` - MySQL
- `cog-db-mongodb` - MongoDB
- `cog-db-redis` - Redis
- `cog-db-elasticsearch` - Elasticsearch

### 5. OS

Modules for operating systems:
- `cog-os-linux` - Linux systems
- `cog-os-mac` - macOS systems
- `cog-os-windows` - Windows systems

### 6. Cloud

Modules for cloud platforms:
- `cog-cloud-aws` - Amazon Web Services
- `cog-cloud-azure` - Microsoft Azure
- `cog-cloud-gcp` - Google Cloud Platform

### 7. Infrastructure

Modules for infrastructure tools:
- `cog-infra-docker` - Docker containers
- `cog-infra-kubernetes` - Kubernetes orchestration

### 8. Tools

Modules for development tools:
- `cog-git` - Git version control

## Module Loading

### Auto-Loading

Modules are automatically loaded based on task keywords:

```python
from cogos import CogOS

cogos = CogOS()

# Automatically loads javascript, react, mongodb modules
result = cogos.think("Create a React app with MongoDB backend")
```

### Manual Loading

Specify which modules to use:

```python
result = cogos.think(
    "Build a web application",
    modules=["javascript", "react", "mongodb"]
)
```

### Module Discovery

CogOS discovers modules in:

1. **Built-in modules** - `cog/modules/`
2. **User modules** - `~/.cogos/modules/`
3. **Project modules** - `.cogos/modules/`

## Tool System

### Tool Structure

Each module provides tools that agents can use:

```json
{
  "name": "create-react-component",
  "description": "Create a React component with TypeScript",
  "prompt": "Create a React component named {name} with props: {props}",
  "parameters": {
    "name": {
      "type": "string",
      "description": "Component name",
      "required": true
    },
    "props": {
      "type": "object",
      "description": "Component props",
      "required": false
    }
  },
  "examples": [
    "Create a Button component",
    "Create a Form component with validation"
  ]
}
```

### Tool Invocation

Agents invoke tools during task execution:

```python
# Agent: "I need to create a React component"
# System: Finds tool 'create-react-component'
# System: Invokes tool with parameters
# System: Returns generated code
```

## Prompt Extensions

Modules provide domain-specific prompt extensions:

### Example: Python Module

```python
# Base prompt
"Write a function to fetch data from an API"

# With Python module extension
"Write a Python function using aiohttp to fetch data from an API asynchronously.
Include proper error handling, type hints, and follow PEP 8 guidelines."
```

### Best Practices Injection

Modules inject best practices into prompts:

```python
# JavaScript module adds:
- Use async/await over promises
- Prefer const over let
- Use template literals
- Follow ESLint rules
- Add JSDoc comments
```

## Module Dependencies

### Declaring Dependencies

```json
{
  "name": "my-module",
  "dependencies": [
    "python",
    "postgresql"
  ]
}
```

### Dependency Resolution

CogOS automatically resolves dependencies:

```python
# Loading module that depends on python and postgresql
cogos.load_module("my-module")
# Automatically loads: python, postgresql, my-module
```

## Module Registry

### Registry Structure

```json
{
  "modules": [
    {
      "name": "cog-lang-python",
      "version": "1.0.0",
      "path": "/path/to/module",
      "enabled": true,
      "tools": 11,
      "prompts": 261
    }
  ],
  "categories": {
    "languages": ["python", "javascript", "java", ...],
    "databases": ["postgres", "mysql", "mongodb", ...]
  }
}
```

### Registry Commands

```python
from cogos import registry

# List all modules
modules = registry.list_modules()

# Get module info
module = registry.get_module("python")

# Search modules
results = registry.search("web")

# Enable/disable module
registry.enable_module("python")
registry.disable_module("python")
```

## Module Versioning

### Semantic Versioning

Modules follow semantic versioning:

- `1.0.0` - Major.Minor.Patch
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

### Compatibility

```json
{
  "cogos_version": ">=1.0.0",
  "python_version": ">=3.8"
}
```

## Module Development

### Creating a Module

```python
from cogos.module import Module, Tool

class MyModule(Module):
    """Create a custom module."""

    def __init__(self):
        super().__init__(
            name="my-module",
            version="1.0.0",
            description="My custom module"
        )

        # Add tools
        self.add_tool(
            name="my-tool",
            description="My custom tool",
            prompt="Do something with {input}",
            parameters={"input": "string"}
        )

    def execute(self, tool_name, parameters):
        """Execute a tool."""
        if tool_name == "my-tool":
            return self._my_tool(parameters)

    def _my_tool(self, params):
        """Tool implementation."""
        # Custom logic here
        return result
```

### Testing Modules

```python
import pytest
from cogos.module import load_module

def test_my_module():
    """Test my module."""
    module = load_module("my-module")

    # Test tools
    tools = module.get_tools()
    assert len(tools) > 0

    # Test execution
    result = module.execute("my-tool", {"input": "test"})
    assert result is not None
```

## Best Practices

1. **Single Responsibility** - Each module should focus on one domain
2. **Minimal Dependencies** - Avoid unnecessary dependencies
3. **Clear Documentation** - Document all tools and parameters
4. **Version Carefully** - Follow semantic versioning
5. **Test Thoroughly** - Test all tools and scenarios
6. **Handle Errors** - Provide helpful error messages
7. **Follow Conventions** - Use standard naming and structure

## Performance

### Module Caching

Modules are cached after loading:

```python
# First load: slow (reads from disk)
module = load_module("python")

# Subsequent loads: fast (from cache)
module = load_module("python")
```

### Lazy Loading

Modules are loaded on-demand:

```python
# Module not loaded yet
cogos = CogOS()

# Module loaded when needed
result = cogos.think("Create a Python script")
```

## Security

### Module Sandboxing

Modules run in sandboxed environment:

```python
# Module cannot:
# - Access files outside project
# - Make network requests (unless allowed)
# - Modify system settings
# - Access sensitive data
```

### Permission System

Modules declare required permissions:

```json
{
  "name": "my-module",
  "permissions": [
    "read:project",
    "write:project",
    "network:http"
  ]
}
```

## Related Documentation

- [Module API](../api/modules.md)
- [Creating Custom Modules](../guides/custom_modules.md)
- [Python API](../api/python.md)

---

**Next:** [Multi-Agent System](multi_agent.md)
