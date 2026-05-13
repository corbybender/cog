# CogOS - Modular Cognitive Runtime System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11%2B-green.svg)](https://www.python.org/downloads/)
[![Modules](https://img.shields.io/badge/Modules-71-purple.svg)](https://github.com/corbybender/cog#modules)
[![Free](https://img.shields.io/badge/Price-Free-success.svg)](https://github.com/corbybender/cog)

**A modular cognitive runtime with expert modules, web UI, and multi-agent collaboration. Free, open source, runs locally.**

[Quick Start](#quick-start) • [Web UI](#web-ui) • [Live Site](https://cogos.vercel.app) • [Docs](#documentation) • [Modules](#modules)

---

## What is CogOS?

CogOS is a **modular cognitive runtime** that enhances any LLM with:

- **71 Domain Modules** - Prompt extensions, tools, and verifiers for Python, JavaScript, AWS, Docker, Kubernetes, and more
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

That's it. `cog init` does three things automatically:

1. **Detects your LLM provider** — reads opencode.json, env vars (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`), or probes for Ollama on localhost. Writes `cog.yaml` for you.
2. **Registers as MCP server** — adds CogOS to Claude Code, Codex CLI, Gemini CLI, opencode. Your AI tool discovers it automatically.
3. **Writes AGENTS.md** — injects CogOS instructions into your project so the AI knows how to use it.

No config files to edit, no instructions to paste.

### How it works

After `cog init`, your AI tool sees CogOS tools automatically:

| MCP Tool | What it does |
|----------|-------------|
| `cog_run` | Run a cognitive task with multi-agent orchestration |
| `cog_chat` | Interactive conversation with CogOS |
| `cog_status` | Show active modules, tools, provider info |
| `cog_modules` | List available domain modules |
| `cog_set_provider` | Configure LLM provider at runtime (no restart) |

Your AI can now call these directly. CogOS uses whatever LLM provider your environment already has (OpenAI, Anthropic, Ollama, etc.) — no duplicate API keys.

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

71 domain-specific modules with 7,100+ prompt extensions, 48+ tools, and 5 verifiers:

### Programming Languages
- **JavaScript** - ES6+, Node.js, async patterns
- **TypeScript** - Generics, utility types, tsconfig
- **Python** - Django, Flask, FastAPI, data science
- **Java** - Spring Boot, Maven, streams, virtual threads
- **Go** - Goroutines, channels, modules, concurrency
- **C#** - .NET, ASP.NET
- **Ruby** - Rails, Bundler, RSpec, metaprogramming
- **PHP** - Laravel, Symfony, Composer, PSR standards
- **Rust** - Memory safety, async, cargo
- **C++** - Templates, STL, RAII, modern C++
- **Swift** - iOS/macOS development
- **Kotlin** - Android, JVM

### Frontend Frameworks
- **React / Next.js** - App Router, SSR, server components
- **Vue / Nuxt.js** - Auto-imports, composables, Nitro
- **Angular** - Signals, RxJS, dependency injection
- **Svelte / SvelteKit** - Reactive declarations, stores
- **SolidJS** - Fine-grained reactivity, reactive primitives
- **Remix** - Loaders/actions, nested routing
- **Astro** - Islands architecture, content collections

### Databases
- **PostgreSQL**, **MySQL**, **SQLite**, **MongoDB**, **Redis**, **Elasticsearch**, **Cassandra**

### Cloud Platforms
- **AWS** - EC2, S3, Lambda
- **Azure** - App Service, Functions, AKS
- **GCP** - Cloud Run, BigQuery, GKE
- **DigitalOcean**, **Linode**

### Containers & Infrastructure
- **Docker** - Dockerfiles, Compose, multi-stage builds
- **Kubernetes** - Pods, deployments, services, Helm
- **Terraform** - HCL, state management, providers
- **Ansible** - Playbooks, roles, inventory
- **GitHub Actions** - Workflows, CI/CD, matrix builds
- **GitLab CI/CD** - Pipelines, runners, stages
- **Jenkins** - Jenkinsfile, shared libraries

### Web Core
- **HTML5** - Semantic markup, accessibility, ARIA
- **CSS3** - Flexbox, Grid, Tailwind, animations

### Package Managers
- **npm**, **pnpm**, **Yarn** (Berry/PnP)

### API Styles
- **REST**, **GraphQL**, **gRPC**

### Testing
- **Playwright**, **Selenium**

### Operating Systems
- **Linux**, **macOS**, **Windows**

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
