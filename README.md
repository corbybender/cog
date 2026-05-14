# CogOS - Modular Cognitive Runtime System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11%2B-green.svg)](https://www.python.org/downloads/)
[![Modules](https://img.shields.io/badge/Modules-55-purple.svg)](https://github.com/corbybender/cog#modules)
[![Free](https://img.shields.io/badge/Price-Free-success.svg)](https://github.com/corbybender/cog)

**A modular cognitive runtime with expert modules, web UI, and multi-agent collaboration. Free, open source, runs locally.**

[Quick Start](#quick-start) • [Web UI](#web-ui) • [Live Site](https://cogos.vercel.app) • [Docs](#documentation) • [Modules](#modules)

---

## What is CogOS?

CogOS is a **modular cognitive runtime** that enhances any LLM with:

- **55 Domain Modules** - Prompt extensions, tools, and verifiers for Python, JavaScript, AWS, Docker, Kubernetes, and more
- **Multi-Agent Orchestration** - Specialized agents that collaborate on complex tasks (planner, researcher, coder, reviewer, tester, critic, documenter, optimizer, security, architect)
- **70 Built-in & Module Tools** - Filesystem operations, shell execution, web fetching/search, plus module-contributed tools for AWS, Docker, databases, languages, and more
- **Token-Efficient by Design** - Chunk indexer, session deduplication, and a configurable character budget keep context overhead minimal
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

1. **Detects your LLM provider** — reads opencode.json, env vars (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`), or probes for Ollama/LM Studio on localhost. Writes `cog.yaml` for you.
2. **Registers as MCP server** — adds CogOS to all detected AI tools. Currently supports:

| Tool | Config Location | Notes |
|------|----------------|-------|
| Claude Code | `~/.claude.json` | Full MCP support |
| Codex CLI | `~/.codex/config.toml` | Full MCP support |
| Gemini CLI | `~/.gemini/settings.json` | Full MCP support |
| opencode | `~/.config/opencode/opencode.json` | Full MCP support |
| Cursor | `.cursor/mcp.json` | Project-level config |
| VS Code / Cline / Roo | `.vscode/mcp.json` | Shared MCP config |
| Goose | `~/.config/goose/config.yaml` | Extension config |

3. **Writes AGENTS.md** — injects CogOS instructions into your project so the AI knows how to use it.

No config files to edit, no instructions to paste.

### How it works

After `cog init`, your AI tool sees CogOS tools automatically:

| MCP Tool | What it does |
|----------|-------------|
| `cog_run` | Returns expert knowledge from matching domain modules. The AI uses it to complete the task. |
| `cog_chat` | Ask follow-up questions about domain topics |
| `cog_status` | Show active modules, tools, and provider info |
| `cog_modules` | List available domain modules |

**CogOS does not need its own LLM.** The AI tool you are already running (Claude Code, Cursor, Gemini CLI, opencode, etc.) is the LLM. When your AI calls `cog_run()`, CogOS finds the relevant expert modules and returns their knowledge as context. Your AI then uses that context to complete the task with deep domain expertise it didn't have before.

No API key. No separate model. No duplicate configuration. Zero cost to add CogOS to an existing workflow.

### CLI commands

```bash
cog init                        # register CogOS as MCP server
cog register                    # re-register with AI tools
cog mcp                         # run the MCP server directly
cog run "your task here"        # run a cognitive task
cog chat                        # interactive chat
cog status                      # show modules, tools, provider info
```

### Token Efficiency — Built In

CogOS has 7,275+ prompt extensions across 55 modules. Without safeguards, a single `cog_run` call could dump 10,000–15,000 tokens of expertise into your context window before your AI writes a line of code. Three mechanisms work together automatically to prevent this:

#### 1. Chunk-level indexing (not module dumps)

The old approach returned every extension from the top 5 matching modules. The new approach scores each extension individually against your task and returns only the highest-relevance ones — across all modules — up to a character budget. A typical `cog_run` call now returns **~1,500 tokens** of tightly targeted knowledge instead of a broad module dump.

#### 2. Session deduplication

Every chunk of expertise returned is fingerprinted. If a follow-up `cog_run` or `cog_chat` call would return a chunk the AI already received this session, it's skipped. The response includes a `chunks_skipped_dedup` count so the AI knows its prior context is still valid. For a long working session, this compounds: the 10th call on a Python/Docker project returns almost nothing because almost everything relevant was already delivered in calls 1–3.

#### 3. Character budget

Total expertise per call is capped. The default is 6,000 characters (~1,500 tokens). Chunks are scored and filled greedily — the most relevant content first — so the budget cut always removes the least useful tail, not random content.

**These three features are automatic. No configuration required.** The budget is tunable in `cog.yaml` or via environment variable if your project genuinely needs more context:

```yaml
# cog.yaml
max_expertise_chars: 6000   # default — ~1,500 tokens per call
```

```bash
export COG_MAX_EXPERTISE_CHARS=10000   # raise for large, complex tasks
```

The response from `cog_run` tells your AI exactly what happened:

```json
{
  "chunks_returned": 12,
  "chunks_skipped_dedup": 8,
  "total_chars": 5840,
  "modules_contributing": [
    { "name": "cog-code-python", "chunks": 7 },
    { "name": "cog-infra-docker", "chunks": 5 }
  ],
  "expertise": "..."
}
```

---

### Model Configuration

**The default is zero configuration.** CogOS uses whatever AI model you are already interacting with. This is called "host AI" mode and it works automatically for every MCP-compatible tool — Claude Code, Cursor, Gemini CLI, opencode, Codex, Goose, and any other tool that supports MCP.

#### Saving tokens with per-agent models (optional)

Some internal CogOS agents — like the planner that breaks tasks into steps, or the document writer — don't need your premium model. You can point them at a smaller, cheaper model while keeping your main AI for the actual work.

Create or edit `cog.yaml` in your project root:

```yaml
# provider: host means "use my current AI tool" (the default)
provider: host

# Per-agent overrides — each can have its own model
agents:
  planner:
    provider: openai
    model: gpt-4o-mini        # cheap model for task planning
    api_key: YOUR_KEY_HERE
    # base_url: optional, for custom endpoints

  document_writer:
    provider: openai
    model: gpt-4o-mini        # cheap model for doc generation
    api_key: YOUR_KEY_HERE

  # executor: not set — uses your current AI (host mode)
  # researcher: not set — uses your current AI (host mode)

memory_backend: sqlite
modules_path: modules
memory_path: cog_memory.db
log_level: INFO
max_agent_iterations: 20
```

If an agent is not listed, it falls back to the global `provider` setting. With `provider: host`, that means your current AI handles it — no extra tokens charged to a separate key.

**Known agent roles:**

| Role | What it does | Cost profile |
|------|-------------|-------------|
| `planner` | Decomposes tasks into steps | Low — short prompts, structured output |
| `document_writer` | Generates docs and summaries | Medium — can use a small model |
| `executor` | Writes and runs code | High — use your best model (host AI by default) |
| `researcher` | Web search and analysis | Medium — use a small model or host AI |

#### Environment variables

| Variable | Purpose |
|----------|---------|
| `COG_PROVIDER` | Override global provider (openai, anthropic, host) |
| `COG_MODEL` | Override global model name |
| `COG_API_KEY` | API key (any provider) |
| `COG_BASE_URL` | Custom endpoint URL |
| `OPENAI_API_KEY` | Auto-detected, sets provider=openai |
| `ANTHROPIC_API_KEY` | Auto-detected, sets provider=anthropic |

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

55 domain-specific modules with 7,275+ prompt extensions, 70 tools, and verifiers:

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
