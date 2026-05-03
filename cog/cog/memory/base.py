from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class MemoryType(str, Enum):
    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"
    PROJECT = "project"
    USER = "user"
    TASK = "task"


@dataclass
class MemoryEntry:
    id: str
    memory_type: MemoryType
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    confidence: float = 1.0
    tags: list[str] = field(default_factory=list)


class MemoryBackend(ABC):
    @abstractmethod
    def store(self, entry: MemoryEntry) -> None: ...

    @abstractmethod
    def retrieve(self, entry_id: str) -> MemoryEntry | None: ...

    @abstractmethod
    def search(
        self,
        query: str,
        memory_type: MemoryType | None = None,
        tags: list[str] | None = None,
        limit: int = 10,
    ) -> list[MemoryEntry]: ...

    @abstractmethod
    def delete(self, entry_id: str) -> bool: ...

    @abstractmethod
    def list_entries(
        self,
        memory_type: MemoryType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MemoryEntry]: ...
