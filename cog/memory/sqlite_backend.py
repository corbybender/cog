from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any

from .base import MemoryBackend, MemoryEntry, MemoryType


class SQLiteMemoryBackend(MemoryBackend):
    def __init__(self, db_path: str | Path = "cog_memory.db"):
        self._db_path = Path(db_path)
        self._conn: sqlite3.Connection | None = None
        self._connect()

    def _connect(self) -> None:
        self._conn = sqlite3.connect(str(self._db_path))
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        assert self._conn is not None
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                memory_type TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT DEFAULT '{}',
                timestamp TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                tags TEXT DEFAULT '[]'
            );

            CREATE INDEX IF NOT EXISTS idx_memory_type ON memories(memory_type);
            CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp);

            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                id,
                content,
                tags,
                content='memories',
                content_rowid='rowid'
            );

            CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, id, content, tags)
                VALUES (new.rowid, new.id, new.content, new.tags);
            END;

            CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, id, content, tags)
                VALUES ('delete', old.rowid, old.id, old.content, old.tags);
            END;
            """
        )
        self._conn.commit()

    def store(self, entry: MemoryEntry) -> None:
        assert self._conn is not None
        if not entry.id:
            entry.id = str(uuid.uuid4())
        self._conn.execute(
            """
            INSERT OR REPLACE INTO memories (id, memory_type, content, metadata, timestamp, confidence, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.id,
                entry.memory_type.value,
                entry.content,
                json.dumps(entry.metadata),
                entry.timestamp,
                entry.confidence,
                json.dumps(entry.tags),
            ),
        )
        self._conn.commit()

    def retrieve(self, entry_id: str) -> MemoryEntry | None:
        assert self._conn is not None
        row = self._conn.execute(
            "SELECT * FROM memories WHERE id = ?", (entry_id,)
        ).fetchone()
        if row is None:
            return None
        return self._row_to_entry(row)

    def search(
        self,
        query: str,
        memory_type: MemoryType | None = None,
        tags: list[str] | None = None,
        limit: int = 10,
    ) -> list[MemoryEntry]:
        assert self._conn is not None
        conditions: list[str] = []
        params: list[Any] = []

        conditions.append(
            "id IN (SELECT id FROM memories_fts WHERE memories_fts MATCH ?)"
        )
        params.append(query)

        if memory_type:
            conditions.append("memory_type = ?")
            params.append(memory_type.value)

        if tags:
            for tag in tags:
                conditions.append("tags LIKE ?")
                params.append(f'%"{tag}"%')

        where = " AND ".join(conditions)
        sql = f"SELECT * FROM memories WHERE {where} ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_entry(row) for row in rows]

    def delete(self, entry_id: str) -> bool:
        assert self._conn is not None
        cursor = self._conn.execute("DELETE FROM memories WHERE id = ?", (entry_id,))
        self._conn.commit()
        return cursor.rowcount > 0

    def list_entries(
        self,
        memory_type: MemoryType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MemoryEntry]:
        assert self._conn is not None
        if memory_type:
            rows = self._conn.execute(
                "SELECT * FROM memories WHERE memory_type = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (memory_type.value, limit, offset),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM memories ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (limit, offset),
            ).fetchall()
        return [self._row_to_entry(row) for row in rows]

    @staticmethod
    def _row_to_entry(row: sqlite3.Row) -> MemoryEntry:
        return MemoryEntry(
            id=row["id"],
            memory_type=MemoryType(row["memory_type"]),
            content=row["content"],
            metadata=json.loads(row["metadata"]),
            timestamp=row["timestamp"],
            confidence=row["confidence"],
            tags=json.loads(row["tags"]),
        )

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
