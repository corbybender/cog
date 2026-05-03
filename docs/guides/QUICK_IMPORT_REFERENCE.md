# 🚀 Quick Reference: Importing and Using CogOS

## Installation (One-Time Setup)

```bash
# From CogOS directory
cd /home/corbybender/Projects/cog
pip install -e .

# Now you can import cog from anywhere!
```

## Basic Import Pattern

```python
# import cog
from cog.cogos import create_cogos
from cog.llm.provider import LLMProvider
from cog.memory.backend import MemoryBackend
from cog.cache.smart_cache import SmartCache

# Initialize
llm = LLMProvider()
memory = MemoryBackend()
cache = SmartCache()
cogos = create_cogos(llm, memory, cache, enable_all=True)

# Use
result = await cogos.solve_complex_problem("Your problem")
```

## Common Patterns

### Pattern 1: Simple Helper Class
```python
class CogOSHelper:
    def __init__(self):
        self.cogos = create_cogos(LLMProvider(), MemoryBackend(), SmartCache())

    async def solve(self, problem: str) -> dict:
        return await self.cogos.solve_complex_problem(problem)
```

### Pattern 2: AI Agent with CogOS
```python
class AIAgent:
    def __init__(self):
        self.cogos = create_cogos(LLMProvider(), MemoryBackend(), SmartCache())

    async def process(self, message: str) -> str:
        # Decide if CogOS is needed
        if self.is_complex(message):
            result = await self.cogos.solve_complex_problem(message)
            return result['solution']
        else:
            return await self.simple_response(message)
```

### Pattern 3: CogOS as Tool
```python
class CogOSTool:
    async def solve(self, problem: str) -> dict:
        result = await self.cogos.solve_complex_problem(problem)
        return {"solution": result['solution'], "confidence": result['validation']['confidence']}
```

## Real-World Examples

### Example 1: Code Review Assistant
```python
from cog.cogos import create_cogos

class CodeReviewer:
    def __init__(self):
        self.cogos = create_cogos(LLMProvider(), MemoryBackend(), SmartCache())

    async def review(self, code: str) -> dict:
        result = await self.cogos.solve_complex_problem(
            problem=f"Review this code:\n\n{code}",
            approach="collaborative"  # Multiple agents review
        )
        return result
```

### Example 2: Documentation Writer
```python
from cog.cogos import create_cogos
from cog.document_writer import DocumentType

class DocWriter:
    def __init__(self):
        self.cogos = create_cogos(LLMProvider(), MemoryBackend(), SmartCache())

    async def write_api_docs(self, api_spec: dict) -> str:
        result = await self.cogos.write_comprehensive_document(
            title=api_spec['title'],
            topic=api_spec['description'],
            doc_type=DocumentType.DOCUMENTATION,
            collaborative=True
        )
        return result['markdown']
```

### Example 3: System Designer
```python
from cog.cogos import create_cogos

class SystemDesigner:
    def __init__(self):
        self.cogos = create_cogos(LLMProvider(), MemoryBackend(), SmartCache())

    async def design(self, requirements: dict) -> dict:
        req_text = "\n".join(f"{k}: {v}" for k, v in requirements.items())
        result = await self.cogos.solve_complex_problem(
            problem=f"Design system:\n{req_text}",
            approach="comprehensive"
        )
        return result
```

## CLI Usage

```bash
# Solve problems
cogos solve "Your complex problem"

# Write documents
cogos write "Title" "Topic" --collaborative --output doc.md

# Research
cogos research "Your question" --sources web codebase

# Create plans
cogos plan "Your goal" --output plan.json

# Interactive demo
python cog/examples/ai_agent_example.py
```

## Environment Setup

Create `.env` file:
```bash
COGOS_LLM_API_KEY=your_key_here
COGOS_MEMORY_DB_PATH=./cog_memory.db
COGOS_ENABLE_MULTI_AGENT=true
COGOS_ENABLE_SELF_REFLECTION=true
```

Load in code:
```python
from dotenv import load_dotenv
load_dotenv()
```

## That's It!

You now have:
- ✅ CogOS installed as a package
- ✅ Can import it anywhere
- ✅ Multiple integration patterns
- ✅ Real-world examples
- ✅ CLI tools ready to use

**Start building super-intelligent applications!** 🚀
