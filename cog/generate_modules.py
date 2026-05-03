#!/usr/bin/env python3
"""
CogOS Module Generator
Quickly generate expert modules for any domain
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any

MODULE_TEMPLATES = {
    "web_framework": {
        "description": "{framework} web framework expertise",
        "capabilities": ["read_{fw}", "write_{fw}", "test_{fw}", "build_{fw}"],
        "tools": ["{fw}.build", "{fw}.test", "{fw}.lint", "{fw}.format"],
        "expertise": [
            "## {Framework} Expertise",
            "You understand {framework} including:",
            "- Component architecture and patterns",
            "- State management (hooks, context, stores)",
            "- Routing and navigation",
            "- Performance optimization",
            "- Testing with Jest, Testing Library",
            "- Build tools (Vite, Webpack, Turbopack)",
            "- Best practices and patterns",
            "",
            "When working with {framework}:",
            "- Use functional components and hooks",
            "- Implement proper error boundaries",
            "- Optimize re-renders and memoization",
            "- Follow {framework} best practices",
            "- Use TypeScript for type safety",
        ]
    },
    
    "programming_language": {
        "description": "{language} programming expertise",
        "capabilities": ["read_{lang}", "write_{lang}", "debug_{lang}", "test_{lang}"],
        "tools": ["{lang}.build", "{lang}.test", "{lang}.lint", "{lang}.format"],
        "expertise": [
            "## {Language} Expertise",
            "You understand {language} including:",
            "- Syntax and type system",
            "- Standard library and ecosystems",
            "- Package management",
            "- Testing frameworks",
            "- Performance characteristics",
            "- Best practices and idioms",
            "- Common patterns and anti-patterns",
            "",
            "When working with {language}:",
            "- Follow {language} best practices",
            "- Use appropriate data structures",
            "- Handle errors properly",
            "- Write clean, maintainable code",
        ]
    },
    
    "database": {
        "description": "{database} database expertise",
        "capabilities": ["query_{db}", "schema_{db}", "optimize_{db}", "backup_{db}"],
        "tools": ["{db}.query", "{db}.dump", "{db}.restore", "{db}.schema"],
        "expertise": [
            "## {Database} Expertise",
            "You understand {database} including:",
            "- Query language and optimization",
            "- Schema design and indexing",
            "- Transactions and consistency",
            "- Backup and recovery",
            "- Performance tuning",
            "- Replication and scaling",
            "",
            "When working with {database}:",
            "- Use parameterized queries",
            "- Optimize with appropriate indexes",
            "- Handle transactions properly",
            "- Consider performance implications",
        ]
    },
    
    "operating_system": {
        "description": "{os} operating system expertise",
        "capabilities": ["shell_{os}", "file_{os}", "process_{os}", "network_{os}"],
        "tools": ["{os}.shell", "{os}.file", "{os}.process", "{os}.service"],
        "expertise": [
            "## {OS} Expertise",
            "You understand {os} including:",
            "- Command line interface",
            "- File system structure",
            "- Process management",
            "- Services and daemons",
            "- Networking configuration",
            "- Package management",
            "- System administration",
            "",
            "When working with {os}:",
            "- Use appropriate commands for {os}",
            "- Follow {os} conventions",
            "- Consider {os}-specific behaviors",
            "- Respect permissions and security",
        ]
    },
    
    "package_manager": {
        "description": "{pkg} package management expertise",
        "capabilities": ["install_{pkg}", "update_{pkg}", "remove_{pkg}", "search_{pkg}"],
        "tools": ["{pkg}.install", "{pkg}.update", "{pkg}.remove", "{pkg}.search"],
        "expertise": [
            "## {Package} Expertise",
            "You understand {package} including:",
            "- Package installation and removal",
            "- Version management",
            "- Dependency resolution",
            "- Configuration files",
            "- Global vs local packages",
            "- Scripts and lifecycle hooks",
            "",
            "When working with {package}:",
            "- Use appropriate commands",
            "- Manage versions carefully",
            "- Understand dependency trees",
            "- Use global flags correctly",
        ]
    },
}


def generate_module(
    name: str,
    module_type: str,
    **variables: str
) -> Dict[str, Any]:
    """Generate a complete module configuration"""
    
    template = MODULE_TEMPLATES[module_type]
    
    # Substitute variables
    description = template["description"].format(**variables)
    capabilities = [cap.format(**variables) for cap in template["capabilities"]]
    tools = [tool.format(**variables) for tool in template["tools"]]
    expertise = "\n".join(template["expertise"]).format(**variables)
    
    # Create manifest
    manifest = {
        "name": name,
        "version": "1.0.0",
        "description": description,
        "capabilities": capabilities,
        "requires": get_requirements(module_type),
        "permissions": get_permissions(module_type),
        "entrypoint": "module.py"
    }
    
    # Create module code
    module_code = generate_module_code(name, expertise, tools)
    
    return {
        "manifest": manifest,
        "module_code": module_code,
        "expertise": expertise
    }


def get_requirements(module_type: str) -> List[str]:
    """Get module dependencies"""
    requirements_map = {
        "web_framework": ["code-core", "language-core", "web-core"],
        "programming_language": ["code-core", "language-core"],
        "database": ["code-core", "tool-core"],
        "operating_system": ["tool-core", "shell-core"],
        "package_manager": ["tool-core"],
    }
    return requirements_map.get(module_type, ["tool-core"])


def get_permissions(module_type: str) -> List[str]:
    """Get required permissions"""
    if module_type == "operating_system":
        return ["shell.execute", "filesystem.read", "filesystem.write"]
    elif module_type == "package_manager":
        return ["shell.execute", "network.request"]
    elif module_type == "database":
        return ["shell.execute", "network.request"]
    return ["shell.execute", "filesystem.read"]


def generate_module_code(name: str, expertise: str, tools: List[str]) -> str:
    """Generate module.py code"""
    return f'''from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult
from cog.verification.base import Verifier, VerificationResult, VerificationStatus


class GeneratedTool(Tool):
    """Auto-generated tool - customize as needed"""
    name = "{name}.tool"
    description = "Generic tool for {name}"
    required_permissions = ["shell.execute"]

    def execute(self, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool
        shell = ShellTool()
        # Implement tool logic
        return shell.execute(command="echo '{name} tool'", **kwargs)


class Cog{name.title().replace('-', '')}(CogModule):
    name = "{name}"
    version = "1.0.0"
    description = "{name} expertise module"

    def register_tools(self) -> list[Tool]:
        return [
            GeneratedTool(),
            # Add more tools as needed
        ]

    def get_prompt_extensions(self) -> list[str]:
        return [
            {expertise}
        ]

    def get_capabilities(self) -> list[str]:
        return [
            # Add capabilities
        ]


module = Cog{name.title().replace('-', '')}()
'''


def create_module_directory(
    base_path: Path,
    name: str,
    module_data: Dict[str, Any]
) -> None:
    """Create complete module directory structure"""
    
    module_path = base_path / name
    module_path.mkdir(parents=True, exist_ok=True)
    
    # Write manifest.json
    with open(module_path / "manifest.json", "w") as f:
        json.dump(module_data["manifest"], f, indent=2)
    
    # Write module.py
    with open(module_path / "module.py", "w") as f:
        f.write(module_data["module_code"])
    
    # Write README.md
    with open(module_path / "README.md", "w") as f:
        f.write(f"# {name}\n\n")
        f.write(f"{module_data['manifest']['description']}\n\n")
        f.write("## Capabilities\n\n")
        for cap in module_data["manifest"]["capabilities"]:
            f.write(f"- {cap}\n")
    
    print(f"✅ Created module: {name}")


# Module specifications for the 50+ experts
MODULES_TO_CREATE = [
    # Operating Systems
    ("cog-os-windows", "operating_system", {"os": "Windows"}),
    ("cog-os-mac", "operating_system", {"os": "macOS"}),
    ("cog-os-linux", "operating_system", {"os": "Linux"}),
    
    # Package Managers
    ("cog-package-npm", "package_manager", {"pkg": "NPM", "package": "npm"}),
    ("cog-package-npx", "package_manager", {"pkg": "NPX", "package": "npx"}),
    ("cog-package-homebrew", "package_manager", {"pkg": "Homebrew", "package": "brew"}),
    
    # Web Core
    ("cog-web-html", "programming_language", {"language": "HTML5"}),
    ("cog-web-css", "programming_language", {"language": "CSS3"}),
    ("cog-lang-javascript", "programming_language", {"language": "JavaScript"}),
    ("cog-lang-typescript", "programming_language", {"language": "TypeScript"}),
    
    # JavaScript Frameworks
    ("cog-framework-react", "web_framework", {"framework": "React", "fw": "react"}),
    ("cog-framework-vue", "web_framework", {"framework": "Vue", "fw": "vue"}),
    ("cog-framework-angular", "web_framework", {"framework": "Angular", "fw": "angular"}),
    ("cog-framework-svelte", "web_framework", {"framework": "Svelte", "fw": "svelte"}),
    
    # Backend
    ("cog-backend-nodejs", "programming_language", {"language": "Node.js"}),
    ("cog-api-rest", "programming_language", {"language": "REST APIs"}),
    
    # Databases
    ("cog-db-mysql", "database", {"database": "MySQL", "db": "mysql"}),
    ("cog-db-mongodb", "database", {"database": "MongoDB", "db": "mongodb"}),
    
    # Programming Languages
    ("cog-lang-go", "programming_language", {"language": "Go"}),
    ("cog-lang-cpp", "programming_language", {"language": "C++"}),
    
    # Modern Frameworks
    ("cog-framework-nextjs", "web_framework", {"framework": "Next.js", "fw": "nextjs"}),
    ("cog-framework-nuxtjs", "web_framework", {"framework": "Nuxt.js", "fw": "nuxtjs"}),
    ("cog-framework-remix", "web_framework", {"framework": "Remix", "fw": "remix"}),
    ("cog-framework-astro", "web_framework", {"framework": "Astro", "fw": "astro"}),
    ("cog-framework-solidjs", "web_framework", {"framework": "SolidJS", "fw": "solidjs"}),
    
    # Infrastructure
    ("cog-infra-mcp", "programming_language", {"language": "MCP Servers"}),
]


def main():
    """Generate all modules"""
    base_path = Path("modules")
    
    print("🚀 CogOS Module Generator")
    print("=" * 50)
    print(f"Generating {len(MODULES_TO_CREATE)} modules...")
    print()
    
    for module_spec in MODULES_TO_CREATE:
        name, module_type, variables = module_spec
        
        try:
            module_data = generate_module(name, module_type, **variables)
            create_module_directory(base_path, name, module_data)
        except Exception as e:
            print(f"❌ Error creating {name}: {e}")
    
    print()
    print("=" * 50)
    print("✅ Module generation complete!")
    print()
    print("Next steps:")
    print("1. Review generated modules")
    print("2. Customize tools for each module")
    print("3. Add domain-specific expertise")
    print("4. Test each module")
    print("5. Publish to registry")


if __name__ == "__main__":
    main()
