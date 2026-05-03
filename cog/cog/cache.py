from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class CacheEntry:
    key: str
    value: Any
    timestamp: float
    hits: int = 0
    ttl: int = 3600  # 1 hour default

    def is_expired(self) -> bool:
        return time.time() - self.timestamp > self.ttl

    def touch(self) -> None:
        self.timestamp = time.time()
        self.hits += 1


class ResponseCache:
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600) -> None:
        self._cache: dict[str, CacheEntry] = {}
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._hits = 0
        self._misses = 0

    def _generate_key(self, *args: Any, **kwargs: Any) -> str:
        """Generate cache key from arguments."""
        key_data = {"args": args, "kwargs": sorted(kwargs.items())}
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.sha256(key_str.encode()).hexdigest()[:32]

    def get(self, key: str | None = None, *args: Any, **kwargs: Any) -> Any | None:
        """Get cached value."""
        if key is None:
            key = self._generate_key(*args, **kwargs)

        entry = self._cache.get(key)
        if entry is None:
            self._misses += 1
            return None

        if entry.is_expired():
            del self._cache[key]
            self._misses += 1
            return None

        entry.touch()
        self._hits += 1
        return entry.value

    def set(
        self,
        value: Any,
        key: str | None = None,
        ttl: int | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Set cached value."""
        if key is None:
            key = self._generate_key(*args, **kwargs)

        # Evict oldest if at capacity
        if len(self._cache) >= self._max_size:
            oldest = min(self._cache.values(), key=lambda e: e.timestamp)
            del self._cache[oldest.key]

        entry = CacheEntry(
            key=key,
            value=value,
            timestamp=time.time(),
            ttl=ttl or self._default_ttl,
        )
        self._cache[key] = entry

    def invalidate(self, key: str) -> bool:
        """Invalidate cache entry."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()

    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0
        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{hit_rate:.1%}",
        }

    def cleanup_expired(self) -> int:
        """Remove expired entries."""
        expired = [k for k, v in self._cache.items() if v.is_expired()]
        for k in expired:
            del self._cache[k]
        return len(expired)


class SmartCache:
    """Intelligent caching with semantic awareness."""

    def __init__(self) -> None:
        self._llm_cache = ResponseCache(max_size=500, default_ttl=7200)
        self._tool_cache = ResponseCache(max_size=1000, default_ttl=3600)
        self._semantic_cache: dict[str, Any] = {}

    def get_llm_response(self, messages: list[Any], tools: list[Any]) -> Any | None:
        """Get cached LLM response."""
        # Create a semantic key from messages and tools
        messages_summary = "".join([m.content or "" for m in messages[-3:]])
        tools_summary = "".join([t.name for t in tools]) if tools else ""
        key = self._llm_cache._generate_key(messages_summary, tools_summary)
        return self._llm_cache.get(key=key)

    def set_llm_response(
        self, messages: list[Any], tools: list[Any], response: Any
    ) -> None:
        """Cache LLM response."""
        messages_summary = "".join([m.content or "" for m in messages[-3:]])
        tools_summary = "".join([t.name for t in tools]) if tools else ""
        key = self._llm_cache._generate_key(messages_summary, tools_summary)
        self._llm_cache.set(response, key=key, ttl=7200)

    def get_tool_result(self, tool_name: str, arguments: dict[str, Any]) -> Any | None:
        """Get cached tool result."""
        key = self._tool_cache._generate_key(tool_name, arguments)
        return self._tool_cache.get(key=key)

    def set_tool_result(
        self, tool_name: str, arguments: dict[str, Any], result: Any, ttl: int = 600
    ) -> None:
        """Cache tool result."""
        key = self._tool_cache._generate_key(tool_name, arguments)
        self._tool_cache.set(result, key=key, ttl=ttl)

    def invalidate_tool(self, tool_name: str) -> None:
        """Invalidate all cached results for a tool."""
        prefix = self._tool_cache._generate_key(tool_name)
        keys_to_delete = [k for k in self._tool_cache._cache if k.startswith(prefix)]
        for k in keys_to_delete:
            self._tool_cache.invalidate(k)

    def stats(self) -> dict[str, Any]:
        """Get comprehensive cache stats."""
        return {
            "llm_cache": self._llm_cache.stats(),
            "tool_cache": self._tool_cache.stats(),
        }

    def cleanup(self) -> dict[str, int]:
        """Clean up expired entries."""
        return {
            "llm_expired": self._llm_cache.cleanup_expired(),
            "tool_expired": self._tool_cache.cleanup_expired(),
        }


# Global cache instance
_cache_instance: SmartCache | None = None


def get_cache() -> SmartCache:
    """Get global cache instance."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = SmartCache()
    return _cache_instance


def cached_tool(tool_name: str, ttl: int = 600):
    """Decorator for caching tool results."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache = get_cache()
            cache_key = {**kwargs}

            # Check cache
            cached = cache.get_tool_result(tool_name, cache_key)
            if cached is not None:
                return cached

            # Execute function
            result = func(*args, **kwargs)

            # Cache result
            cache.set_tool_result(tool_name, cache_key, result, ttl=ttl)
            return result

        return wrapper

    return decorator
