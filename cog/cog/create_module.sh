#!/bin/bash
# Quick module template generator

MODULE_NAME=$1
MODULE_DESC=$2
CAPABILITIES=$3

mkdir -p modules/$MODULE_NAME

# Create manifest
cat > modules/$MODULE_NAME/manifest.json << MANIFEST
{
  "name": "$MODULE_NAME",
  "version": "1.0.0",
  "description": "$MODULE_DESC",
  "capabilities": $CAPABILITIES,
  "requires": ["code-core", "language-core"],
  "permissions": ["filesystem.read", "filesystem.write", "shell.execute"],
  "entrypoint": "module.py"
}
MANIFEST

# Create module
cat > modules/$MODULE_NAME/module.py << MODULE
from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult

class $MODULE_NAME(CogModule):
    name = "$MODULE_NAME"
    version = "1.0.0"
    description = "$MODULE_DESC"

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## $MODULE_NAME Expertise",
            "",
            "You understand $MODULE_NAME including:",
            "- Core concepts and patterns",
            "- Best practices",
            "- Common tools and workflows",
            "- Troubleshooting",
        ]

    def get_capabilities(self) -> list[str]:
        return [
            # Add capabilities
        ]

module = $MODULE_NAME()
MODULE

echo "✅ Created module: $MODULE_NAME"
