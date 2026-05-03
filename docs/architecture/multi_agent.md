# Multi-Agent System

Comprehensive guide to CogOS's multi-agent orchestration system.

## Overview

CogOS uses 8 specialized AI agents that collaborate to produce superior results compared to single-pass LLMs.

## The 8 Agents

### 1. 🔬 Research Agent

Gathers information from multiple sources before task execution.

**Responsibilities:**
- Multi-source research (codebase, web, documentation)
- Best practices research
- Pattern identification
- Technology research

**When It Runs:**
- First in the agent pipeline
- Before complex tasks
- When domain expertise is needed

**Example:**
```python
from cogos.agents import ResearchAgent

agent = ResearchAgent()
result = agent.research("Docker best practices for Node.js microservices")
print(result.findings)
print(result.sources)
```

### 2. 💻 Code Agent

Writes production-ready code with best practices.

**Responsibilities:**
- Write clean, maintainable code
- Follow language/framework conventions
- Implement proper error handling
- Add type hints and documentation

**When It Runs:**
- After research completes
- For code-generation tasks
- When implementation is needed

**Example:**
```python
from cogos.agents import CodeAgent

agent = CodeAgent()
result = agent.write_code("Create a FastAPI endpoint with PostgreSQL")
print(result.code)
print(result.explanation)
```

### 3. 🧪 Test Agent

Creates comprehensive test suites.

**Responsibilities:**
- Generate unit tests
- Create integration tests
- Add edge case coverage
- Implement test fixtures

**When It Runs:**
- After code is generated
- For test-generation tasks
- When validation is needed

**Example:**
```python
from cogos.agents import TestAgent

agent = TestAgent()
result = agent.generate_tests(code_string, framework="pytest")
print(result.tests)
print(result.coverage_plan)
```

### 4. 📝 Document Agent

Writes clear documentation and comments.

**Responsibilities:**
- Generate API documentation
- Write code comments
- Create usage examples
- Document edge cases

**When It Runs:**
- After code and tests are complete
- For documentation tasks
- When clarity is needed

**Example:**
```python
from cogos.agents import DocumentAgent

agent = DocumentAgent()
result = agent.generate_docs(code_string)
print(result.documentation)
print(result.examples)
```

### 5. 🎨 Architect Agent

Designs system architecture and structure.

**Responsibilities:**
- Design system architecture
- Plan component structure
- Define interfaces
- Consider scalability

**When It Runs:**
- For complex system design tasks
- When architecture decisions are needed
- Before implementation

**Example:**
```python
from cogos.agents import ArchitectAgent

agent = ArchitectAgent()
result = agent.design_architecture("Design a microservices e-commerce platform")
print(result.architecture)
print(result.components)
```

### 6. 🔍 Critique Agent

Reviews code and identifies issues.

**Responsibilities:**
- Code review and quality analysis
- Identify potential bugs
- Suggest improvements
- Check for anti-patterns

**When It Runs:**
- After code is generated
- For review tasks
- Before finalization

**Example:**
```python
from cogos.agents import CritiqueAgent

agent = CritiqueAgent()
result = agent.critique(code_string)
print(result.issues)
print(result.suggestions)
print(result.score)
```

### 7. ✅ Validate Agent

Verifies requirements are met.

**Responsibilities:**
- Validate against requirements
- Check acceptance criteria
- Verify completeness
- Test functionality

**When It Runs:**
- After all agents complete
- For validation tasks
- Before final output

**Example:**
```python
from cogos.agents import ValidateAgent

agent = ValidateAgent()
result = agent.validate(
    code=code_string,
    requirements=requirements_list
)
print(result.passed)
print(result.issues)
```

### 8. ⚡ Optimize Agent

Optimizes for performance and cost.

**Responsibilities:**
- Performance optimization
- Cost reduction
- Efficiency improvements
- Resource optimization

**When It Runs:**
- After validation passes
- For optimization tasks
- Before final output

**Example:**
```python
from cogos.agents import OptimizeAgent

agent = OptimizeAgent()
result = agent.optimize(
    code=code_string,
    objective="performance"
)
print(result.optimized_code)
print(result.improvements)
```

---

## Agent Collaboration

### Debate and Voting

Agents collaborate through structured debate and voting:

1. **Initial Proposals** - Each agent proposes their solution
2. **Debate Phase** - Agents discuss and critique proposals
3. **Voting Phase** - Agents vote on best approach
4. **Consensus** - Final solution incorporates best ideas

### Example Workflow

```python
from cogos import CogOS

cogos = CogOS()
result = cogos.think("Build a REST API with user authentication")

# Behind the scenes:
# 1. Research Agent: Researches best practices for REST APIs
# 2. Architect Agent: Designs API structure
# 3. Code Agent: Implements the API
# 4. Test Agent: Generates tests
# 5. Document Agent: Writes documentation
# 6. Critique Agent: Reviews implementation
# 7. Validate Agent: Verifies requirements
# 8. Optimize Agent: Optimizes performance

print(result.summary)
print(result.code)
print(result.tests)
```

---

## Custom Agent Workflows

You can create custom agent workflows:

```python
from cogos import AgentWorkflow
from cogos.agents import (
    ResearchAgent, CodeAgent, TestAgent,
    DocumentAgent, CritiqueAgent
)

# Create custom workflow
workflow = AgentWorkflow()
workflow.add_agent("research", ResearchAgent())
workflow.add_agent("code", CodeAgent(), dependencies=["research"])
workflow.add_agent("test", TestAgent(), dependencies=["code"])
workflow.add_agent("critique", CritiqueAgent(), dependencies=["code"])
workflow.add_agent("document", DocumentAgent(), dependencies=["code"])

# Execute with custom workflow
cogos = CogOS(workflow=workflow)
result = cogos.think("Create a Python web scraper")
```

---

## Agent Configuration

### Configure Individual Agents

```python
from cogos import CogOS

cogos = CogOS(
    agent_config={
        "research": {
            "timeout": 120,
            "max_sources": 10
        },
        "code": {
            "language": "python",
            "style": "pep8"
        },
        "test": {
            "framework": "pytest",
            "coverage_target": 90
        }
    }
)
```

### Agent Timeout

```python
cogos = CogOS(
    agent_timeout=300,  # 5 minutes per agent
    max_agent_iterations=3
)
```

### Parallel Execution

```python
cogos = CogOS(
    enable_parallel_agents=True,
    max_concurrent_agents=4
)
```

---

## Agent Communication

### Message Passing

Agents communicate through structured messages:

```python
# Agent 1 sends message
message = {
    "from": "research",
    "to": "code",
    "content": "Use FastAPI framework for best performance"
}

# Agent 2 receives and acts
# ...
```

### Shared Context

Agents share a common context:

```python
context = {
    "task": "Build REST API",
    "research_findings": {...},
    "architecture": {...},
    "code": "...",
    "tests": "...",
    "documentation": "..."
}
```

---

## Best Practices

1. **Let Agents Collaborate** - Don't skip agents unnecessarily
2. **Provide Clear Tasks** - Ambiguous tasks reduce agent effectiveness
3. **Review Agent Output** - Agents make mistakes, review their work
4. **Use Appropriate Safety Levels** - Some agents need more supervision
5. **Configure Timeouts** - Prevent agents from running too long
6. **Enable Caching** - Reduce redundant agent work
7. **Monitor Performance** - Track which agents take longest

---

## Troubleshooting

### Agent Not Running

```python
# Check agent is enabled
cogos = CogOS(enabled_agents=["research", "code", "test"])

# Verify agent configuration
print(cogos.agent_config)
```

### Agent Timeout

```python
# Increase timeout
cogos = CogOS(agent_timeout=600)

# Or disable specific agent
cogos = CogOS(enabled_agents=["research", "code"])
```

### Poor Agent Collaboration

```python
# Enable debate phase
cogos = CogOS(enable_debate=True, debate_rounds=3)

# Increase iterations
cogos = CogOS(max_agent_iterations=5)
```

---

## Performance Tips

1. **Enable Caching** - Reduces redundant agent work
2. **Use Parallel Execution** - Run independent agents simultaneously
3. **Set Appropriate Timeouts** - Balance speed and quality
4. **Disable Unused Agents** - Skip agents you don't need
5. **Use Faster Models** - For less critical tasks

---

## Related Documentation

- [Super-Intelligence System](../architecture/README_SUPER_INTELLIGENCE.md)
- [Python API](../api/python.md)
- [Configuration](../api/configuration.md)

---

**Next:** [Module System](../api/modules.md)
