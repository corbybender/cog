"""
CogOS Enhanced Self-Improvement System
Extracts learnings, generates improvements, maintains knowledge base
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import asyncio

class EnhancedSelfImprovementEngine:
    """Advanced self-improvement with knowledge base and automatic code generation"""
    
    def __init__(self, knowledge_base_path: str = "cog/knowledge_base"):
        self.kb_path = Path(knowledge_base_path)
        self.kb_path.mkdir(parents=True, exist_ok=True)
        
        self.patterns_db = self._load_patterns_db()
        self.improvements_log = self._load_improvements_log()
        self.success_metrics = self._load_success_metrics()
        
    def _load_patterns_db(self) -> Dict[str, Any]:
        """Load patterns database"""
        db_path = self.kb_path / "patterns.json"
        if db_path.exists():
            return json.loads(db_path.read_text())
        return {
            "common_issues": {},
            "successful_patterns": {},
            "anti_patterns": {}
        }
    
    def _load_improvements_log(self) -> List[Dict[str, Any]]:
        """Load improvements history"""
        log_path = self.kb_path / "improvements.jsonl"
        if log_path.exists():
            return [json.loads(line) for line in log_path.read_text().split("\n") if line.strip()]
        return []
    
    def _load_success_metrics(self) -> Dict[str, Any]:
        """Load success metrics for pattern evaluation"""
        metrics_path = self.kb_path / "metrics.json"
        if metrics_path.exists():
            return json.loads(metrics_path.read_text())
        return {}
    
    async def analyze_task_execution(self, task: str, execution: Dict[str, Any], result: Any) -> Dict[str, Any]:
        """Analyze task execution and extract learnings"""
        
        analysis = {
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "patterns_found": [],
            "issues_detected": [],
            "successful_approaches": [],
            "learnings": [],
            "improvements_generated": []
        }
        
        # Extract patterns from execution
        patterns = self._extract_patterns(execution)
        analysis["patterns_found"] = patterns
        
        # Detect common issues
        issues = self._detect_issues(execution, result)
        analysis["issues_detected"] = issues
        
        # Identify successful approaches
        successes = self._identify_successes(execution, result)
        analysis["successful_approaches"] = successes
        
        # Generate learnings
        learnings = self._generate_learnings(patterns, issues, successes)
        analysis["learnings"] = learnings
        
        # Generate automatic improvements
        improvements = await self._generate_improvements(issues, learnings)
        analysis["improvements_generated"] = improvements
        
        # Store in knowledge base
        await self._store_analysis(analysis)
        
        return analysis
    
    def _extract_patterns(self, execution: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract recurring patterns from execution"""
        patterns = []
        
        # Agent interaction patterns
        if "agent_sequence" in execution:
            agent_pattern = self._analyze_agent_sequence(execution["agent_sequence"])
            if agent_pattern:
                patterns.append(agent_pattern)
        
        # Module usage patterns
        if "modules_used" in execution:
            module_pattern = self._analyze_module_usage(execution["modules_used"])
            if module_pattern:
                patterns.append(module_pattern)
        
        # Code generation patterns
        if "generated_code" in execution:
            code_pattern = self._analyze_code_patterns(execution["generated_code"])
            if code_pattern:
                patterns.append(code_pattern)
        
        return patterns
    
    def _detect_issues(self, execution: Dict[str, Any], result: Any) -> List[Dict[str, Any]]:
        """Detect issues and problems"""
        issues = []
        
        # Check for errors
        if "errors" in execution and execution["errors"]:
            for error in execution["errors"]:
                issue = {
                    "type": "error",
                    "description": error,
                    "severity": "high",
                    "pattern": self._classify_error(error),
                    "suggested_fix": self._suggest_fix(error)
                }
                issues.append(issue)
        
        # Check for inefficiencies
        inefficiencies = self._detect_inefficiencies(execution)
        issues.extend(inefficiencies)
        
        # Check for quality issues
        quality_issues = self._detect_quality_issues(execution, result)
        issues.extend(quality_issues)
        
        return issues
    
    def _identify_successes(self, execution: Dict[str, Any], result: Any) -> List[Dict[str, Any]]:
        """Identify successful approaches"""
        successes = []
        
        # High-quality outputs
        if self._is_high_quality(result):
            successes.append({
                "type": "quality",
                "description": "High quality output generated",
                "pattern": self._extract_success_pattern(execution)
            })
        
        # Efficient execution
        if self._is_efficient(execution):
            successes.append({
                "type": "efficiency",
                "description": "Efficient execution",
                "metrics": self._get_efficiency_metrics(execution)
            })
        
        # Novel solutions
        if self._is_novel(execution):
            successes.append({
                "type": "innovation",
                "description": "Novel approach",
                "pattern": self._extract_novel_pattern(execution)
            })
        
        return successes
    
    def _generate_learnings(self, patterns: List, issues: List, successes: List) -> List[Dict[str, Any]]:
        """Generate learnings from analysis"""
        learnings = []
        
        # Learn from issues
        for issue in issues:
            if issue.get("pattern"):
                learning = {
                    "type": "avoid",
                    "pattern": issue["pattern"],
                    "description": f"Avoid: {issue['description']}",
                    "suggestion": issue.get("suggested_fix", ""),
                    "confidence": 0.8
                }
                learnings.append(learning)
        
        # Learn from successes
        for success in successes:
            if success.get("pattern"):
                learning = {
                    "type": "adopt",
                    "pattern": success["pattern"],
                    "description": f"Adopt: {success['description']}",
                    "confidence": 0.9
                }
                learnings.append(learning)
        
        return learnings
    
    async def _generate_improvements(self, issues: List, learnings: List) -> List[Dict[str, Any]]:
        """Generate automatic improvements"""
        improvements = []
        
        # Generate code improvements
        for issue in issues:
            if issue["type"] == "error" or issue["severity"] == "high":
                improvement = await self._generate_code_improvement(issue)
                if improvement:
                    improvements.append(improvement)
        
        # Generate pattern improvements
        for learning in learnings:
            if learning["confidence"] > 0.8:
                improvement = self._generate_pattern_improvement(learning)
                if improvement:
                    improvements.append(improvement)
        
        return improvements
    
    async def _generate_code_improvement(self, issue: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate automatic code improvement for an issue"""
        improvement = {
            "type": "code_fix",
            "issue": issue["description"],
            "pattern": issue.get("pattern", ""),
            "suggested_code": self._generate_fix_code(issue),
            "explanation": issue.get("suggested_fix", ""),
            "confidence": 0.7,
            "auto_applicable": True
        }
        return improvement
    
    def _generate_pattern_improvement(self, learning: Dict[str, Any]) -> Dict[str, Any]:
        """Generate pattern-based improvement"""
        improvement = {
            "type": "pattern_update",
            "pattern": learning["pattern"],
            "action": "adopt" if learning["type"] == "adopt" else "avoid",
            "description": learning["description"],
            "confidence": learning["confidence"]
        }
        return improvement
    
    async def _store_analysis(self, analysis: Dict[str, Any]):
        """Store analysis in knowledge base"""
        # Update patterns database
        for pattern in analysis["patterns_found"]:
            pattern_hash = hashlib.md5(json.dumps(pattern, sort_keys=True).encode()).hexdigest()
            self.patterns_db["successful_patterns"][pattern_hash] = {
                "pattern": pattern,
                "occurrences": self.patterns_db["successful_patterns"].get(pattern_hash, {}).get("occurrences", 0) + 1,
                "last_seen": datetime.now().isoformat()
            }
        
        # Store issues
        for issue in analysis["issues_detected"]:
            if issue.get("pattern"):
                issue_hash = hashlib.md5(json.dumps(issue["pattern"], sort_keys=True).encode()).hexdigest()
                self.patterns_db["common_issues"][issue_hash] = {
                    "pattern": issue["pattern"],
                    "occurrences": self.patterns_db["common_issues"].get(issue_hash, {}).get("occurrences", 0) + 1,
                    "last_seen": datetime.now().isoformat()
                }
        
        # Save to disk
        (self.kb_path / "patterns.json").write_text(json.dumps(self.patterns_db, indent=2))
        
        # Append to improvements log
        self.improvements_log.append(analysis)
        with open(self.kb_path / "improvements.jsonl", "a") as f:
            f.write(json.dumps(analysis) + "\n")
    
    def get_relevant_learnings(self, task: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get learnings relevant to current task"""
        # Simple similarity matching (can be enhanced with embeddings)
        relevant = []
        
        task_lower = task.lower()
        
        for learning in self.improvements_log:
            # Check if task mentions similar concepts
            for pattern in learning.get("patterns_found", []):
                if any(keyword in task_lower for keyword in str(pattern).lower().split()):
                    relevant.append(learning)
                    break
        
        # Sort by relevance and confidence
        relevant.sort(key=lambda x: len(x.get("learnings", [])), reverse=True)
        
        return relevant[:5]  # Return top 5
    
    def get_best_practices(self, domain: str) -> List[Dict[str, Any]]:
        """Get best practices for a domain"""
        practices = []
        
        # Extract from successful patterns
        for pattern_hash, pattern_data in self.patterns_db["successful_patterns"].items():
            if domain.lower() in str(pattern_data["pattern"]).lower():
                practices.append({
                    "pattern": pattern_data["pattern"],
                    "usage_count": pattern_data["occurrences"],
                    "last_seen": pattern_data["last_seen"]
                })
        
        # Sort by usage
        practices.sort(key=lambda x: x["usage_count"], reverse=True)
        
        return practices
    
    async def auto_improve(self, code: str, context: Dict[str, Any]) -> str:
        """Automatically improve code based on knowledge base"""
        improved_code = code
        
        # Get relevant learnings
        relevant_learnings = self.get_relevant_learnings(context.get("task", ""), context)
        
        # Apply improvements
        for learning in relevant_learnings:
            for improvement in learning.get("improvements_generated", []):
                if improvement.get("auto_applicable"):
                    # Apply the improvement
                    improved_code = self._apply_improvement(improved_code, improvement)
        
        return improved_code
    
    def _apply_improvement(self, code: str, improvement: Dict[str, Any]) -> str:
        """Apply an improvement to code"""
        # This would contain actual code transformation logic
        # For now, return original code
        return code
    
    def _classify_error(self, error: str) -> str:
        """Classify error type"""
        error_lower = error.lower()
        
        if "syntax" in error_lower:
            return "syntax_error"
        elif "import" in error_lower:
            return "import_error"
        elif "type" in error_lower:
            return "type_error"
        elif "name" in error_lower:
            return "name_error"
        elif "attribute" in error_lower:
            return "attribute_error"
        else:
            return "unknown_error"
    
    def _suggest_fix(self, error: str) -> str:
        """Suggest fix for error"""
        error_type = self._classify_error(error)
        
        fixes = {
            "syntax_error": "Check for missing parentheses, brackets, or quotes",
            "import_error": "Verify the module is installed and import path is correct",
            "type_error": "Check variable types and use appropriate type conversions",
            "name_error": "Ensure variable is defined before use",
            "attribute_error": "Verify the object has the specified attribute or method"
        }
        
        return fixes.get(error_type, "Review the error message and code logic")
    
    def _detect_inefficiencies(self, execution: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect performance inefficiencies"""
        inefficiencies = []
        
        if "tokens_used" in execution:
            # Check if excessive tokens used
            if execution["tokens_used"] > 10000:
                inefficiencies.append({
                    "type": "performance",
                    "description": f"High token usage: {execution['tokens_used']}",
                    "severity": "medium",
                    "suggestion": "Consider breaking into smaller tasks or using caching"
                })
        
        return inefficiencies
    
    def _detect_quality_issues(self, execution: Dict[str, Any], result: Any) -> List[Dict[str, Any]]:
        """Detect code quality issues"""
        issues = []
        
        # Check for common quality issues
        if "generated_code" in execution:
            code = execution["generated_code"]
            
            # Check for code smells
            if len(code.split("\n")) < 5:
                issues.append({
                    "type": "quality",
                    "description": "Very short code - may lack proper error handling or documentation",
                    "severity": "low"
                })
        
        return issues
    
    def _is_high_quality(self, result: Any) -> bool:
        """Check if result is high quality"""
        # Simple heuristic - can be enhanced
        if isinstance(result, dict):
            return result.get("quality_score", 0) > 0.8
        return True
    
    def _is_efficient(self, execution: Dict[str, Any]) -> bool:
        """Check if execution was efficient"""
        if "tokens_used" in execution:
            return execution["tokens_used"] < 5000
        return True
    
    def _is_novel(self, execution: Dict[str, Any]) -> bool:
        """Check if approach is novel"""
        # Simple heuristic - check if uses unique combination of modules
        if "modules_used" in execution:
            return len(execution["modules_used"]) > 3
        return False
    
    def _analyze_agent_sequence(self, sequence: List[str]) -> Optional[Dict[str, Any]]:
        """Analyze agent interaction pattern"""
        if not sequence or len(sequence) < 2:
            return None
        
        return {
            "type": "agent_sequence",
            "pattern": "->".join(sequence),
            "length": len(sequence)
        }
    
    def _analyze_module_usage(self, modules: List[str]) -> Optional[Dict[str, Any]]:
        """Analyze module usage pattern"""
        if not modules:
            return None
        
        return {
            "type": "module_usage",
            "modules": modules,
            "count": len(modules)
        }
    
    def _analyze_code_patterns(self, code: str) -> Optional[Dict[str, Any]]:
        """Analyze code generation patterns"""
        if not code:
            return None
        
        return {
            "type": "code_pattern",
            "language": self._detect_language(code),
            "lines": len(code.split("\n"))
        }
    
    def _detect_language(self, code: str) -> str:
        """Detect programming language from code"""
        if "def " in code or "import " in code:
            return "python"
        elif "function" in code or "const " in code:
            return "javascript"
        elif "struct " in code or "func " in code:
            return "go"
        else:
            return "unknown"
    
    def _generate_fix_code(self, issue: Dict[str, Any]) -> str:
        """Generate code fix for issue"""
        # This would generate actual fix code
        return "# Suggested fix based on pattern analysis"
    
    def _extract_success_pattern(self, execution: Dict[str, Any]) -> Dict[str, Any]:
        """Extract pattern from successful execution"""
        return {
            "agents": execution.get("agent_sequence", []),
            "modules": execution.get("modules_used", []),
            "approach": execution.get("strategy", "unknown")
        }
    
    def _extract_novel_pattern(self, execution: Dict[str, Any]) -> Dict[str, Any]:
        """Extract novel pattern"""
        return {
            "unique_combination": execution.get("modules_used", []),
            "innovation": execution.get("novel_approach", "")
        }
    
    def _get_efficiency_metrics(self, execution: Dict[str, Any]) -> Dict[str, Any]:
        """Get efficiency metrics"""
        return {
            "tokens": execution.get("tokens_used", 0),
            "time": execution.get("execution_time", 0),
            "agents": len(execution.get("agent_sequence", []))
        }

# Global instance
_enhanced_improvement = None

def get_enhanced_improvement_engine():
    """Get global enhanced improvement engine instance"""
    global _enhanced_improvement
    if _enhanced_improvement is None:
        _enhanced_improvement = EnhancedSelfImprovementEngine()
    return _enhanced_improvement
