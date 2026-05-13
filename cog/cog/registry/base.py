from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from cog.cog_logger import get_logger


class TrustLevel(str, Enum):
    OFFICIAL = "official"
    VERIFIED = "verified"
    COMMUNITY = "community"
    EXPERIMENTAL = "experimental"
    UNSAFE = "unsafe"


@dataclass
class RegistryEntry:
    name: str
    version: str
    description: str
    author: str = ""
    trust_level: TrustLevel = TrustLevel.COMMUNITY
    url: str = ""
    dependencies: list[str] = field(default_factory=list)
    rating: float = 0.0
    verified: bool = False
    install_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "trust_level": self.trust_level.value,
            "url": self.url,
            "dependencies": self.dependencies,
            "rating": self.rating,
            "verified": self.verified,
            "install_path": self.install_path,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RegistryEntry:
        return cls(
            name=data["name"],
            version=data["version"],
            description=data.get("description", ""),
            author=data.get("author", ""),
            trust_level=TrustLevel(data.get("trust_level", "community")),
            url=data.get("url", ""),
            dependencies=data.get("dependencies", []),
            rating=data.get("rating", 0.0),
            verified=data.get("verified", False),
            install_path=data.get("install_path", ""),
        )


class Registry:
    DEFAULT_REGISTRY_PATH = "modules/registry.json"

    def __init__(self, registry_path: str | None = None) -> None:
        self._entries: dict[str, RegistryEntry] = {}
        self._logger = get_logger()
        self._registry_path = Path(registry_path or self.DEFAULT_REGISTRY_PATH)
        self._load()

    def _load(self) -> None:
        if not self._registry_path.exists():
            self._seed_builtin_entries()
            self._save()
            return
        try:
            data = json.loads(self._registry_path.read_text())
            self._entries = {
                entry["name"]: RegistryEntry.from_dict(entry) for entry in data
            }
            self._logger.info("registry", f"Loaded {len(self._entries)} entries")
        except Exception as e:
            self._logger.warning("registry", f"Failed to load registry: {e}")
            self._seed_builtin_entries()

    def _save(self) -> None:
        try:
            self._registry_path.parent.mkdir(parents=True, exist_ok=True)
            data = [entry.to_dict() for entry in self._entries.values()]
            self._registry_path.write_text(json.dumps(data, indent=2))
        except Exception as e:
            self._logger.warning("registry", f"Failed to save registry: {e}")

    def _seed_builtin_entries(self) -> None:
        builtin = [
            RegistryEntry(
                name="code-core",
                version="1.0.0",
                description="Core programming abstractions and code understanding foundations",
                author="CogOS",
                trust_level=TrustLevel.OFFICIAL,
                dependencies=[],
            ),
            RegistryEntry(
                name="language-core",
                version="1.0.0",
                description="Core language understanding and parsing foundations",
                author="CogOS",
                trust_level=TrustLevel.OFFICIAL,
                dependencies=[],
            ),
            RegistryEntry(
                name="tool-core",
                version="1.0.0",
                description="Core tool execution and command understanding foundations",
                author="CogOS",
                trust_level=TrustLevel.OFFICIAL,
                dependencies=[],
            ),
            RegistryEntry(
                name="cog-code-python",
                version="1.0.0",
                description="Python code reasoning module",
                author="CogOS",
                trust_level=TrustLevel.OFFICIAL,
                dependencies=["code-core", "language-core"],
            ),
            RegistryEntry(
                name="cog-git",
                version="1.0.0",
                description="Git operations module",
                author="CogOS",
                trust_level=TrustLevel.OFFICIAL,
                dependencies=["tool-core"],
            ),
        ]
        for entry in builtin:
            self._entries[entry.name] = entry

    def register(self, entry: RegistryEntry) -> None:
        self._entries[entry.name] = entry
        self._save()
        self._logger.info("registry", f"Registered: {entry.name}@{entry.version}")

    def unregister(self, name: str) -> bool:
        if name in self._entries:
            del self._entries[name]
            self._save()
            self._logger.info("registry", f"Unregistered: {name}")
            return True
        return False

    def get(self, name: str) -> RegistryEntry | None:
        return self._entries.get(name)

    def search(self, query: str) -> list[RegistryEntry]:
        query = query.lower()
        return [
            e
            for e in self._entries.values()
            if query in e.name.lower() or query in e.description.lower()
        ]

    def list_all(self) -> list[RegistryEntry]:
        return list(self._entries.values())

    def resolve_dependencies(self, name: str) -> list[str]:
        visited: set[str] = set()
        order: list[str] = []

        def _walk(n: str) -> None:
            if n in visited:
                return
            visited.add(n)
            entry = self._entries.get(n)
            if entry:
                for dep in entry.dependencies:
                    _walk(dep)
            order.append(n)

        _walk(name)
        return order

    def install(self, name: str, modules_path: str = "modules") -> bool:
        entry = self.get(name)
        if not entry:
            self._logger.error("registry", f"Module not found in registry: {name}")
            return False

        module_path = Path(modules_path) / name
        if module_path.exists():
            self._logger.info("registry", f"Module already installed: {name}")
            return True

        if entry.url:
            return self._install_from_url(entry.url, module_path)

        self._logger.error("registry", f"No installation URL for {name}")
        return False

    def _install_from_url(self, url: str, dest_path: Path) -> bool:
        import subprocess

        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(
                ["git", "clone", url, str(dest_path)],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode == 0:
                self._logger.info("registry", f"Installed from {url} to {dest_path}")
                return True
            self._logger.error("registry", f"Git clone failed: {result.stderr}")
            return False
        except Exception as e:
            self._logger.error("registry", f"Installation failed: {e}")
            return False

    def publish(self, module_path: str) -> bool:
        module_dir = Path(module_path)
        manifest_file = module_dir / "manifest.json"
        if not manifest_file.exists():
            self._logger.error("registry", f"No manifest.json found in {module_path}")
            return False

        try:
            manifest = json.loads(manifest_file.read_text())
            entry = RegistryEntry(
                name=manifest["name"],
                version=manifest["version"],
                description=manifest.get("description", ""),
                author=manifest.get("author", "Unknown"),
                trust_level=TrustLevel.COMMUNITY,
                dependencies=manifest.get("requires", []),
                install_path=str(module_dir),
            )
            self.register(entry)
            return True
        except Exception as e:
            self._logger.error("registry", f"Failed to publish: {e}")
            return False
