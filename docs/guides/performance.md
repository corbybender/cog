# Performance Optimization

Guide to optimizing CogOS for speed, cost, and efficiency.

## Table of Contents

- [Caching Strategies](#caching-strategies)
- [Token Optimization](#token-optimization)
- [Parallel Processing](#parallel-processing)
- [Model Selection](#model-selection)
- [Resource Management](#resource-management)
- [Monitoring](#monitoring)

---

## Caching Strategies

### Response Caching

Cache LLM responses to avoid redundant API calls:

```python
from cogos import CogOS

cogos = CogOS(
    cache_enabled=True,
    cache_ttl=3600,  # Cache for 1 hour
    cache_max_size=1000  # Max 1000 cached entries
)
```

**Benefits:**
- 40-60% reduction in API calls
- Faster response times
- Lower costs

**Cache Keys:**
- Task hash
- Modules used
- Parameters
- Model version

### Cache Eviction Policies

```python
from cogos.cache import SmartCache

cache = SmartCache(
    ttl=3600,
    max_size=1000,
    eviction_policy="lru"  # or "lfu", "fifo"
)
```

**Policies:**
- `lru` - Least Recently Used (default)
- `lfu` - Least Frequently Used
- `fifo` - First In, First Out

### Cache Statistics

```python
# Get cache performance
stats = cogos.cache.stats()
print(f"Hit rate: {stats.hit_rate:.2%}")
print(f"Miss rate: {stats.miss_rate:.2%}")
print(f"Entries: {stats.entries}")
print(f"Size: {stats.size_mb:.2f} MB")
```

### Manual Cache Management

```python
# Clear cache
cogos.cache.clear()

# Clear specific entry
cogos.cache.delete("task_hash")

# Pre-warm cache
cogos.cache.warm_with([
    "Common task 1",
    "Common task 2",
    "Common task 3"
])
```

---

## Token Optimization

### Efficient Prompting

Use concise prompts:

```python
# Bad: Verbose
result = cogos.think("""
I would like you to please create a REST API using
the FastAPI framework with the following specifications...
""")

# Good: Concise
result = cogos.think("Create FastAPI REST API with CRUD endpoints")
```

### Module Filtering

Use only necessary modules:

```python
# Bad: Auto-loading all modules
result = cogos.think("Create a Python script")

# Good: Specific modules
result = cogos.think(
    "Create a Python script",
    modules=["python"]  # Only Python module
)
```

### Token Limits

Set appropriate token limits:

```python
cogos = CogOS(
    max_tokens=2048,  # Limit response tokens
    temperature=0.7,  # Reduce randomness
    top_p=0.9  # Nucleus sampling
)
```

### Streaming Responses

Use streaming for faster feedback:

```python
cogos = CogOS(
    enable_streaming=True
)

for chunk in cogos.think_stream("Create a REST API"):
    print(chunk, end="", flush=True)
```

---

## Parallel Processing

### Parallel Agent Execution

Run agents in parallel:

```python
cogos = CogOS(
    enable_parallel_agents=True,
    max_concurrent_agents=4
)
```

**When to Use:**
- Independent tasks
- Different modules
- Non-dependent agents

**When NOT to Use:**
- Sequential dependencies
- Shared resources
- Order matters

### Task Batching

Batch multiple tasks:

```python
tasks = [
    "Create user service",
    "Create product service",
    "Create order service"
]

results = cogos.think_batch(tasks, parallel=True)
```

### Async Operations

Use async for I/O-bound tasks:

```python
import asyncio
from cogos import CogOS

async def process_tasks():
    cogos = CogOS()
    tasks = [
        cogos.think_async("Task 1"),
        cogos.think_async("Task 2"),
        cogos.think_async("Task 3")
    ]
    results = await asyncio.gather(*tasks)
    return results

results = asyncio.run(process_tasks())
```

---

## Model Selection

### Choose Right Model

Select model based on task complexity:

```python
from cogos import CogOS

# Simple tasks: Use fast model
simple_cogos = CogOS(model="claude-3-5-haiku-20241022")

# Complex tasks: Use capable model
complex_cogos = CogOS(model="claude-3-5-sonnet-20241022")

# Critical tasks: Use best model
best_cogos = CogOS(model="claude-3-opus-20240229")
```

### Model Routing

Route tasks to appropriate models:

```python
class ModelRouter:
    """Route tasks to appropriate models."""

    def __init__(self):
        self.models = {
            "simple": CogOS(model="haiku"),
            "complex": CogOS(model="sonnet"),
            "critical": CogOS(model="opus")
        }

    def route(self, task):
        """Route task to appropriate model."""
        complexity = self.assess_complexity(task)

        if complexity == "low":
            return self.models["simple"]
        elif complexity == "medium":
            return self.models["complex"]
        else:
            return self.models["critical"]

    def assess_complexity(self, task):
        """Assess task complexity."""
        # Complexity assessment logic
        if len(task) < 100:
            return "low"
        elif len(task) < 500:
            return "medium"
        else:
            return "high"
```

### Cost Optimization

Optimize for cost:

```python
# For development
dev_cogos = CogOS(
    model="haiku",  # Cheapest
    cache_enabled=True,
    max_tokens=1024
)

# For production
prod_cogos = CogOS(
    model="sonnet",  # Balanced
    cache_enabled=True,
    max_tokens=2048
)
```

---

## Resource Management

### Connection Pooling

Use connection pooling for API calls:

```python
cogos = CogOS(
    max_concurrent_requests=10,
    connection_pool_size=20,
    request_timeout=30
)
```

### Memory Management

Manage memory efficiently:

```python
cogos = CogOS(
    memory_backend="sqlite",  # Lightweight
    cache_max_size=1000,  # Limit cache size
    enable_memory_compression=True
)
```

### Thread Safety

Use thread-safe operations:

```python
from concurrent.futures import ThreadPoolExecutor

def process_task(task):
    """Process single task."""
    cogos = CogOS()  # Each thread gets own instance
    return cogos.think(task)

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_task, tasks)
```

---

## Monitoring

### Performance Metrics

Track performance:

```python
# Enable performance tracking
cogos = CogOS(
    track_performance=True,
    log_performance=True
)

# Get metrics
metrics = cogos.get_performance_metrics()
print(f"Average latency: {metrics.avg_latency:.2f}ms")
print(f"Tokens per second: {metrics.tokens_per_sec:.2f}")
print(f"Cache hit rate: {metrics.cache_hit_rate:.2%}")
```

### Custom Metrics

Add custom metrics:

```python
from cogos import monitor

@monitor.track("custom_task")
def custom_task():
    """Custom tracked task."""
    result = cogos.think("Do something")
    monitor.increment("custom_tasks_completed")
    return result
```

### Alerts

Set up performance alerts:

```python
cogos = CogOS(
    alert_on_slow_response=True,
    slow_response_threshold=5000,  # 5 seconds
    alert_on_high_error_rate=True,
    error_rate_threshold=0.05  # 5%
)
```

---

## Optimization Strategies

### 1. Development

```python
# Fast iteration
dev_cogos = CogOS(
    model="haiku",
    cache_enabled=True,
    max_tokens=1024,
    timeout=30
)
```

### 2. Staging

```python
# Balanced
staging_cogos = CogOS(
    model="sonnet",
    cache_enabled=True,
    max_tokens=2048,
    timeout=60
)
```

### 3. Production

```python
# Optimized
prod_cogos = CogOS(
    model="sonnet",
    cache_enabled=True,
    cache_ttl=3600,
    enable_parallel_agents=True,
    max_concurrent_agents=4,
    track_performance=True
)
```

---

## Performance Tuning

### Agent Iterations

Reduce unnecessary iterations:

```python
cogos = CogOS(
    max_agent_iterations=3,  # Default: 5
    early_stopping=True,  # Stop if consensus reached
    consensus_threshold=0.8  # 80% agreement
)
```

### Research Timeout

Limit research time:

```python
cogos = CogOS(
    research_enabled=True,
    research_timeout=60,  # 60 seconds max
    research_max_sources=10  # Limit sources
)
```

### Output Filtering

Filter unnecessary output:

```python
cogos = CogOS(
    include_metadata=False,  # Skip metadata
    save_intermediate_results=False,  # Save memory
    output_format="code"  # Only code, no explanation
)
```

---

## Benchmarks

### Typical Performance

| Task | Model | Time | Tokens | Cost |
|------|-------|------|--------|------|
| Simple script | Haiku | 2s | 500 | $0.00025 |
| REST API | Sonnet | 15s | 3000 | $0.009 |
| Microservice | Sonnet | 30s | 5000 | $0.015 |
| Full app | Opus | 60s | 8000 | $0.096 |

### Cache Impact

| Scenario | No Cache | With Cache | Improvement |
|----------|----------|------------|-------------|
| First run | 15s | 15s | - |
| Repeated run | 15s | 0.5s | 30x faster |
| 10 runs | 150s | 20s | 7.5x faster |

---

## Best Practices

1. **Always enable caching** in production
2. **Use appropriate models** for task complexity
3. **Set timeouts** to prevent hanging
4. **Monitor performance** metrics
5. **Use parallel processing** when possible
6. **Optimize prompts** for conciseness
7. **Limit token usage** with max_tokens
8. **Profile before optimizing** - measure first

---

## Troubleshooting

### Slow Performance

```python
# Check cache hit rate
stats = cogos.cache.stats()
if stats.hit_rate < 0.5:
    print("Low cache hit rate - consider increasing TTL")

# Check for bottlenecks
metrics = cogos.get_performance_metrics()
print(f"Slowest agent: {metrics.slowest_agent}")
```

### High Costs

```python
# Switch to cheaper model
cogos = CogOS(model="haiku")

# Reduce token usage
cogos = CogOS(max_tokens=1024)

# Improve caching
cogos = CogOS(cache_ttl=7200)  # 2 hours
```

### Memory Issues

```python
# Clear cache
cogos.cache.clear()

# Reduce cache size
cogos = CogOS(cache_max_size=500)

# Use lighter backend
cogos = CogOS(memory_backend="json")
```

---

## Related Documentation

- [Configuration](../api/configuration.md)
- [Python API](../api/python.md)
- [Multi-Agent System](../architecture/multi_agent.md)

---

**Next:** [Monitoring & Debugging](../guides/debugging.md)
