from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Permission(str, Enum):
    FILESYSTEM_READ = "filesystem.read"
    FILESYSTEM_WRITE = "filesystem.write"
    SHELL_EXECUTE = "shell.execute"
    NETWORK_ACCESS = "network.access"
    MEMORY_READ = "memory.read"
    MEMORY_WRITE = "memory.write"
    MODULE_LOAD = "module.load"
    MODULE_UNLOAD = "module.unload"


@dataclass
class PermissionSet:
    allowed: set[Permission] = field(default_factory=set)
    denied: set[Permission] = field(default_factory=set)

    def is_allowed(self, permission: Permission) -> bool:
        if permission in self.denied:
            return False
        return permission in self.allowed

    def grant(self, *permissions: Permission) -> None:
        for p in permissions:
            self.allowed.add(p)
            self.denied.discard(p)

    def revoke(self, *permissions: Permission) -> None:
        for p in permissions:
            self.allowed.discard(p)
            self.denied.add(p)

    def check(self, permission: Permission) -> None:
        if not self.is_allowed(permission):
            raise PermissionError(f"Permission denied: {permission.value}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": [p.value for p in self.allowed],
            "denied": [p.value for p in self.denied],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PermissionSet:
        ps = cls()
        for p in data.get("allowed", []):
            ps.allowed.add(Permission(p))
        for p in data.get("denied", []):
            ps.denied.add(Permission(p))
        return ps

    @classmethod
    def all(cls) -> PermissionSet:
        ps = cls()
        ps.allowed = set(Permission)
        return ps

    @classmethod
    def none(cls) -> PermissionSet:
        return cls()


DEFAULT_PERMISSIONS = PermissionSet(
    allowed={
        Permission.FILESYSTEM_READ,
        Permission.MEMORY_READ,
        Permission.MEMORY_WRITE,
    }
)
