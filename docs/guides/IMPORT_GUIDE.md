# 📦 How to Import and Use CogOS in Your Projects

## Installation

### Option 1: Install from Local Directory
```bash
cd /home/corbybender/Projects/cog
pip install -e .
```

### Option 2: Install Directly
```bash
pip install -e /home/corbybender/Projects/cog
```

This makes `cog` available as an importable package anywhere on your system.

---

## 🚀 Basic Usage in Your Projects

### Example 1: Simple Import and Use

```python
# your_project/main.py
import asyncio
from cog.cogos import create_cogos
from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache


async def solve_problem():
    # Initialize CogOS
    llm = LLMProvider()
    memory = MemoryBackend(db_path=":memory:")
    cache = SmartCache(max_size=1000, ttl_seconds=3600)
    cogos = create_cogos(llm, memory, cache, enable_all=True)

    # Solve a complex problem
    result = await cogos.solve_complex_problem(
        problem="How should I design a scalable microservices architecture?",
        approach="comprehensive"
    )

    if result['success']:
        print("Solution:", result['solution'])
        print("Confidence:", result['validation']['confidence'])
        return result['solution']
    else:
        print("Error:", result['error'])
        return None


if __name__ == "__main__":
    solution = asyncio.run(solve_problem())
```

### Example 2: Using with Existing Project

```python
# your_project/ai_helper.py
import asyncio
from pathlib import Path
from cog.cogos import create_cogos


class CogOSHelper:
    """Helper class to use CogOS in your project"""

    def __init__(self):
        # Initialize CogOS once
        from cog.llm.provider import LLMProvider
        from cog.memory.backend import MemoryBackend
        from cog.cache.smart_cache import SmartCache

        self.llm = LLMProvider()
        self.memory = MemoryBackend(db_path=Path("cog_memory.db"))
        self.cache = SmartCache(max_size=1000, ttl_seconds=3600)
        self.cogos = create_cogos(
            self.llm,
            self.memory,
            self.cache,
            enable_all=True
        )

    async def design_system(self, requirements: str) -> dict:
        """Design a system based on requirements"""
        result = await self.cogos.solve_complex_problem(
            problem=f"Design a system with these requirements: {requirements}",
            approach="collaborative"
        )
        return result

    async def write_docs(self, title: str, topic: str) -> str:
        """Generate documentation"""
        from cog.document_writer import DocumentType

        result = await self.cogos.write_comprehensive_document(
            title=title,
            topic=topic,
            doc_type=DocumentType.TECHNICAL_REPORT,
            collaborative=True
        )
        return result.get('markdown', '')

    async def debug_issue(self, issue_description: str) -> dict:
        """Debug an issue using research and analysis"""
        result = await self.cogos.solve_complex_problem(
            problem=f"Debug this issue: {issue_description}",
            approach="researched"
        )
        return result

    async def create_plan(self, goal: str) -> dict:
        """Create an execution plan"""
        result = await self.cogos.solve_complex_problem(
            problem=goal,
            approach="planned"
        )
        return result


# Usage in your project
async def main():
    helper = CogOSHelper()

    # Design a system
    design = await helper.design_system(
        "Real-time collaboration platform with 10k concurrent users"
    )
    print("Design:", design['solution'])

    # Write documentation
    docs = await helper.write_docs(
        "API Reference",
        "REST API endpoints for user management"
    )
    print("Docs:", docs[:500])

    # Debug an issue
    debug = await helper.debug_issue(
        "Database connection timeout after 30 seconds under load"
    )
    print("Debug:", debug['solution'])


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🤖 How to Get an AI Agent to Use CogOS

### Approach 1: Wrapper Agent (Recommended)

Create an AI agent that uses CogOS as a tool:

```python
# your_project/agent_with_cogos.py
import asyncio
from typing import Dict, Any
from cog.cogos import create_cogos


class AIAgentWithCogOS:
    """
    An AI agent that uses CogOS for complex problem-solving

    This agent can:
    - Decide when to use CogOS
    - Delegate complex tasks to CogOS
    - Use CogOS results in its responses
    """

    def __init__(self):
        # Initialize CogOS
        from cog.llm.provider import LLMProvider
        from cog.memory.backend import MemoryBackend
        from cog.cache.smart_cache import SmartCache

        self.llm = LLMProvider()
        self.memory = MemoryBackend()
        self.cache = SmartCache()
        self.cogos = create_cogos(self.llm, self.memory, self.cache)

        # Agent state
        self.conversation_history = []
        self.task_queue = []

    async def process_message(self, user_message: str) -> str:
        """Process a user message using CogOS when needed"""

        # Step 1: Analyze the message
        analysis = await self._analyze_message(user_message)

        # Step 2: Decide if CogOS is needed
        if analysis['needs_cogos']:
            # Step 3: Use CogOS to solve
            cogos_result = await self._use_cogos(
                user_message,
                analysis['approach']
            )

            # Step 4: Format CogOS result for user
            response = self._format_cogos_result(cogos_result)
        else:
            # Handle with simple LLM call
            response = await self._simple_response(user_message)

        # Store in history
        self.conversation_history.append({
            "user": user_message,
            "agent": response,
            "used_cogos": analysis['needs_cogos']
        })

        return response

    async def _analyze_message(self, message: str) -> Dict[str, Any]:
        """Analyze message to determine if CogOS is needed"""

        # Simple heuristics (can be improved with LLM)
        complex_indicators = [
            "design", "architecture", "implement", "build",
            "plan", "debug", "optimize", "research"
        ]

        needs_cogos = any(
            indicator in message.lower()
            for indicator in complex_indicators
        )

        # Determine best approach
        if "design" in message.lower() or "architecture" in message.lower():
            approach = "collaborative"
        elif "implement" in message.lower() or "build" in message.lower():
            approach = "planned"
        elif "debug" in message.lower():
            approach = "researched"
        else:
            approach = "auto"

        return {
            "needs_cogos": needs_cogos,
            "approach": approach,
            "complexity": "high" if needs_cogos else "low"
        }

    async def _use_cogos(self, problem: str, approach: str) -> Dict[str, Any]:
        """Delegate problem to CogOS"""
        result = await self.cogos.solve_complex_problem(
            problem=problem,
            approach=approach
        )
        return result

    async def _simple_response(self, message: str) -> str:
        """Generate simple response without CogOS"""
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": message}
        ]

        response = await self.llm.generate(
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        return response.content

    def _format_cogos_result(self, result: Dict[str, Any]) -> str:
        """Format CogOS result for user"""

        if not result.get('success'):
            return f"I encountered an error: {result.get('error')}"

        # Build response
        parts = []

        # Add solution
        if result.get('solution'):
            parts.append("## Solution\n")
            parts.append(result['solution'])

        # Add validation info
        validation = result.get('validation', {})
        if validation:
            confidence = validation.get('confidence', 0)
            parts.append(f"\n## Confidence\n{confidence:.1%}")

            issues = validation.get('issues', [])
            if issues:
                parts.append("\n## Notes")
                parts.extend(f"- {issue}" for issue in issues)

        # Add stages if verbose
        if result.get('stages'):
            parts.append("\n## Process")
            for i, stage in enumerate(result['stages'], 1):
                stage_name = stage.get('stage', 'unknown')
                parts.append(f"{i}. {stage_name.replace('_', ' ').title()}")

        return "\n".join(parts)


# Usage example
async def main():
    # Create agent
    agent = AIAgentWithCogOS()

    # Test messages
    messages = [
        "What is Python?",  # Simple - won't use CogOS
        "Design a scalable microservices architecture for an e-commerce platform",  # Complex - uses CogOS
        "How do I fix a database connection timeout?",  # Debug - uses CogOS
        "Write documentation for a REST API",  # Complex - uses CogOS
    ]

    for msg in messages:
        print(f"\n{'='*80}")
        print(f"User: {msg}")
        print(f"{'='*80}")

        response = await agent.process_message(msg)
        print(f"\nAgent:\n{response}\n")


if __name__ == "__main__":
    asyncio.run(main())
```

### Approach 2: CogOS as a Tool

```python
# your_project/agent_tools.py
import asyncio
from typing import Optional


class CogOSTool:
    """
    CogOS as a tool that can be called by any AI agent
    """

    def __init__(self):
        from cog.cogos import create_cogos
        from cog.llm.provider import LLMProvider
        from cog.memory.backend import MemoryBackend
        from cog.cache.smart_cache import SmartCache

        self.cogos = create_cogos(
            LLMProvider(),
            MemoryBackend(),
            SmartCache()
        )

    async def solve(
        self,
        problem: str,
        approach: str = "auto",
        context: str = ""
    ) -> dict:
        """
        Solve a complex problem using CogOS

        This can be called by any AI agent as a tool.
        """
        result = await self.cogos.solve_complex_problem(
            problem=problem,
            context=context,
            approach=approach
        )

        return {
            "success": result.get("success", False),
            "solution": result.get("solution", ""),
            "confidence": result.get("validation", {}).get("confidence", 0),
            "stages": len(result.get("stages", [])),
            "error": result.get("error")
        }

    async def research(self, question: str, max_results: int = 10) -> dict:
        """Research a question"""
        from cog.research import Researcher, ResearchSource

        researcher = Researcher(
            self.cogos.llm,
            self.cogos.memory,
            self.cogos.cache
        )

        query = await researcher.research(
            question=question,
            sources=[
                ResearchSource.WEB_SEARCH,
                ResearchSource.CODEBASE,
                ResearchSource.DOCUMENTATION
            ],
            max_results=max_results
        )

        synthesis = await researcher.synthesize_findings(query)

        return {
            "question": question,
            "synthesis": synthesis,
            "results": len(query.results)
        }

    async def write_doc(
        self,
        title: str,
        topic: str,
        doc_type: str = "technical_report"
    ) -> dict:
        """Write a document"""
        from cog.document_writer import DocumentType

        type_map = {
            "technical_report": DocumentType.TECHNICAL_REPORT,
            "tutorial": DocumentType.TUTORIAL,
            "guide": DocumentType.GUIDE,
            "documentation": DocumentType.DOCUMENTATION
        }

        result = await self.cogos.write_comprehensive_document(
            title=title,
            topic=topic,
            doc_type=type_map.get(doc_type, DocumentType.TECHNICAL_REPORT),
            collaborative=True
        )

        return {
            "success": result.get("success", False),
            "title": title,
            "sections": len(result.get("document", {}).get("sections", [])),
            "markdown": result.get("markdown", ""),
            "error": result.get("error")
        }


# Example: Integration with LangChain-like agent
class ToolUsingAgent:
    """
    Example of an AI agent that can choose to use CogOS tools
    """

    def __init__(self):
        self.cogos_tool = CogOSTool()
        self.available_tools = {
            "cogos_solve": self.cogos_tool.solve,
            "cogos_research": self.cogos_tool.research,
            "cogos_write": self.cogos_tool.write_doc,
        }

    async def decide_and_act(self, user_input: str) -> str:
        """Decide which tool to use and act"""

        # Simple decision logic (in practice, use LLM)
        if "design" in user_input.lower() or "architecture" in user_input.lower():
            # Use CogOS solve
            result = await self.cogos_tool.solve(user_input)
            return f"I've designed a solution (confidence: {result['confidence']:.1%}):\n\n{result['solution']}"

        elif "research" in user_input.lower() or "find out" in user_input.lower():
            # Use CogOS research
            result = await self.cogos_tool.research(user_input)
            return f"Research findings:\n\n{result['synthesis']}"

        elif "write" in user_input.lower() or "document" in user_input.lower():
            # Use CogOS write
            # Extract title and topic (simplified)
            result = await self.cogos_tool.write_doc(
                title="Document",
                topic=user_input
            )
            return f"I've written a document with {result['sections']} sections"

        else:
            # Default response
            return "I can help you design systems, research topics, or write documentation. What would you like?"


async def main():
    agent = ToolUsingAgent()

    test_inputs = [
        "Design a microservices architecture",
        "Research the best practices for API authentication",
        "Write documentation for a REST API"
    ]

    for input_text in test_inputs:
        print(f"\n{'='*80}")
        print(f"User: {input_text}")
        print(f"{'='*80}")

        response = await agent.decide_and_act(input_text)
        print(f"\nAgent:\n{response}\n")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📁 Project Structure

```
your_project/
├── main.py                  # Your main entry point
├── ai_agent.py             # Your AI agent
├── cogos_helper.py         # CogOS wrapper/helper
├── requirements.txt        # Dependencies
└── ...
```

### requirements.txt
```
# Your project dependencies
cog  # This will install from your local /home/corbybender/Projects/cog
openai  # For LLM
aiohttp  # For async
python-dotenv  # For env vars
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
# CogOS Configuration
COGOS_LLM_PROVIDER=openai
COGOS_LLM_API_KEY=your_api_key_here
COGOS_LLM_MODEL=glm-5.1
COGOS_MEMORY_DB_PATH=./cog_memory.db
COGOS_CACHE_SIZE=1000
COGOS_ENABLE_MULTI_AGENT=true
COGOS_ENABLE_SELF_REFLECTION=true
COGOS_ENABLE_RESEARCH=true
```

### Load Config in Code
```python
import os
from dotenv import load_dotenv

load_dotenv()

from cog.cogos import CogOSConfig, CogOSSuperIntelligence
from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache

config = CogOSConfig(
    llm_provider=LLMProvider(),
    memory=MemoryBackend(db_path=os.getenv("COGOS_MEMORY_DB_PATH")),
    cache=SmartCache(
        max_size=int(os.getenv("COGOS_CACHE_SIZE", 1000)),
        ttl_seconds=3600
    ),
    enable_multi_agent=os.getenv("COGOS_ENABLE_MULTI_AGENT", "true").lower() == "true",
    enable_self_reflection=os.getenv("COGOS_ENABLE_SELF_REFLECTION", "true").lower() == "true",
    enable_research=os.getenv("COGOS_ENABLE_RESEARCH", "true").lower() == "true"
)

cogos = CogOSSuperIntelligence(config)
```

---

## 🎯 Real-World Examples

### Example 1: Code Review Agent
```python
class CodeReviewAgent:
    """AI agent that uses CogOS for comprehensive code reviews"""

    def __init__(self):
        self.cogos_tool = CogOSTool()

    async def review_code(self, code: str, file_path: str) -> dict:
        # Use CogOS to analyze code
        result = await self.cogos_tool.solve(
            problem=f"Review this code for bugs, security issues, and improvements:\n\n{code}",
            context=f"File: {file_path}",
            approach="collaborative"  # Multiple perspectives
        )

        return result
```

### Example 2: Technical Writer Agent
```python
class TechnicalWriterAgent:
    """AI agent that uses CogOS to write technical docs"""

    def __init__(self):
        self.cogos_tool = CogOSTool()

    async def write_api_docs(self, api_spec: dict) -> str:
        # Extract info from spec
        title = api_spec.get("title", "API Reference")
        description = api_spec.get("description", "")

        # Use CogOS to write docs
        result = await self.cogos_tool.write_doc(
            title=title,
            topic=description,
            doc_type="documentation"
        )

        return result["markdown"]
```

### Example 3: System Design Agent
```python
class SystemDesignAgent:
    """AI agent that uses CogOS for system design"""

    def __init__(self):
        self.cogos_tool = CogOSTool()

    async def design_system(self, requirements: dict) -> dict:
        # Format requirements
        req_text = "\n".join(f"- {k}: {v}" for k, v in requirements.items())

        # Use CogOS to design
        result = await self.cogos_tool.solve(
            problem=f"Design a system with these requirements:\n{req_text}",
            approach="comprehensive"  # Use all capabilities
        )

        return result
```

---

## 🚀 Quick Start Template

Copy this template to get started:

```python
# your_project/main.py
import asyncio
from cog.cogos import create_cogos
from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache


async def main():
    # Initialize CogOS
    llm = LLMProvider()
    memory = MemoryBackend()
    cache = SmartCache()
    cogos = create_cogos(llm, memory, cache, enable_all=True)

    # Use CogOS
    result = await cogos.solve_complex_problem(
        problem="Your complex problem here",
        approach="comprehensive"
    )

    if result['success']:
        print("Solution:", result['solution'])
        print("Confidence:", result['validation']['confidence'])
    else:
        print("Error:", result['error'])


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📚 Summary

**To use CogOS in your project:**

1. **Install it**: `pip install -e /home/corbybender/Projects/cog`
2. **Import it**: `from cog.cogos import create_cogos`
3. **Initialize it**: `cogos = create_cogos(llm, memory, cache)`
4. **Use it**: `result = await cogos.solve_complex_problem(problem)`

**To get an AI agent to use CogOS:**

1. **Create a wrapper class** that initializes CogOS
2. **Add methods** that delegate to CogOS
3. **Let your agent decide** when to use CogOS based on complexity
4. **Format results** for your users

That's it! You now have super-intelligent capabilities in your projects! 🚀
