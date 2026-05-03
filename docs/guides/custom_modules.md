# Creating Custom Modules

Guide to creating your own CogOS modules with custom tools and expertise.

## Quick Start

### Module Generator

Use the built-in module generator:

```bash
cogos create-module my-module
```

This creates:
```
my-module/
├── manifest.json
├── module.py
├── tools/
│   └── example.json
└── README.md
```

## Manual Module Creation

### 1. Create Module Directory

```bash
mkdir ~/.cogos/modules/my-module
cd ~/.cogos/modules/my-module
```

### 2. Create Manifest

Create `manifest.json`:

```json
{
  "name": "my-framework",
  "displayName": "My Framework",
  "description": "Custom framework module",
  "version": "1.0.0",
  "category": "framework",
  "author": "Your Name",
  "license": "MIT",
  "cogos_version": ">=1.0.0",
  "tools": [
    {
      "name": "create-component",
      "description": "Create a component",
      "prompt": "Create a {type} component with {props} props using MyFramework",
      "parameters": {
        "type": "string",
        "props": "object"
      },
      "examples": [
        "Create a Button component",
        "Create a Form component"
      ]
    }
  ],
  "dependencies": [],
  "keywords": ["my-framework", "web"]
}
```

### 3. Create Module Implementation

Create `module.py`:

```python
from cogos.module import Module, Tool

class MyFrameworkModule(Module):
    """My Framework module."""

    def __init__(self):
        super().__init__(
            name="my-framework",
            version="1.0.0",
            description="Custom framework module"
        )

    def initialize(self):
        """Initialize module."""
        self.load_tools_from_json("tools/")

    def get_best_practices(self):
        """Return framework best practices."""
        return [
            "Use components for reusability",
            "Follow naming conventions",
            "Implement proper error handling",
            "Write tests for all components"
        ]

    def get_code_templates(self):
        """Return code templates."""
        return {
            "component": """
import { Component } from 'my-framework';

export class {ClassName} extends Component {
    render() {
        return `
            <div class="{className}">
                {content}
            </div>
        `;
    }
}
"""
        }
```

### 4. Create Tools

Create `tools/create-component.json`:

```json
{
  "name": "create-component",
  "description": "Create a MyFramework component",
  "prompt": "Create a {type} component in MyFramework with these props: {props}. Follow framework best practices.",
  "parameters": {
    "type": {
      "type": "string",
      "description": "Component type",
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
  ],
  "best_practices": [
    "Use PascalCase for component names",
    "Define prop types",
    "Add default props",
    "Include JSDoc comments"
  ]
}
```

### 5. Create Documentation

Create `README.md`:

```markdown
# My Framework Module

CogOS module for MyFramework development.

## Features

- Component generation
- Best practice enforcement
- Code templates
- Auto-completion

## Tools

### create-component

Create a MyFramework component.

**Example:**
\`\`\`
cogos think "Create a Button component in MyFramework"
\`\`\`

## Installation

\`\`\`bash
cogos install-module my-framework
\`\`\`

## Usage

\`\`\`python
from cogos import CogOS

cogos = CogOS()
result = cogos.think(
    "Create a Form component in MyFramework",
    modules=["my-framework"]
)
\`\`\`
```

## Module Registration

### Register Module

```bash
cogos register-module ~/.cogos/modules/my-module
```

### Verify Registration

```bash
cogos modules | grep my-framework
```

## Advanced Features

### Module Dependencies

Declare dependencies in manifest:

```json
{
  "dependencies": ["javascript", "react"]
}
```

### Custom Tool Logic

Implement custom tool execution:

```python
class MyFrameworkModule(Module):
    def execute_tool(self, tool_name, params):
        """Execute tool with custom logic."""
        if tool_name == "create-component":
            return self._create_component(params)

    def _create_component(self, params):
        """Custom component creation logic."""
        # Custom logic here
        component = self.generate_component(
            type=params["type"],
            props=params.get("props", {})
        )

        # Add framework-specific features
        component = self.add_framework_boilerplate(component)

        return component
```

### Prompt Extensions

Add custom prompt extensions:

```python
class MyFrameworkModule(Module):
    def extend_prompt(self, prompt, context):
        """Extend prompt with framework-specific context."""
        extensions = [
            "Use MyFramework v3.0+ syntax",
            "Follow component naming conventions",
            "Implement proper lifecycle methods",
            "Add error boundaries"
        ]

        return f"{prompt}\n\nFramework Guidelines:\n" + "\n".join(f"- {e}" for e in extensions)
```

### Code Generation

Implement code generation:

```python
class MyFrameworkModule(Module):
    def generate_code(self, spec):
        """Generate code from specification."""
        template = self.get_template(spec["type"])

        code = template.format(
            className=self.to_pascal_case(spec["name"]),
            props=self.generate_props(spec["props"]),
            methods=self.generate_methods(spec["methods"])
        )

        return code
```

## Testing Modules

### Unit Tests

Create `tests/test_my_module.py`:

```python
import pytest
from cogos.module import load_module

@pytest.fixture
def module():
    """Load module for testing."""
    return load_module("my-framework")

def test_module_loads(module):
    """Test module loads successfully."""
    assert module is not None
    assert module.name == "my-framework"

def test_module_tools(module):
    """Test module has tools."""
    tools = module.get_tools()
    assert len(tools) > 0
    assert "create-component" in [t["name"] for t in tools]

def test_tool_execution(module):
    """Test tool executes correctly."""
    result = module.execute_tool("create-component", {
        "type": "Button",
        "props": {"label": "Click me"}
    })
    assert result is not None
    assert "Button" in result
```

### Integration Tests

```python
def test_module_with_cogos():
    """Test module works with CogOS."""
    from cogos import CogOS

    cogos = CogOS()
    result = cogos.think(
        "Create a Button component",
        modules=["my-framework"]
    )

    assert result.code is not None
    assert "Button" in result.code
```

## Publishing Modules

### Prepare for Publishing

1. **Update manifest** with correct metadata
2. **Add documentation** (README.md)
3. **Add tests** (tests/)
4. **Add license** (LICENSE)
5. **Version properly** (semantic versioning)

### Publish to GitHub

```bash
cd ~/.cogos/modules/my-module
git init
git add .
git commit -m "Initial commit"
gh repo create my-framework-module --public
git remote add origin https://github.com/username/my-framework-module
git push -u origin main
```

### Publish to npm (for JS modules)

```bash
cd ~/.cogos/modules/my-module
npm publish
```

### Register in CogOS Registry

Submit your module to the CogOS module registry:

```bash
cogos publish-module my-framework
```

## Module Best Practices

### 1. Naming

- Use kebab-case for module names: `my-framework`
- Use descriptive names: `cog-cloud-aws` not `cog-aws`
- Avoid conflicts: Check existing modules first

### 2. Structure

- Follow standard directory structure
- Separate tools from logic
- Include comprehensive README
- Add examples and tests

### 3. Documentation

- Document all tools
- Provide examples
- Explain parameters
- Show usage patterns

### 4. Testing

- Test all tools
- Add integration tests
- Test edge cases
- Document test coverage

### 5. Versioning

- Follow semantic versioning
- Update CHANGELOG
- Tag releases
- Communicate breaking changes

## Module Examples

### Simple Module

```json
{
  "name": "text-processor",
  "description": "Text processing utilities",
  "tools": [
    {
      "name": "format-text",
      "description": "Format text according to style guide",
      "prompt": "Format this text according to {style} style guide: {text}"
    }
  ]
}
```

### Complex Module

```json
{
  "name": "microservice-framework",
  "description": "Microservice development framework",
  "dependencies": ["python", "docker", "kubernetes"],
  "tools": [
    {
      "name": "create-service",
      "description": "Create a microservice",
      "prompt": "Create a {language} microservice with {database}"
    },
    {
      "name": "generate-api",
      "description": "Generate REST API",
      "prompt": "Generate REST API for {service}"
    },
    {
      "name": "deploy-service",
      "description": "Deploy to Kubernetes",
      "prompt": "Deploy {service} to Kubernetes with {replicas} replicas"
    }
  ]
}
```

## Troubleshooting

### Module Not Found

```bash
# Check module is registered
cogos modules | grep my-module

# Re-register if needed
cogos register-module ~/.cogos/modules/my-module
```

### Tool Not Working

```python
# Test tool directly
from cogos.module import load_module

module = load_module("my-module")
result = module.execute_tool("my-tool", {"param": "value"})
print(result)
```

### Import Errors

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install dependencies
pip install -r requirements.txt
```

## Resources

- [Module API](../api/modules.md)
- [Architecture](../architecture/modules.md)
- [Examples](../examples/)

---

**Next:** [Performance Optimization](performance.md)
