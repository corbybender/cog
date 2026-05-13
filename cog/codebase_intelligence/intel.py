"""
CogOS Deep Codebase Intelligence System
Understands code structure, dependencies, patterns, and evolution
"""

import ast
import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from datetime import datetime
import subprocess
import re


class CodebaseIntelligence:
    """Deep understanding of entire codebase structure and patterns"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.cache_path = self.root_path / ".cogos" / "codebase_intel"
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        self.file_map = {}
        self.dependency_graph = {}
        self.patterns = {}
        self.evolution_history = []
        
    def analyze_structure(self) -> Dict[str, Any]:
        """Map entire codebase structure"""
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "root_path": str(self.root_path),
            "summary": {},
            "directories": {},
            "files": {},
            "languages": {},
            "frameworks": {},
            "dependencies": {},
            "entry_points": [],
            "patterns": []
        }
        
        # Analyze directories
        for item in self.root_path.rglob("*"):
            if item.is_dir():
                if self._should_ignore_dir(item):
                    continue
                    
                dir_info = self._analyze_directory(item)
                if dir_info:
                    analysis["directories"][str(item.relative_to(self.root_path))] = dir_info
        
        # Analyze files
        for item in self.root_path.rglob("*"):
            if item.is_file() and self._should_analyze_file(item):
                file_info = self._analyze_file(item)
                if file_info:
                    analysis["files"][str(item.relative_to(self.root_path))] = file_info
        
        # Build summary
        analysis["summary"] = {
            "total_directories": len(analysis["directories"]),
            "total_files": len(analysis["files"]),
            "languages": self._count_languages(analysis["files"]),
            "frameworks": self._detect_frameworks(analysis["files"])
        }
        
        # Find entry points
        analysis["entry_points"] = self._find_entry_points(analysis["files"])
        
        # Identify patterns
        analysis["patterns"] = self._identify_patterns(analysis["files"])
        
        # Save to cache
        self._save_analysis(analysis)
        
        return analysis
    
    def _should_ignore_dir(self, dir_path: Path) -> bool:
        """Check if directory should be ignored"""
        ignore_dirs = {
            ".git", ".cogos", "node_modules", "__pycache__", 
            "venv", ".venv", "env", ".env", "dist", "build",
            "target", ".next", ".nuxt", "coverage", ".pytest_cache"
        }
        return any(ignore_dir in dir_path.parts for ignore_dir in ignore_dirs)
    
    def _should_analyze_file(self, file_path: Path) -> bool:
        """Check if file should be analyzed"""
        if not file_path.is_file():
            return False
            
        extensions = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs", ".rb", ".php"}
        return file_path.suffix in extensions
    
    def _analyze_directory(self, dir_path: Path) -> Dict[str, Any]:
        """Analyze a directory"""
        try:
            files = list(dir_path.iterdir())
            code_files = [f for f in files if f.is_file() and self._should_analyze_file(f)]
            
            return {
                "name": dir_path.name,
                "path": str(dir_path.relative_to(self.root_path)),
                "file_count": len(code_files),
                "total_files": len(files),
                "code_ratio": len(code_files) / len(files) if files else 0
            }
        except PermissionError:
            return None
    
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file"""
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            info = {
                "name": file_path.name,
                "path": str(file_path.relative_to(self.root_path)),
                "extension": file_path.suffix,
                "size": file_path.stat().st_size,
                "lines": len(lines),
                "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
                "imports": [],
                "exports": [],
                "classes": [],
                "functions": [],
                "complexity": 0
            }
            
            # Extract information based on file type
            if file_path.suffix == ".py":
                info.update(self._analyze_python_file(file_path, content))
            elif file_path.suffix in {".js", ".ts", ".jsx", ".tsx"}:
                info.update(self._analyze_javascript_file(file_path, content))
            
            # Calculate complexity
            info["complexity"] = self._calculate_complexity(info)
            
            return info
        except Exception as e:
            return None
    
    def _analyze_python_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze Python file"""
        try:
            tree = ast.parse(content)
            
            imports = []
            classes = []
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                        "lineno": node.lineno
                    })
                elif isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "lineno": node.lineno
                    })
            
            return {
                "imports": imports,
                "classes": classes,
                "functions": functions
            }
        except:
            return {"imports": [], "classes": [], "functions": []}
    
    def _analyze_javascript_file(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript file"""
        imports = []
        exports = []
        classes = []
        functions = []
        
        # Simple regex-based extraction (can be enhanced with proper parsers)
        import_pattern = r"(?:import|require)\s+['\"]([^'\"]+)['\"]"
        exports_pattern = r"(?:export\s+(?:default\s+)?)?(\w+)"
        
        for match in re.finditer(import_pattern, content):
            imports.append(match.group(1))
        
        for match in re.finditer(exports_pattern, content):
            exports.append(match.group(1))
        
        # Find functions
        func_pattern = r"(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>|(\w+)\s*:\s*(?:async\s*)?\([^)]*\)\s*=>)"
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1) or match.group(2) or match.group(3)
            if func_name:
                functions.append({"name": func_name})
        
        # Find classes
        class_pattern = r"class\s+(\w+)"
        for match in re.finditer(class_pattern, content):
            classes.append({"name": match.group(1)})
        
        return {
            "imports": list(set(imports)),
            "exports": list(set(exports)),
            "classes": classes,
            "functions": functions
        }
    
    def _calculate_complexity(self, file_info: Dict[str, Any]) -> int:
        """Calculate file complexity"""
        complexity = 0
        
        # Base complexity from lines of code
        complexity += file_info.get("lines", 0) // 10
        
        # Add complexity for classes
        complexity += len(file_info.get("classes", [])) * 5
        
        # Add complexity for functions
        complexity += len(file_info.get("functions", [])) * 2
        
        # Add complexity for imports
        complexity += len(file_info.get("imports", []))
        
        return complexity
    
    def _count_languages(self, files: Dict[str, Dict]) -> Dict[str, int]:
        """Count files by language"""
        language_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".jsx": "JavaScript React",
            ".tsx": "TypeScript React",
            ".java": "Java",
            ".go": "Go",
            ".rs": "Rust",
            ".rb": "Ruby",
            ".php": "PHP"
        }
        
        languages = {}
        for file_path, file_info in files.items():
            ext = file_info.get("extension", "")
            lang = language_map.get(ext, "Other")
            languages[lang] = languages.get(lang, 0) + 1
        
        return languages
    
    def _detect_frameworks(self, files: Dict[str, Dict]) -> List[str]:
        """Detect frameworks used"""
        frameworks = []
        
        # Check for framework indicators
        for file_path, file_info in files.items():
            path_lower = file_path.lower()
            
            # React
            if any(x in path_lower for x in ["react", "jsx", "tsx"]):
                if "React" not in frameworks:
                    frameworks.append("React")
            
            # Vue
            if "vue" in path_lower:
                if "Vue" not in frameworks:
                    frameworks.append("Vue")
            
            # Next.js
            if "next" in path_lower:
                if "Next.js" not in frameworks:
                    frameworks.append("Next.js")
            
            # Django
            if "django" in path_lower or "settings.py" in path_lower:
                if "Django" not in frameworks:
                    frameworks.append("Django")
            
            # Flask
            if "flask" in path_lower or "app.py" in path_lower:
                if "Flask" not in frameworks:
                    frameworks.append("Flask")
        
        return frameworks
    
    def _find_entry_points(self, files: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """Find application entry points"""
        entry_points = []
        
        for file_path, file_info in files.items():
            file_name = file_info["name"].lower()
            
            # Common entry point files
            if file_name in ["main.py", "app.py", "index.js", "index.ts", "server.js", "app.js"]:
                entry_points.append({
                    "file": file_path,
                    "type": "application",
                    "confidence": "high"
                })
            
            # CLI entry points
            if file_name in ["cli.py", "command.js", "cmd.js"]:
                entry_points.append({
                    "file": file_path,
                    "type": "cli",
                    "confidence": "high"
                })
        
        return entry_points
    
    def _identify_patterns(self, files: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """Identify architectural patterns"""
        patterns = []
        
        # MVC pattern
        has_models = any("model" in f.lower() for f in files.keys())
        has_views = any("view" in f.lower() for f in files.keys())
        has_controllers = any("controller" in f.lower() for f in files.keys())
        
        if has_models and (has_views or has_controllers):
            patterns.append({
                "name": "MVC",
                "confidence": "high",
                "description": "Model-View-Controller architecture"
            })
        
        # Microservices pattern
        service_count = len([f for f in files.keys() if "service" in f.lower()])
        if service_count >= 3:
            patterns.append({
                "name": "Microservices",
                "confidence": "high",
                "description": f"{service_count} services detected"
            })
        
        # Repository pattern
        if any("repository" in f.lower() for f in files.keys()):
            patterns.append({
                "name": "Repository",
                "confidence": "medium",
                "description": "Repository pattern detected"
            })
        
        return patterns
    
    def _save_analysis(self, analysis: Dict[str, Any]):
        """Save analysis to cache"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cache_file = self.cache_path / f"analysis_{timestamp}.json"
        
        # Save current analysis
        cache_file.write_text(json.dumps(analysis, indent=2))
        
        # Update evolution history
        self.evolution_history.append({
            "timestamp": datetime.now().isoformat(),
            "file": str(cache_file),
            "summary": analysis["summary"]
        })
        
        # Save history
        history_file = self.cache_path / "evolution_history.json"
        history_file.write_text(json.dumps(self.evolution_history, indent=2))
    
    def generate_dependency_graph(self) -> Dict[str, List[str]]:
        """Generate dependency graph"""
        graph = {}
        
        analysis_file = self._get_latest_analysis()
        if not analysis_file:
            return graph
        
        analysis = json.loads(analysis_file.read_text())
        
        # Build dependency graph from file imports
        for file_path, file_info in analysis.get("files", {}).items():
            imports = file_info.get("imports", [])
            graph[file_path] = imports
        
        self.dependency_graph = graph
        return graph
    
    def trace_data_flow(self, entry_point: str) -> List[Dict[str, Any]]:
        """Trace how data flows through the system"""
        flow = []
        
        graph = self.generate_dependency_graph()
        
        # Start from entry point
        visited = set()
        queue = [entry_point]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            
            visited.add(current)
            
            # Find dependencies
            deps = graph.get(current, [])
            
            flow.append({
                "file": current,
                "dependencies": deps,
                "depth": len(visited)
            })
            
            # Add dependencies to queue
            queue.extend(deps)
        
        return flow
    
    def find_related_code(self, file_path: str, context_lines: int = 3) -> Dict[str, Any]:
        """Find code related to a specific file"""
        
        # Get imports from the file
        analysis = json.loads(self._get_latest_analysis().read_text())
        file_info = analysis.get("files", {}).get(file_path)
        
        if not file_info:
            return {}
        
        imports = file_info.get("imports", [])
        
        # Find files that import this file or share dependencies
        related = {
            "imports": imports,
            "imported_by": [],
            "shared_dependencies": []
        }
        
        for other_file, other_info in analysis.get("files", {}).items():
            # Find files that import this file
            if file_path in other_info.get("imports", []):
                related["imported_by"].append(other_file)
            
            # Find files with shared dependencies
            shared = set(imports) & set(other_info.get("imports", []))
            if shared:
                related["shared_dependencies"].extend(list(shared))
        
        return related
    
    def _get_latest_analysis(self) -> Path:
        """Get the latest analysis file"""
        cache_files = list(self.cache_path.glob("analysis_*.json"))
        if cache_files:
            return max(cache_files, key=lambda p: p.stat().st_mtime)
        return None
    
    def get_code_summary(self) -> str:
        """Get human-readable codebase summary"""
        analysis_file = self._get_latest_analysis()
        
        if not analysis_file:
            return "No analysis available. Run analyze_structure() first."
        
        analysis = json.loads(analysis_file.read_text())
        
        summary = f"""
📊 Codebase Analysis Summary

📁 Structure:
  • Directories: {analysis['summary']['total_directories']}
  • Files: {analysis['summary']['total_files']}

💻 Languages:
"""
        
        for lang, count in analysis['summary']['languages'].items():
            summary += f"  • {lang}: {count} files\n"
        
        summary += f"\n🎯 Frameworks:\n"
        for fw in analysis['summary']['frameworks']:
            summary += f"  • {fw}\n"
        
        summary += f"\n🚪 Entry Points:\n"
        for ep in analysis['entry_points']:
            summary += f"  • {ep['file']}: {ep['type']}\n"
        
        summary += f"\n🔍 Patterns:\n"
        for pattern in analysis['patterns']:
            summary += f"  • {pattern['name']}: {pattern['description']}\n"
        
        return summary


# Singleton instance
_codebase_intel = None

def get_codebase_intelligence(root_path: str = "."):
    """Get codebase intelligence instance"""
    global _codebase_intel
    if _codebase_intel is None:
        _codebase_intel = CodebaseIntelligence(root_path)
    return _codebase_intel
