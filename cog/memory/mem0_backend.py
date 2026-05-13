from __future__ import annotations

from typing import Any

from mem0 import Memory

from .base import MemoryBackend, MemoryEntry, MemoryType

_USER_ID = "cogos-agent"


class Mem0MemoryBackend(MemoryBackend):
    def __init__(
        self,
        config: dict[str, Any] | None = None,
        agent_id: str = "cogos",
        user_id: str = _USER_ID,
    ) -> None:
        if config:
            self._mem0 = Memory.from_config(config_dict=config)
        else:
            self._mem0 = Memory()
        self._agent_id = agent_id
        self._user_id = user_id

    def store(self, entry: MemoryEntry) -> None:
        messages = [{"role": "user", "content": entry.content}]
        metadata = dict(entry.metadata)
        metadata["memory_type"] = entry.memory_type.value
        metadata["tags"] = entry.tags
        metadata["confidence"] = entry.confidence

        self._mem0.add(
            messages,
            agent_id=self._agent_id,
            user_id=self._user_id,
            metadata=metadata,
            infer=True,
        )

    def store_conversation(
        self,
        messages: list[dict[str, str]],
        user_id: str | None = None,
        agent_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._mem0.add(
            messages,
            user_id=user_id or self._user_id,
            agent_id=agent_id or self._agent_id,
            metadata=metadata,
            infer=True,
        )

    def retrieve(self, entry_id: str) -> MemoryEntry | None:
        return None

    def search(
        self,
        query: str,
        memory_type: MemoryType | None = None,
        tags: list[str] | None = None,
        limit: int = 10,
    ) -> list[MemoryEntry]:
        filters: dict[str, Any] = {}
        if memory_type:
            filters["memory_type"] = memory_type.value

        results = self._mem0.search(
            query=query,
            agent_id=self._agent_id,
            user_id=self._user_id,
            limit=limit,
            filters=filters if filters else None,
        )

        entries = []
        for item in results.get("results", []):
            meta = item.get("metadata", {})
            entries.append(
                MemoryEntry(
                    id=item.get("id", ""),
                    memory_type=MemoryType(meta.get("memory_type", "semantic")),
                    content=item.get("memory", ""),
                    metadata=meta,
                    confidence=item.get("score", 1.0),
                    tags=meta.get("tags", []),
                    timestamp=meta.get("created_at", ""),
                )
            )
        return entries

    def search_raw(
        self,
        query: str,
        user_id: str | None = None,
        agent_id: str | None = None,
        limit: int = 10,
        threshold: float | None = None,
    ) -> list[dict[str, Any]]:
        results = self._mem0.search(
            query=query,
            user_id=user_id or self._user_id,
            agent_id=agent_id or self._agent_id,
            limit=limit,
            threshold=threshold,
        )
        return results.get("results", [])

    def delete(self, entry_id: str) -> bool:
        try:
            self._mem0.delete(entry_id)
            return True
        except Exception:
            return False

    def list_entries(
        self,
        memory_type: MemoryType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MemoryEntry]:
        return self.search(
            query="*",
            memory_type=memory_type,
            limit=limit,
        )

    def get_relevant_context(self, query: str, limit: int = 5) -> str:
        results = self.search(query=query, limit=limit)
        if not results:
            return ""
        lines = []
        for entry in results:
            source = f" [{entry.confidence:.0%}]" if entry.confidence < 1.0 else ""
            lines.append(f"- {entry.content}{source}")
        return "\n".join(lines)

    def close(self) -> None:
        pass
