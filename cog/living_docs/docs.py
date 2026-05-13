"""
CogOS Living Documentation System
Auto-generates and maintains always-up-to-date documentation
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import subprocess


class LivingDocumentation:
    """Generate and maintain living documentation"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.docs_path = self.root_path / "docs"
        self.docs_path.mkdir(exist_ok=True)
        
    def generate_api_docs(self, output_path: Optional[str] = None) -> str:
        """Create API documentation from code"""
        
        api_docs = "# API Documentation\n\n"
        api_docs += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Analyze Python files
        for py_file in sorted(self.root_path.rglob("*.py")):
            if "test" in py_file.name.lower() or "__" in py_file.name:
                continue
            
            try:
                api_docs += self._generate_file_api_docs(py_file)
            except:
                pass
        
        # Analyze JavaScript files
        for js_file in sorted(self.root_path.rglob("*.{js,ts,jsx,tsx}")):
            try:
                api_docs += self._generate_js_api_docs(js_file)
            except:
                pass
        
        output_file = Path(output_path) if output_path else self.docs_path / "API.md"
        output_file.write_text(api_docs)
        
        return str(output_file)
    
    def _generate_file_api_docs(self, py_file: Path) -> str:
        """Generate API docs for Python file"""
        
        docs = f"## {py_file.name}\n\n"
        docs += f"**Path:** `{py_file.relative_to(self.root_path)}`\n\n"
        
        try:
            content = py_file.read_text()
            tree = ast.parse(content)
            
            # Extract module docstring
            module_doc = ast.get_docstring(tree)
            if module_doc:
                docs += f"{module_doc}\n\n"
            
            # Find classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    docs += self._generate_class_docs(node, py_file)
                
                elif isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                    docs += self._generate_function_docs(node, py_file)
        
        except:
            docs += f"*Error parsing file*\n\n"
        
        return docs
    
    def _generate_class_docs(self, node: ast.ClassDef, py_file: Path) -> str:
        """Generate documentation for a class"""
        
        docs = f"### Class: `{node.name}`\n\n"
        
        # Class docstring
        class_doc = ast.get_docstring(node)
        if class_doc:
            docs += f"{class_doc}\n\n"
        
        # Methods
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        if methods:
            docs += "**Methods:**\n\n"
            for method in methods:
                if not method.name.startswith('_'):
                    args = [arg.arg for arg in method.args.args]
                    returns = ast.get_source_segment(method.returns[0]) if method.returns else "None"
                    
                    docs += f"- `{method.name}({', '.join(args)}) -> {returns}`\n"
                    
                    method_doc = ast.get_docstring(method)
                    if method_doc:
                        docs += f"  {method_doc}\n"
                    docs += "\n"
        
        return docs
    
    def _generate_function_docs(self, node: ast.FunctionDef, py_file: Path) -> str:
        """Generate documentation for a function"""
        
        docs = f"### Function: `{node.name}()`\n\n"
        
        # Function docstring
        func_doc = ast.get_docstring(node)
        if func_doc:
            docs += f"{func_doc}\n\n"
        
        # Arguments
        if node.args.args:
            docs += "**Parameters:**\n\n"
            for arg in node.args.args:
                docs += f"- `{arg.arg}`: "
                if arg.annotation:
                    docs += f"{arg.annotation}"
                else:
                    docs += "Any"
                docs += "\n"
            docs += "\n"
        
        # Return type
        if node.returns:
            docs += f"**Returns:** {node.returns}\n\n"
        
        return docs
    
    def _generate_js_api_docs(self, js_file: Path) -> str:
        """Generate API docs for JavaScript/TypeScript file"""
        
        docs = f"## {js_file.name}\n\n"
        docs += f"**Path:** `{js_file.relative_to(self.root_path)}`\n\n"
        
        try:
            content = js_file.read_text()
            
            # Extract JSDoc comments
            jsdoc_pattern = r'/\*\*\s*(.*?)\s*\*/'
            for match in re.finditer(jsdoc_pattern, content, re.DOTALL):
                docs += f"{match.group(1)}\n\n"
            
            # Find exports
            exports = re.findall(r'(?:export\s+)?(?:const|function|class)\s+(\w+)', content)
            if exports:
                docs += "**Exports:**\n\n"
                for export_name in set(exports):
                    docs += f"- `{export_name}`\n"
                docs += "\n"
        
        except:
            docs += "*Error parsing file*\n\n"
        
        return docs
    
    def generate_architecture_diagrams(self) -> str:
        """Visualize system architecture"""
        
        diagrams = "# Architecture Diagrams\n\n"
        diagrams += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Generate dependency graph
        diagrams += "## Dependency Graph\n\n"
        diagrams += "```mermaid\n"
        diagrams += "graph TD\n"
        
        # Find modules and their dependencies
        modules = {}
        
        for py_file in self.root_path.rglob("*.py"):
            if "test" in py_file.name.lower() or "__" in py_file.name:
                continue
            
            try:
                content = py_file.read_text()
                imports = re.findall(r'^import\s+(\w+)|^from\s+(\w+)', content, re.MULTILINE)
                
                module_name = py_file.stem
                modules[module_name] = [imp[0] or imp[1] for imp in imports]
            except:
                pass
        
        # Build graph
        added_modules = set()
        for module, deps in modules.items():
            if module not in added_modules:
                diagrams += f"    {module}[{module}]\n"
                added_modules.add(module)
            
            for dep in deps:
                if dep not in added_modules:
                    diagrams += f"    {dep}[{dep}]\n"
                    added_modules.add(dep)
                
                diagrams += f"    {module} --> {dep}\n"
        
        diagrams += "```\n\n"
        
        # Generate component diagram
        diagrams += "## Component Architecture\n\n"
        diagrams += "```mermaid\n"
        diagrams += "graph LR\n"
        
        # Group by functionality
        api_modules = []
        model_modules = []
        service_modules = []
        
        for module in modules.keys():
            if any(x in module.lower() for x in ['api', 'route', 'controller']):
                api_modules.append(module)
            elif any(x in module.lower() for x in ['model', 'schema', 'entity']):
                model_modules.append(module)
            else:
                service_modules.append(module)
        
        # Create component layers
        if api_modules:
            diagrams += "    subgraph API\n"
            for module in api_modules:
                diagrams += f"        {module}[{module}]\n"
            diagrams += "    end\n"
        
        if model_modules:
            diagrams += "    subgraph Models\n"
            for module in model_modules:
                diagrams += f"        {module}[{module}]\n"
            diagrams += "    end\n"
        
        if service_modules:
            diagrams += "    subgraph Services\n"
            for module in service_modules:
                diagrams += f"        {module}[{module}]\n"
            diagrams += "    end\n"
        
        diagrams += "```\n\n"
        
        # Save diagrams
        diagrams_file = self.docs_path / "ARCHITECTURE.md"
        diagrams_file.write_text(diagrams)
        
        return str(diagrams_file)
    
    def generate_runbooks(self) -> str:
        """Create operational runbooks"""
        
        runbook = "# Operational Runbooks\n\n"
        runbook += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Development runbook
        runbook += "## Development Setup\n\n"
        runbook += "### Prerequisites\n"
        runbook += "- Python 3.8+\n"
        runbook += "- Git\n"
        runbook += "- Virtual environment\n\n"
        
        runbook += "### Setup Steps\n\n"
        runbook += "```bash\n"
        runbook += "# Clone repository\n"
        runbook += "git clone <repo-url>\n"
        runbook += "cd <project-name>\n\n"
        runbook += "# Create virtual environment\n"
        runbook += "python -m venv venv\n"
        runbook += "source venv/bin/activate  # On Windows: venv\\Scripts\\activate\n\n"
        runbook += "# Install dependencies\n"
        runbook += "pip install -r requirements.txt\n"
        runbook += "```\n\n"
        
        # Testing runbook
        runbook += "## Testing Procedures\n\n"
        runbook += "### Running Tests\n\n"
        runbook += "```bash\n"
        runbook += "# Run all tests\n"
        runbook += "pytest\n\n"
        runbook += "# Run specific test file\n"
        runbook += "pytest tests/test_specific.py\n\n"
        runbook += "# Run with coverage\n"
        runbook += "pytest --cov=cog --cov-report=html\n"
        runbook += "```\n\n"
        
        # Deployment runbook
        runbook += "## Deployment Guide\n\n"
        runbook += "### Pre-deployment Checklist\n"
        runbook += "- [ ] All tests passing\n"
        runbook += "- [ ] Environment variables configured\n"
        runbook += "- [ ] Database migrations applied\n"
        runbook += "- [ ] Static assets built\n\n"
        
        runbook += "### Deployment Steps\n\n"
        runbook += "```bash\n"
        runbook += "# Build application\n"
        runbook += "npm run build  # or python setup.py\n\n"
        runbook += "# Deploy to production\n"
        runbook += "./deploy.sh production\n"
        runbook += "```\n\n"
        
        # Troubleshooting runbook
        runbook += "## Troubleshooting\n\n"
        runbook += "### Common Issues\n\n"
        runbook += "#### Database connection errors\n"
        runbook += "**Symptoms:** Application cannot connect to database\n\n"
        runbook += "**Solutions:**\n"
        runbook += "1. Check database is running: `systemctl status postgresql`\n"
        runbook += "2. Verify connection string in .env\n"
        runbook += "3. Check database logs: `tail -f /var/log/postgresql/postgresql.log`\n\n"
        runbook += "#### Memory issues\n"
        runbook += "**Symptoms:** Application becomes slow or crashes\n\n"
        runbook += "**Solutions:**\n"
        runbook += "1. Check memory usage: `free -h`\n"
        runbook += "2. Restart application services\n"
        runbook += "3. Review logs for memory leaks\n\n"
        
        runbook_file = self.docs_path / "RUNBOOKS.md"
        runbook_file.write_text(runbook)
        
        return str(runbook_file)
    
    def generate_onboarding(self) -> str:
        """Create team onboarding guide"""
        
        onboarding = "# Developer Onboarding Guide\n\n"
        onboarding += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        onboarding += "## Welcome to the Team! 👋\n\n"
        onboarding += "This guide will help you get productive quickly.\n\n"
        
        # Day 1
        onboarding += "## Day 1: Setup and First Contribution\n\n"
        onboarding += "### Morning\n"
        onboarding += "1. **Setup Development Environment**\n"
        onboarding += "   - Follow [Development Setup](docs/RUNBOOKS.md#development-setup)\n"
        onboarding += "   - Get access to all required repositories\n"
        onboarding += "   - Configure your IDE\n\n"
        
        onboarding += "2. **Understand the Codebase**\n"
        onboarding += "   ```bash\n"
        onboarding += "   cog explain 'Show me the project structure'\n"
        onboarding += "   ```\n\n"
        
        onboarding += "### Afternoon\n"
        onboarding += "1. **Make Your First Change**\n"
        onboarding += "   - Pick a good first issue (marked 'good first issue')\n"
        onboarding += "   - Create a branch: `git checkout -b your-name/issue-123`\n"
        onboarding += "   - Make your changes\n"
        onboarding += "   - Run tests: `pytest`\n"
        onboarding += "   - Submit pull request\n\n"
        
        # Week 1
        onboarding += "## Week 1: Learning and Contributing\n\n"
        onboarding += "### Goals\n"
        onboarding += "- Complete 5 pull requests\n"
        onboarding += "- Review code with senior developers\n"
        onboarding += "- Attend team standups\n"
        onboarding += "- Read key documentation\n\n"
        
        onboarding += "### Resources\n"
        onboarding += "- [Architecture Documentation](docs/ARCHITECTURE.md)\n"
        onboarding += "- [API Reference](docs/API.md)\n"
        onboarding += "- [Coding Standards](docs/CODE_STANDARDS.md)\n"
        onboarding += "- [Troubleshooting Guide](docs/RUNBOOKS.md#troubleshooting)\n\n"
        
        # Key concepts
        onboarding += "## Key Concepts to Learn\n\n"
        
        # Analyze codebase to generate concepts
        concepts = self._extract_key_concepts()
        
        for concept in concepts[:10]:
            onboarding += f"### {concept['name']}\n\n"
            onboarding += f"{concept['description']}\n\n"
            if concept.get('files'):
                onboarding += f"**Key Files:**\n"
                for file in concept['files'][:5]:
                    onboarding += f"- `{file}`\n"
                onboarding += "\n"
        
        # Contacts
        onboarding += "## Team Contacts\n\n"
        onboarding += "- **Tech Lead:** [Contact info]\n"
        onboarding += "- **Product Owner:** [Contact info]\n"
        onboarding += "- **DevOps:** [Contact info]\n"
        onboarding += "- **Questions?** Ask in team chat or daily standup\n\n"
        
        onboarding_file = self.docs_path / "ONBOARDING.md"
        onboarding_file.write_text(onboarding)
        
        return str(onboarding_file)
    
    def _extract_key_concepts(self) -> List[Dict[str, Any]]:
        """Extract key concepts from codebase"""
        
        concepts = []
        
        # Find common patterns
        file_count = 0
        function_count = 0
        class_count = 0
        
        for py_file in self.root_path.rglob("*.py"):
            if "test" in py_file.name.lower() or "__" in py_file.name:
                continue
            
            file_count += 1
            
            try:
                content = py_file.read_text()
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        class_count += 1
                        
                        # Determine what the class does
                        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                        
                        # Add concept
                        concepts.append({
                            "name": node.name,
                            "type": "class",
                            "description": f"Class with {len(methods)} methods: {', '.join(methods[:5])}",
                            "files": [str(py_file.relative_to(self.root_path))]
                        })
                    
                    elif isinstance(node, ast.FunctionDef):
                        function_count += 1
                        
                        if not node.name.startswith('_'):
                            concepts.append({
                                "name": node.name,
                                "type": "function",
                                "description": f"Function with {len(node.args.args)} parameters",
                                "files": [str(py_file.relative_to(self.root_path))]
                            })
            
            except:
                pass
        
        # Add summary concepts
        concepts.insert(0, {
            "name": "Codebase Overview",
            "type": "overview",
            "description": f"Contains {file_count} Python files, {class_count} classes, {function_count} functions",
            "files": []
        })
        
        return concepts
    
    def watch_and_update(self, file_path: Path) -> bool:
        """Watch for changes and update documentation"""
        
        # This would normally use a file watcher
        # For now, just regenerate relevant docs
        
        if file_path.suffix in {".py", ".js", ".ts"}:
            # Update API docs
            self.generate_api_docs()
            
            # Update architecture diagrams if needed
            if "test" not in file_path.name.lower():
                self.generate_architecture_diagrams()
            
            return True
        
        return False
    
    def get_docs_summary(self) -> str:
        """Get summary of generated documentation"""
        
        summary = "📝 Living Documentation Summary\n\n"
        
        # List generated docs
        docs_files = list(self.docs_path.glob("*.md"))
        
        summary += f"Total documentation files: {len(docs_files)}\n\n"
        summary += "**Generated Documentation:**\n\n"
        
        for doc_file in docs_files:
            summary += f"- [{doc_file.stem}]({doc_file.name})\n"
        
        summary += f"\nLast updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        
        return summary


# Singleton instance
_living_docs = None

def get_living_documentation(root_path: str = "."):
    """Get living documentation instance"""
    global _living_docs
    if _living_docs is None:
        _living_docs = LivingDocumentation(root_path)
    return _living_docs
