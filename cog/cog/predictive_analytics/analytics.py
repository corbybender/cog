"""
CogOS Predictive Analytics System
Predict bugs, performance issues, and scalability problems
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class PredictiveAnalytics:
    """Predict future issues before they happen"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.predictions = []
        self.historical_data = self._load_historical_data()
        
    def predict_bugs(self, timeframe: str = "2 weeks") -> List[Dict[str, Any]]:
        """Forecast potential bugs"""
        
        predictions = []
        
        # Analyze code for bug-prone patterns
        for py_file in self.root_path.rglob("*.py"):
            file_predictions = self._predict_file_bugs(py_file)
            predictions.extend(file_predictions)
        
        # Analyze bug density over time
        density_prediction = self._predict_bug_density(timeframe)
        if density_prediction:
            predictions.append(density_prediction)
        
        return predictions
    
    def _predict_file_bugs(self, file_path: Path) -> List[Dict[str, Any]]:
        """Predict bugs in a specific file"""
        
        predictions = []
        
        try:
            content = file_path.read_text()
            lines = content.split('\n')
            
            # High complexity files are more bug-prone
            complexity = len(lines) // 10 + content.count('class ') * 5 + content.count('def ') * 2
            
            if complexity > 50:
                predictions.append({
                    "type": "high_complexity",
                    "severity": "medium",
                    "confidence": 0.7,
                    "file": str(file_path),
                    "prediction": f"High complexity ({complexity}) increases bug risk",
                    "suggestion": "Consider refactoring into smaller modules",
                    "timeframe": "2-4 weeks"
                })
            
            # Files with many TODOs have technical debt
            todo_count = content.count('TODO') + content.count('FIXME')
            if todo_count > 5:
                predictions.append({
                    "type": "technical_debt",
                    "severity": "low",
                    "confidence": 0.8,
                    "file": str(file_path),
                    "prediction": f"{todo_count} unresolved TODOs indicate potential issues",
                    "suggestion": "Resolve TODOs or document technical decisions",
                    "timeframe": "1-2 weeks"
                })
            
            # Files with many imports may have dependency issues
            import_count = len(re.findall(r'^import |^from ', content, re.MULTILINE))
            if import_count > 15:
                predictions.append({
                    "type": "dependency_bloat",
                    "severity": "medium",
                    "confidence": 0.6,
                    "file": str(file_path),
                    "prediction": f"High import count ({import_count}) suggests tight coupling",
                    "suggestion": "Review dependencies and consider facades",
                    "timeframe": "3-6 weeks"
                })
            
            # Files with many exception handlers may have error-prone logic
            try_count = content.count('try:')
            if try_count > 10:
                predictions.append({
                    "type": "error_handling_complexity",
                    "severity": "medium",
                    "confidence": 0.65,
                    "file": str(file_path),
                    "prediction": f"High try count ({try_count}) suggests complex error scenarios",
                    "suggestion": "Consider simplifying error handling strategy",
                    "timeframe": "2-3 weeks"
                })
        
        except:
            pass
        
        return predictions
    
    def _predict_bug_density(self, timeframe: str) -> Dict[str, Any]:
        """Predict overall bug density"""
        
        # This would normally use historical data
        # For now, use heuristics
        
        total_files = len(list(self.root_path.rglob("*.py")))
        high_complexity_files = 0
        
        for py_file in self.root_path.rglob("*.py"):
            try:
                lines = len(py_file.read_text().split('\n'))
                if lines > 500:
                    high_complexity_files += 1
            except:
                pass
        
        bug_risk = (high_complexity_files / total_files) if total_files > 0 else 0
        
        if bug_risk > 0.3:
            return {
                "type": "bug_density",
                "severity": "high",
                "confidence": 0.75,
                "prediction": f"High bug density expected: {bug_risk:.1%} of files are high-complexity",
                "suggestion": "Focus testing on high-complexity files",
                "timeframe": timeframe
            }
        
        return None
    
    def predict_performance(self, timeframe: str = "2 weeks") -> List[Dict[str, Any]]:
        """Identify future performance bottlenecks"""
        
        predictions = []
        
        # Analyze database queries
        for py_file in self.root_path.rglob("*.py"):
            try:
                content = py_file.read_text()
                lines = content.split('\n')
                
                # Find database queries
                for i, line in enumerate(lines):
                    # SELECT * without LIMIT
                    if re.search(r'SELECT\s+\*\s+FROM', line, re.IGNORECASE):
                        if 'LIMIT' not in line:
                            predictions.append({
                                "type": "query_performance",
                                "severity": "medium",
                                "confidence": 0.7,
                                "file": str(py_file),
                                "line": i + 1,
                                "prediction": "SELECT * without LIMIT may cause performance issues",
                                "suggestion": "Add LIMIT clause or select specific columns",
                                "timeframe": "1-2 weeks"
                            })
                    
                    # Nested loops (O(n²) complexity)
                    if re.search(r'for\s+\w+\s+in\s+.*:.*for\s+\w+\s+in', line):
                        predictions.append({
                            "type": "algorithmic_complexity",
                            "severity": "high",
                            "confidence": 0.8,
                            "file": str(py_file),
                            "line": i + 1,
                            "prediction": "Nested loop detected - O(n²) or worse complexity",
                            "suggestion": "Consider using sets, dictionaries, or algorithm optimization",
                            "timeframe": "2-4 weeks"
                        })
                    
                    # Synchronous I/O in async context
                    if 'async def' in content:
                        if re.search(r'\.sleep\(|\.read\(|\.write\(', line):
                            predictions.append({
                                "type": "async_blocking",
                                "severity": "high",
                                "confidence": 0.75,
                                "file": str(py_file),
                                "line": i + 1,
                                "prediction": "Blocking I/O in async function defeats async benefits",
                                "suggestion": "Use async/await versions of I/O operations",
                                "timeframe": "1 week"
                            })
            
            except:
                pass
        
        # Predict memory issues
        large_files = []
        for py_file in self.root_path.rglob("*.py"):
            try:
                if py_file.stat().st_size > 100000:  # 100KB
                    large_files.append(str(py_file))
            except:
                pass
        
        if large_files:
            predictions.append({
                "type": "memory_usage",
                "severity": "medium",
                "confidence": 0.6,
                "prediction": f"Large files ({len(large_files)} files > 100KB) may cause memory issues",
                "suggestion": "Consider splitting large files into modules",
                "timeframe": "3-4 weeks",
                "files": large_files
            })
        
        return predictions
    
    def predict_scalability(self, scenario: str = "double_traffic") -> Dict[str, Any]:
        """Forecast scaling issues"""
        
        prediction = {
            "scenario": scenario,
            "predictions": [],
            "confidence": 0.0,
            "recommendations": []
        }
        
        # Analyze current architecture
        has_caching = self._check_for_caching()
        has_load_balancing = self._check_for_load_balancing()
        has_database_indexing = self._check_for_database_indexing()
        
        if scenario == "double_traffic":
            confidence = 0.0
            
            # Check for bottlenecks
            if not has_caching:
                prediction["predictions"].append({
                    "issue": "Database bottleneck",
                    "severity": "high",
                    "reason": "No caching detected - database will be hit twice as hard"
                })
                confidence += 0.3
            
            if not has_load_balancing:
                prediction["predictions"].append({
                    "issue": "Single point of failure",
                    "severity": "high",
                    "reason": "No load balancing detected"
                })
                confidence += 0.3
            
            if not has_database_indexing:
                prediction["predictions"].append({
                    "issue": "Query slowdown",
                    "severity": "medium",
                    "reason": "Missing database indexes will slow down under load"
                })
                confidence += 0.2
            
            prediction["confidence"] = min(confidence, 0.85)
            
            # Generate recommendations
            prediction["recommendations"] = [
                "Implement Redis caching for frequent queries",
                "Add database connection pooling",
                "Create read replicas for database",
                "Implement CDN for static assets",
                "Add horizontal auto-scaling"
            ]
        
        elif scenario == "10x_users":
            prediction["predictions"].append({
                "issue": "Database connection exhaustion",
                "severity": "high",
                "reason": "Connection pools will be exhausted"
            })
            
            prediction["predictions"].append({
                "issue": "Memory exhaustion",
                "severity": "high",
                "reason": "Memory usage scales linearly with users"
            })
            
            prediction["confidence"] = 0.8
            prediction["recommendations"] = [
                "Implement connection pooling with limits",
                "Add database sharding",
                "Implement session stores (Redis)",
                "Add horizontal pod autoscaling",
                "Consider microservices architecture"
            ]
        
        return prediction
    
    def _check_for_caching(self) -> bool:
        """Check if caching is implemented"""
        
        cache_keywords = ['cache', 'redis', 'memcached', 'lru_cache']
        
        for py_file in self.root_path.rglob("*.py"):
            try:
                content = py_file.read_text().lower()
                if any(keyword in content for keyword in cache_keywords):
                    return True
            except:
                pass
        
        return False
    
    def _check_for_load_balancing(self) -> bool:
        """Check if load balancing is configured"""
        
        lb_keywords = ['load_balancer', 'nginx', 'haproxy', 'kubernetes', 'ecs']
        
        for config_file in self.root_path.rglob("*.{yml,yaml,json,conf}"):
            try:
                content = config_file.read_text().lower()
                if any(keyword in content for keyword in lb_keywords):
                    return True
            except:
                pass
        
        return False
    
    def _check_for_database_indexing(self) -> bool:
        """Check if database indexes are used"""
        
        index_keywords = ['create index', 'index=True', 'db_index']
        
        for py_file in self.root_path.rglob("*.py"):
            try:
                content = py_file.read_text().lower()
                if any(keyword in content for keyword in index_keywords):
                    return True
            except:
                pass
        
        return False
    
    def estimate_tech_debt(self) -> Dict[str, Any]:
        """Calculate technical debt cost"""
        
        tech_debt = {
            "total_debt_hours": 0,
            "debt_categories": {},
            "priority_items": []
        }
        
        # Count TODOs and FIXMEs
        todo_count = 0
        fixme_count = 0
        
        for py_file in self.root_path.rglob("*.py"):
            try:
                content = py_file.read_text()
                todo_count += content.count('TODO')
                fixme_count += content.count('FIXME')
            except:
                pass
        
        if todo_count > 0:
            tech_debt["debt_categories"]["TODOs"] = todo_count
            tech_debt["total_debt_hours"] += todo_count * 2  # 2 hours per TODO
        
        if fixme_count > 0:
            tech_debt["debt_categories"]["FIXMEs"] = fixme_count
            tech_debt["total_debt_hours"] += fixme_count * 4  # 4 hours per FIXME
        
        # Check for duplicate code
        duplicate_estimate = self._estimate_duplicate_code()
        if duplicate_estimate > 0:
            tech_debt["debt_categories"]["duplicate_code"] = duplicate_estimate
            tech_debt["total_debt_hours"] += duplicate_estimate * 8  # 8 hours to refactor
        
        # Check for complex files
        complex_files = 0
        for py_file in self.root_path.rglob("*.py"):
            try:
                if len(py_file.read_text().split('\n')) > 500:
                    complex_files += 1
            except:
                pass
        
        if complex_files > 0:
            tech_debt["debt_categories"]["complex_files"] = complex_files
            tech_debt["total_debt_hours"] += complex_files * 16  # 16 hours to refactor
        
        # Generate priority items
        if fixme_count > 0:
            tech_debt["priority_items"].append({
                "priority": "high",
                "issue": f"{fixme_count} FIXMEs need attention",
                "estimated_hours": fixme_count * 4
            })
        
        if complex_files > 3:
            tech_debt["priority_items"].append({
                "priority": "medium",
                "issue": f"{complex_files} complex files need refactoring",
                "estimated_hours": complex_files * 16
            })
        
        return tech_debt
    
    def _estimate_duplicate_code(self) -> int:
        """Estimate amount of duplicate code"""
        
        # Simple heuristic: count similar function names
        function_names = defaultdict(list)
        
        for py_file in self.root_path.rglob("*.py"):
            try:
                content = py_file.read_text()
                # Find function definitions
                for match in re.finditer(r'def\s+(\w+)', content):
                    func_name = match.group(1)
                    if not func_name.startswith('_'):
                        function_names[func_name].append(str(py_file))
            except:
                pass
        
        # Count potential duplicates
        duplicates = sum(1 for funcs in function_names.values() if len(funcs) > 1)
        
        return duplicates
    
    def _load_historical_data(self) -> Dict[str, Any]:
        """Load historical prediction accuracy"""
        
        # In production, this would load from a database
        # For now, return empty dict
        return {
            "predictions_made": 0,
            "predictions_correct": 0,
            "accuracy": 0.0
        }
    
    def generate_predictions_report(self) -> str:
        """Generate human-readable predictions report"""
        
        bug_predictions = self.predict_bugs()
        perf_predictions = self.predict_performance()
        scalability_prediction = self.predict_scalability()
        
        report = f"""
🔮 Predictive Analytics Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

🐛 Bug Predictions ({len(bug_predictions)})
"""
        
        for pred in bug_predictions[:10]:
            report += f"\n  {pred.get('severity', 'unknown').upper()} [{pred.get('confidence', 0):.0%}] {pred['prediction']}"
            report += f"\n     File: {pred.get('file', 'unknown')}"
            report += f"\n     Fix: {pred.get('suggestion', 'N/A')}\n"
        
        report += f"\n⚡ Performance Predictions ({len(perf_predictions)})\n"
        
        for pred in perf_predictions[:10]:
            report += f"\n  {pred.get('severity', 'unknown').upper()} [{pred.get('confidence', 0):.0%}] {pred['prediction']}"
            report += f"\n     File: {pred.get('file', 'unknown')}:{pred.get('line', '?')}"
            report += f"\n     Fix: {pred.get('suggestion', 'N/A')}\n"
        
        report += f"\n📈 Scalability Prediction\n"
        report += f"\n  Confidence: {scalability_prediction['confidence']:.0%}\n"
        
        for pred in scalability_prediction.get('predictions', []):
            report += f"\n  {pred['severity'].upper()} {pred['issue']}"
            report += f"\n  Reason: {pred['reason']}\n"
        
        report += f"\n  💡 Recommendations:\n"
        for rec in scalability_prediction.get('recommendations', []):
            report += f"  • {rec}\n"
        
        return report


# Singleton instance
_predictive_analytics = None

def get_predictive_analytics(root_path: str = "."):
    """Get predictive analytics instance"""
    global _predictive_analytics
    if _predictive_analytics is None:
        _predictive_analytics = PredictiveAnalytics(root_path)
    return _predictive_analytics
