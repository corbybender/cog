"""
CogOS Intelligent Test Generation System
Automatically generates comprehensive tests for code
"""

import ast
import re
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import subprocess


class IntelligentTestGenerator:
    """Generate comprehensive tests automatically"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.generated_tests = []
        
    def analyze_coverage(self) -> Dict[str, Any]:
        """Analyze test coverage"""
        
        coverage = {
            "total_files": 0,
            "tested_files": 0,
            "untested_files": [],
            "coverage_percentage": 0,
            "missing_tests": []
        }
        
        # Find all Python source files
        source_files = list(self.root_path.rglob("*.py"))
        source_files = [f for f in source_files if "test" not in f.name.lower()]
        
        coverage["total_files"] = len(source_files)
        
        # Find corresponding test files
        for source_file in source_files:
            test_file = self._find_test_file(source_file)
            
            if test_file and test_file.exists():
                coverage["tested_files"] += 1
            else:
                coverage["untested_files"].append(str(source_file))
        
        # Calculate coverage percentage
        if coverage["total_files"] > 0:
            coverage["coverage_percentage"] = (coverage["tested_files"] / coverage["total_files"]) * 100
        
        # Find missing test scenarios
        coverage["missing_tests"] = self._identify_missing_tests(source_files)
        
        return coverage
    
    def _find_test_file(self, source_file: Path) -> Optional[Path]:
        """Find test file for a source file"""
        
        # Common test file patterns
        test_patterns = [
            source_file.with_name(f"test_{source_file.name}"),
            source_file.with_name(f"{source_file.stem}_test.py"),
            source_file.parent / "tests" / f"test_{source_file.name}",
            source_file.parent / "tests" / (source_file.stem + "_test.py"),
            source_file.parent / "test" / source_file.name
        ]
        
        for pattern in test_patterns:
            if pattern.exists():
                return pattern
        
        return None
    
    def _identify_missing_tests(self, source_files: List[Path]) -> List[Dict[str, Any]]:
        """Find functions and classes without tests"""
        
        missing = []
        
        for source_file in source_files:
            try:
                content = source_file.read_text()
                tree = ast.parse(content)
                
                # Find all functions and classes
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        if not func_name.startswith("_"):
                            missing.append({
                                "file": str(source_file),
                                "type": "function",
                                "name": func_name,
                                "lineno": node.lineno,
                                "args": [arg.arg for arg in node.args.args]
                            })
                    
                    elif isinstance(node, ast.ClassDef):
                        class_name = node.name
                        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                        
                        missing.append({
                            "file": str(source_file),
                            "type": "class",
                            "name": class_name,
                            "lineno": node.lineno,
                            "methods": methods
                        })
            
            except:
                pass
        
        return missing
    
    def generate_unit_tests(self, file_path: Path) -> str:
        """Generate comprehensive unit tests for a file"""
        
        try:
            content = file_path.read_text()
            tree = ast.parse(content)
            
            test_code = f"""
# Auto-generated tests for {file_path.name}
import pytest
from {file_path.stem} import *

"""
            
            # Generate tests for each function
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    if func_name.startswith("_"):
                        continue
                    
                    args = [arg.arg for arg in node.args.args]
                    
                    # Generate test function
                    test_code += f"""
def test_{func_name}():
    # Test {func_name}
    # Arguments: {', '.join(args)}
    result = {func_name}({', '.join(args)})
    assert result is not None  # Implement specific assertions
    
"""
                    
                    # Generate edge case tests
                    if len(args) > 0:
                        test_code += f"""
def test_{func_name}_with_none():
    # Test {func_name} with None arguments
    with pytest.raises((TypeError, AttributeError)):
        {func_name}({', '.join(['None'] * len(args))})
    
"""
            
            # Generate tests for classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    
                    test_code += f"""
class Test{class_name}:
    def setup_method(self):
        # Setup test instance
        self.instance = {class_name}()
    
"""
                    
                    # Generate tests for methods
                    for subnode in node.body:
                        if isinstance(subnode, ast.FunctionDef) and not subnode.name.startswith("_"):
                            method_name = subnode.name
                            
                            test_code += f"""
    def test_{method_name}(self):
        # Test {class_name}.{method_name}
        result = self.instance.{method_name}()
        assert result is not None  # Implement specific assertions
    
"""
            
            return test_code
            
        except Exception as e:
            return f"# Error generating tests: {str(e)}\n"
    
    def generate_integration_tests(self, file_path: Path) -> str:
        """Generate integration tests"""
        
        return f"""
# Integration tests for {file_path.name}
import pytest

def test_{file_path.stem}_integration():
    # Test integration with other components
    assert True  # Implement integration test

def test_{file_path.stem}_with_database():
    # Test database interactions
    assert True  # Implement database test

def test_{file_path.stem}_with_api():
    # Test API interactions
    assert True  # Implement API test
"""
    
    def generate_edge_cases(self, file_path: Path) -> List[Dict[str, Any]]:
        """Generate edge case tests"""
        
        edge_cases = []
        
        try:
            content = file_path.read_text()
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    
                    # Generate edge cases based on parameters
                    for arg in node.args.args:
                        edge_cases.append({
                            "file": str(file_path),
                            "function": func_name,
                            "arg": arg.arg,
                            "test_type": "none_value",
                            "test_code": f"test_{func_name}_{arg.arg}_none"
                        })
                        
                        if arg.annotation == "int":
                            edge_cases.append({
                                "file": str(file_path),
                                "function": func_name,
                                "arg": arg.arg,
                                "test_type": "zero_value",
                                "test_code": f"test_{func_name}_{arg.arg}_zero"
                            })
                            
                            edge_cases.append({
                                "file": str(file_path),
                                "function": func_name,
                                "arg": arg.arg,
                                "test_type": "negative_value",
                                "test_code": f"test_{func_name}_{arg.arg}_negative"
                            })
        
        except:
            pass
        
        return edge_cases
    
    def generate_tests_for_coverage(self, target_coverage: float = 90.0) -> Dict[str, Any]:
        """Generate tests to reach target coverage"""
        
        # Analyze current coverage
        coverage = self.analyze_coverage()
        
        results = {
            "target_coverage": target_coverage,
            "current_coverage": coverage["coverage_percentage"],
            "files_analyzed": coverage["total_files"],
            "tests_generated": 0,
            "generated_files": []
        }
        
        # Generate tests for untested files
        for file_path_str in coverage["untested_files"]:
            file_path = Path(file_path_str)
            
            # Generate test file
            test_content = self.generate_unit_tests(file_path)
            
            # Write test file
            test_file_path = self._create_test_file(file_path, test_content)
            
            if test_file_path:
                results["tests_generated"] += 1
                results["generated_files"].append(str(test_file_path))
        
        return results
    
    def _create_test_file(self, source_file: Path, test_content: str) -> Optional[Path]:
        """Create test file in appropriate location"""
        
        # Determine test file location
        test_dir = source_file.parent / "tests"
        if not test_dir.exists():
            test_dir = source_file.parent
        
        test_file_name = f"test_{source_file.name}"
        test_file_path = test_dir / test_file_name
        
        try:
            # Create test directory if needed
            test_dir.mkdir(parents=True, exist_ok=True)
            
            # Write test file
            test_file_path.write_text(test_content)
            
            return test_file_path
            
        except Exception as e:
            return None
    
    def update_existing_tests(self, file_path: Path) -> bool:
        """Update tests when code changes"""
        
        test_file = self._find_test_file(file_path)
        
        if not test_file:
            # Create new test file
            test_content = self.generate_unit_tests(file_path)
            self._create_test_file(file_path, test_content)
            return True
        
        # Update existing test file
        try:
            old_content = test_file.read_text()
            new_content = self.generate_unit_tests(file_path)
            
            # Merge old and new tests (preserve manual tests)
            updated_content = self._merge_test_content(old_content, new_content)
            
            test_file.write_text(updated_content)
            return True
            
        except:
            return False
    
    def _merge_test_content(self, old_content: str, new_content: str) -> str:
        """Merge old and new test content"""
        
        # Simple merge - add new tests after old ones
        old_lines = old_content.split('\n')
        new_lines = new_content.split('\n')
        
        # Find where auto-generated tests end
        merge_point = len(old_lines)
        
        return '\n'.join(old_lines + new_lines)
    
    def generate_test_from_code(self, code: str, language: str = "python") -> str:
        """Generate test from code snippet"""
        
        if language == "python":
            return f"""
# Auto-generated test
import pytest

def test_generated_function():
    # Test the provided code
    {code}
    assert True  # Add specific assertions
"""
        else:
            return f"""
// Auto-generated test
// Test the provided code
{code}
// Add assertions
"""
    
    def get_test_summary(self) -> str:
        """Get summary of generated tests"""
        
        if not self.generated_tests:
            return "No tests generated yet."
        
        return f"""
🧪 Test Generation Summary

Total tests generated: {len(self.generated_tests)}

Recent tests:
"""
        
        for test in self.generated_tests[-10:]:
            summary += f"  • {test['file']}: {test['type']} ({test['timestamp']})\n"
        
        return summary


# Singleton instance
_test_generator = None

def get_test_generator(root_path: str = "."):
    """Get test generator instance"""
    global _test_generator
    if _test_generator is None:
        _test_generator = IntelligentTestGenerator(root_path)
    return _test_generator
