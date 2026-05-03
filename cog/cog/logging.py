from __future__ import annotations

import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogEntry:
    timestamp: str
    level: str
    module: str
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)


class CogLogger:
    def __init__(self, name: str = "cog", level: LogLevel = LogLevel.INFO):
        self._name = name
        self._level = level
        self._entries: list[LogEntry] = []
        self._python_logger = logging.getLogger(name)
        self._python_logger.setLevel(level.value)
        if not self._python_logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            self._python_logger.addHandler(handler)

    def _log(
        self, level: LogLevel, module: str, message: str, **metadata: Any
    ) -> LogEntry:
        entry = LogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            level=level.value,
            module=module,
            message=message,
            metadata=metadata,
        )
        self._entries.append(entry)
        getattr(self._python_logger, level.value.lower())(
            f"[{module}] {message}", extra=metadata if metadata else None
        )
        return entry

    def debug(self, module: str, message: str, **metadata: Any) -> LogEntry:
        return self._log(LogLevel.DEBUG, module, message, **metadata)

    def info(self, module: str, message: str, **metadata: Any) -> LogEntry:
        return self._log(LogLevel.INFO, module, message, **metadata)

    def warning(self, module: str, message: str, **metadata: Any) -> LogEntry:
        return self._log(LogLevel.WARNING, module, message, **metadata)

    def error(self, module: str, message: str, **metadata: Any) -> LogEntry:
        return self._log(LogLevel.ERROR, module, message, **metadata)

    def critical(self, module: str, message: str, **metadata: Any) -> LogEntry:
        return self._log(LogLevel.CRITICAL, module, message, **metadata)

    @property
    def entries(self) -> list[LogEntry]:
        return list(self._entries)

    def clear(self) -> None:
        self._entries.clear()


_logger: CogLogger | None = None


def get_logger() -> CogLogger:
    global _logger
    if _logger is None:
        _logger = CogLogger()
    return _logger
