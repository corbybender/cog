# CogOS Configuration Guide

Complete guide to configuring CogOS for your needs.

## Table of Contents

- [Environment Variables](#environment-variables)
- [Configuration File](#configuration-file)
- [LLM Providers](#llm-providers)
- [Memory Backends](#memory-backends)
- [Caching](#caching)
- [Safety](#safety)
- [Logging](#logging)

---

## Environment Variables

CogOS uses environment variables for sensitive configuration like API keys.

### Required Variables

```bash
# LLM API Keys (at least one required)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Optional Variables

```bash
# Memory Backend
MEM0_API_KEY=your_mem0_api_key_here

# Research Tools
SERPER_API_KEY=your_serper_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Logging
LOG_LEVEL=INFO
LOG_FILE=cog.log

# Cache
CACHE_ENABLED=true
CACHE_TTL=3600

# Safety
SAFETY_LEVEL=STANDARD
SANDBOX_ENABLED=true
```

See [`.env.example`](../.env.example) for a complete list.

---

## Configuration File

CogOS can be configured via `cog.yaml` in your project root.

### Basic Configuration

```yaml
# LLM Provider
provider: anthropic
model: claude-3.5-sonnet
api_key: YOUR_API_KEY_HERE

# Memory
memory_backend: sqlite
memory_path: cog_memory.db

# Modules
modules_path: modules
auto_load_modules: true

# Logging
log_level: INFO
```

See [`cog.yaml.example`](../cog.yaml.example) for all options.

---

## LLM Providers

CogOS supports multiple LLM providers.

### Anthropic (Claude)

```yaml
provider: anthropic
model: claude-3.5-sonnet
base_url: https://api.anthropic.com
api_key: YOUR_ANTHROPIC_API_KEY
```

**Available Models:**
- `claude-3-5-sonnet-20241022` - Best for complex tasks
- `claude-3-5-haiku-20241022` - Fast and cost-effective
- `claude-3-opus-20240229` - High quality

### OpenAI (GPT)

```yaml
provider: openai
model: gpt-4
base_url: https://api.openai.com/v1
api_key: YOUR_OPENAI_API_KEY
```

**Available Models:**
- `gpt-4` - Best for complex tasks
- `gpt-4-turbo` - Fast and capable
- `gpt-3.5-turbo` - Fast and cost-effective

### Custom Provider

```yaml
provider: openai
model: your-model-name
base_url: https://your-api-endpoint.com
api_key: YOUR_API_KEY
```

---

## Memory Backends

CogOS supports multiple memory backends for conversation history and context.

### SQLite (Default)

```yaml
memory_backend: sqlite
memory_path: cog_memory.db
```

**Pros:**
- No external dependencies
- Fast for local development
- Easy to backup

**Cons:**
- Not suitable for distributed systems

### Mem0 (Cloud)

```yaml
memory_backend: mem0
mem0_api_key: YOUR_MEM0_API_KEY
```

**Pros:**
- Cloud-based
- Suitable for distributed systems
- Advanced search capabilities

**Cons:**
- Requires API key
- Internet connection required

### JSON (Development)

```yaml
memory_backend: json
memory_path: cog_memory.json
```

**Pros:**
- Human-readable
- Easy to debug

**Cons:**
- Slow for large conversations
- No concurrent access

---

## Caching

CogOS includes intelligent caching to reduce API calls and costs.

### Enable Caching

```yaml
cache_enabled: true
cache_ttl: 3600  # seconds
cache_max_size: 1000  # number of entries
```

### Cache Strategies

**Time-to-Live (TTL)**
```yaml
cache_ttl: 3600  # Cache for 1 hour
```

**LRU Eviction**
```yaml
cache_max_size: 1000  # Keep last 1000 entries
eviction_policy: lru
```

### Cache Statistics

```python
from cogos import CogOS

cogos = CogOS(cache_enabled=True)
# ... use cogos ...

# Get cache stats
stats = cogos.cache.stats()
print(f"Hit rate: {stats.hit_rate:.2%}")
print(f"Entries: {stats.entries}")
```

---

## Safety

CogOS includes multiple safety features to protect your system.

### Safety Levels

```yaml
safety_level: STANDARD
```

**Available Levels:**
- `SAFE` - No dangerous operations
- `STANDARD` - Requires approval for dangerous ops
- `ADVANCED` - More freedom with warnings
- `EXPERT` - Full access
- `CRITICAL` - Dangerous operations, explicit approval

### Sandboxing

```yaml
sandbox_enabled: true
sandbox_type: docker  # or 'fake' for development
```

**What Sandbox Does:**
- Isolates file system access
- Limits network access
- Restricts system calls
- Timeboxes execution

### Approval Required

```yaml
approval_required: true
approval_mode: interactive  # or 'auto'
```

**Operations Requiring Approval:**
- File writes outside project directory
- Network requests
- System commands
- Database modifications

---

## Logging

Configure logging to debug issues and monitor performance.

### Log Levels

```yaml
log_level: INFO
```

**Available Levels:**
- `DEBUG` - Detailed information for debugging
- `INFO` - General information (default)
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical errors only

### Log Files

```yaml
log_file: cog.log
log_max_size: 10MB
log_backup_count: 5
```

### Structured Logging

```yaml
log_format: json  # or 'text'
log_timestamps: true
log_metadata: true
```

### Programmatic Configuration

```python
import logging

# Configure CogOS logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cog.log'),
        logging.StreamHandler()
    ]
)
```

---

## Advanced Configuration

### Performance Tuning

```yaml
# Agent Configuration
max_agent_iterations: 20
agent_timeout: 300
enable_parallel_agents: true
max_concurrent_requests: 5

# Model Configuration
temperature: 0.7
max_tokens: 4096
top_p: 0.9
frequency_penalty: 0.0
presence_penalty: 0.0
```

### Research Configuration

```yaml
research_enabled: true
research_sources:
  - codebase
  - web
  - documentation
research_timeout: 60
research_max_results: 10
```

### Output Configuration

```yaml
output_format: markdown  # or 'json'
include_metadata: true
save_intermediate_results: false
output_directory: output/
```

---

## Configuration Examples

### Development Setup

```yaml
provider: anthropic
model: claude-3-5-haiku-20241022
cache_enabled: true
log_level: DEBUG
safety_level: SAFE
memory_backend: json
memory_path: dev_memory.json
```

### Production Setup

```yaml
provider: anthropic
model: claude-3-5-sonnet-20241022
cache_enabled: true
cache_ttl: 3600
log_level: INFO
log_file: /var/log/cog/cog.log
safety_level: STANDARD
memory_backend: mem0
mem0_api_key: ${MEM0_API_KEY}
```

### High-Performance Setup

```yaml
provider: openai
model: gpt-4-turbo
cache_enabled: true
cache_max_size: 10000
enable_parallel_agents: true
max_concurrent_requests: 10
research_enabled: false  # Disable for speed
```

---

## Troubleshooting

### Configuration Not Loading

```bash
# Check configuration file exists
ls cog.yaml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('cog.yaml'))"

# Check environment variables
env | grep COGOS
```

### API Key Issues

```bash
# Verify environment variables
echo $ANTHROPIC_API_KEY

# Test API connection
python -c "from cogos import CogOS; c = CogOS(); print('OK')"
```

### Cache Issues

```python
# Clear cache
from cogos import CogOS
cogos = CogOS()
cogos.cache.clear()

# Disable cache
cogos = CogOS(cache_enabled=False)
```

---

## Best Practices

1. **Use Environment Variables** for sensitive data
2. **Enable Caching** in production to reduce costs
3. **Set Appropriate Safety Levels** for your use case
4. **Monitor Logs** for issues and performance
5. **Test Configuration** before production deployment
6. **Use Separate Configs** for dev/staging/production
7. **Version Control** `cog.yaml.example`, not `cog.yaml`
8. **Document Custom** configurations for your team

---

## Related Documentation

- [Getting Started](../START_HERE.md)
- [Python API](api/python.md)
- [CLI Reference](api/cli.md)
- [Architecture](../architecture/README_SUPER_INTELLIGENCE.md)

---

**Next:** [Module System](api/modules.md)
