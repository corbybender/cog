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

### Installation

```bash
pip install -e .
```

Or for development:

```bash
git clone https://github.com/corbybender/cog.git
cd cog
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Configure Your AI Provider

CogOS requires an LLM provider — it doesn't ship with one. Pass yours in directly:

**Option A: Pass-through mode (recommended)** — hand your existing provider to CogOS:

```python
from cog import CogOS
from cog.providers.openai_provider import OpenAIProvider

provider = OpenAIProvider(model="gpt-4o", api_key="sk-...")
cog = CogOS(provider=provider)

result = cog.run("Build a REST API with Node.js and PostgreSQL")
print(result["output"])
```

Works with any provider: OpenAI, Anthropic, DeepSeek, Zhipu/GLM, OpenRouter, or any OpenAI-compatible endpoint.

**Option B: String-based** — provide model name and API key:

```python
from cog import CogOS

cog = CogOS(llm="gpt-4o", api_key="sk-...", base_url=None)
```

**Option C: From environment / config file** — auto-detect from env vars or `cog.yaml`:

```python
from cog import CogOS

cog = CogOS.from_env()  # reads COG_*, OPENAI_*, ANTHROPIC_* env vars + cog.yaml
```

**Option D: CLI** — create a `cog.yaml` config file:

```bash
cog init                        # creates cog.yaml with defaults
# Edit cog.yaml to set your provider, model, and api_key
cog run "Create a React component with TypeScript"
```

### Using CogOS from Another AI Tool

CogOS is designed as a library that any AI tool (Claude Code, Codex CLI, Gemini CLI, etc.) can call:

```python
# Your AI tool already has a provider — pass it through
from cog import CogOS

cog = CogOS(provider=my_existing_provider)
result = cog.run("Analyze this codebase for security issues")
```

No API keys duplicated, no second config. Your host tool's provider is CogOS's provider.

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
