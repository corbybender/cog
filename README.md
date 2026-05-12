# CogOS - Modular Cognitive Runtime System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11%2B-green.svg)](https://www.python.org/downloads/)
[![Modules](https://img.shields.io/badge/Modules-38-purple.svg)](https://github.com/corbybender/cog#modules)
[![Free](https://img.shields.io/badge/Price-Free-success.svg)](https://github.com/corbybender/cog)

**A modular cognitive runtime with expert modules, web UI, and multi-agent collaboration. Free, open source, runs locally.**

[Quick Start](#quick-start) • [Web UI](#web-ui) • [Live Site](https://cogos.vercel.app) • [Docs](#documentation) • [Modules](#modules)

---

## What is CogOS?

CogOS is a **modular cognitive runtime** that enhances any LLM with:

- **38 Domain Modules** - Prompt extensions, tools, and verifiers for Python, JavaScript, AWS, Docker, Kubernetes, and more
- **Multi-Agent Orchestration** - Specialized agents that collaborate on complex tasks (planner, researcher, coder, reviewer, tester, critic, documenter, optimizer, security, architect)
- **Built-in Tools** - Filesystem operations, shell execution, web fetching/search, plus 60+ module-contributed tools
- **Caching** - Response and tool-result caching to reduce token usage
- **Memory** - SQLite or Mem0-backed conversation and task memory
- **Approval Gates** - Require user approval for destructive operations
- **Web UI** - Optional dashboard for task management and analytics

---

## Quick Start

### Install

```bash
git clone https://github.com/corbybender/cog.git
cd cog
pip install -e .
cog init
```

That's it. `cog init` registers CogOS as an MCP server with your AI tools (Claude Code, Codex CLI, Gemini CLI). They discover it automatically — no config files to edit, no instructions to paste.

### How it works

After `cog init`, your AI tool sees CogOS tools automatically:

| MCP Tool | What it does |
|----------|-------------|
| `cog_run` | Run a cognitive task with multi-agent orchestration |
| `cog_chat` | Interactive conversation with CogOS |
| `cog_status` | Show active modules, tools, provider info |
| `cog_modules` | List available domain modules |

Your AI can now call these directly. CogOS uses whatever LLM provider your environment already has (OpenAI, Anthropic, DeepSeek, etc.) — no duplicate API keys.

### CLI commands

```bash
cog init                        # register CogOS as MCP server
cog register                    # re-register with AI tools
cog mcp                         # run the MCP server directly
cog run "your task here"        # run a cognitive task
cog chat                        # interactive chat
cog status                      # show modules, tools, provider info
```

### Advanced: Provider Configuration

<details>
<summary>Click to expand all provider options</summary>

**Pass-through** — for tool builders embedding CogOS:

```python
from cog import CogOS
from cog.providers.openai_provider import OpenAIProvider

provider = OpenAIProvider(model="gpt-4o", api_key="sk-...")
cog = CogOS(provider=provider)
```

**String-based** — for quick scripts:

```python
cog = CogOS(llm="gpt-4o", api_key="sk-...")
cog = CogOS(llm="claude-sonnet-4-20250514", api_key="sk-ant-...")
cog = CogOS(llm="deepseek-chat", api_key="...", base_url="https://api.deepseek.com/v1")
```

**Config file** — for project-level settings:

```bash
cog init   # creates cog.yaml
```

```yaml
# cog.yaml (gitignored by default)
provider: openai
model: gpt-4o
api_key: sk-...
base_url: null          # optional, for custom endpoints
```

**Environment variables** — full list:

| Variable | Purpose |
|----------|---------|
| `COG_PROVIDER` | Override provider (openai, anthropic) |
| `COG_MODEL` | Override model name |
| `COG_API_KEY` | API key (any provider) |
| `COG_BASE_URL` | Custom endpoint URL |
| `OPENAI_API_KEY` | Auto-detected, sets provider=openai |
| `ANTHROPIC_API_KEY` | Auto-detected, sets provider=anthropic |
| `OPENAI_BASE_URL` | Custom OpenAI endpoint |

</details>

---

## Web UI

An optional local dashboard for task management, analytics, and module browsing.

### Start the Web UI

```bash
cd web-ui
./start.sh
# Opens http://localhost:8000
```

### Features

- Create and monitor tasks
- Browse available modules
- Track token usage and task completion
- Real-time WebSocket updates

See [web-ui/README.md](web-ui/README.md) for details.

---

## Modules

38 domain-specific modules with prompt extensions, tools, and verifiers:

### Programming Languages
- **JavaScript** - ES6+, Node.js, TypeScript
- **Python** - Django, Flask, FastAPI, data science
- **Java** - Spring Boot, Maven
- **C#** - .NET, ASP.NET
- **Ruby** - Rails, Sinatra
- **PHP** - Laravel, Symfony
- **Rust** - Memory safety, async
- **Go** - Concurrency, microservices
- **Swift** - iOS/macOS development
- **Kotlin** - Android, JVM

### Databases
- **PostgreSQL**, **MySQL**, **SQLite**, **Elasticsearch**, **Cassandra**

### Cloud Platforms
- **AWS** - EC2, S3, Lambda
- **Azure** - App Service, Functions
- **GCP** - Compute Engine, Cloud Run
- **DigitalOcean**, **Linode**

### Containers & Infrastructure
- **Docker** - Build, compose, optimization
- **Kubernetes** - Deployments, services

### Web & Frontend
- **CSS**, **HTML**
- **Vue**, **Angular**, **Svelte**

### API Styles
- **REST**, **GraphQL**, **gRPC**

### Testing
- **Playwright**, **Selenium**

### Operating Systems
- **Linux**, **macOS**, **Windows**

### Development Tools
- **70 Tools** - 7 built-in plus 63 from modules

---

## Multi-Agent System

10 specialized agent roles that can collaborate on tasks:

| Agent | Role |
|-------|------|
| Planner | Decompose complex tasks into steps |
| Researcher | Multi-source information gathering |
| Coder | Write production code |
| Reviewer | Review and critique code |
| Tester | Comprehensive testing strategies |
| Critic | Find flaws and propose alternatives |
| Documenter | Clear documentation |
| Optimizer | Performance optimization |
| Security | Security analysis |
| Architect | System design |

---

## Documentation

### Getting Started
- [Quick Start Guide](docs/START_HERE.md)
- [Configuration](docs/api/configuration.md)

### Architecture
- [Multi-Agent System](docs/architecture/multi_agent.md)
- [Module System](docs/architecture/modules.md)

### API Reference
- [Python API](docs/api/python.md)
- [CLI Reference](docs/api/cli.md)
- [Module API](docs/api/modules.md)

---

## Testing

```bash
pytest
```

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/corbybender/cog.git
cd cog
python -m venv venv
source venv/bin/activate
pip install -e .
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Support

- **GitHub Issues**: [github.com/corbybender/cog/issues](https://github.com/corbybender/cog/issues)
- **Documentation**: [docs/](docs/)
