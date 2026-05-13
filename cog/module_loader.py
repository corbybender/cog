from __future__ import annotations

import importlib.util
import inspect
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from cog.cog_module import CogModule
from cog.permissions import Permission, PermissionSet


class ModuleState(str, Enum):
    DISCOVERED = "discovered"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"
    UNLOADED = "unloaded"


@dataclass
class ModuleManifest:
    name: str
    version: str
    description: str
    capabilities: list[str] = field(default_factory=list)
    requires: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    entrypoint: str = "module.py"
    verification: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "capabilities": self.capabilities,
            "requires": self.requires,
            "permissions": self.permissions,
            "entrypoint": self.entrypoint,
            "verification": self.verification,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ModuleManifest:
        return cls(
            name=data["name"],
            version=data["version"],
            description=data.get("description", ""),
            capabilities=data.get("capabilities", []),
            requires=data.get("requires", []),
            permissions=data.get("permissions", []),
            entrypoint=data.get("entrypoint", "module.py"),
            verification=data.get("verification", {}),
        )


@dataclass
class Module:
    manifest: ModuleManifest
    path: Path
    state: ModuleState = ModuleState.DISCOVERED
    raw_module: Any = None
    cog_module: CogModule | None = None
    error: str | None = None

    @property
    def name(self) -> str:
        return self.manifest.name

    @property
    def capabilities(self) -> list[str]:
        return self.manifest.capabilities

    @property
    def instance(self) -> Any:
        return self.raw_module

    @instance.setter
    def instance(self, value: Any) -> None:
        self.raw_module = value

    def get_permission_set(self) -> PermissionSet:
        ps = PermissionSet()
        for perm_str in self.manifest.permissions:
            try:
                ps.grant(Permission(perm_str))
            except ValueError:
                pass
        return ps


class ModuleLoader:
    MANIFEST_FILE = "manifest.json"

    def __init__(self, search_paths: list[str | Path] | None = None):
        self._search_paths = [Path(p) for p in (search_paths or ["modules"])]
        self._modules: dict[str, Module] = {}

    def discover(self) -> list[Module]:
        discovered = []
        for search_path in self._search_paths:
            if not search_path.exists():
                continue
            for child in sorted(search_path.iterdir()):
                if not child.is_dir():
                    continue
                manifest_path = child / self.MANIFEST_FILE
                if not manifest_path.exists():
                    continue
                try:
                    manifest = self._load_manifest(manifest_path)
                    module = Module(manifest=manifest, path=child)
                    self._modules[manifest.name] = module
                    discovered.append(module)
                except Exception as e:
                    discovered.append(
                        Module(
                            manifest=ModuleManifest(
                                name=child.name, version="0.0.0", description=""
                            ),
                            path=child,
                            state=ModuleState.ERROR,
                            error=str(e),
                        )
                    )
        return discovered

    def load(self, name: str) -> Module:
        module = self._modules.get(name)
        if module is None:
            raise ValueError(f"Module not discovered: {name}")
        if module.state == ModuleState.LOADED or module.state == ModuleState.ACTIVE:
            return module
        entrypoint = module.path / module.manifest.entrypoint
        if not entrypoint.exists():
            module.state = ModuleState.ERROR
            module.error = f"Entrypoint not found: {entrypoint}"
            return module
        try:
            spec = importlib.util.spec_from_file_location(name, str(entrypoint))
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load module from {entrypoint}")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            module.raw_module = mod

            cog_mod = self._find_cog_module(mod)
            if cog_mod is not None:
                module.cog_module = cog_mod
                module.state = ModuleState.LOADED
            else:
                module.state = ModuleState.LOADED
        except Exception as e:
            module.state = ModuleState.ERROR
            module.error = str(e)
        return module

    def _find_cog_module(self, mod: Any) -> CogModule | None:
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)
            if (
                inspect.isclass(attr)
                and issubclass(attr, CogModule)
                and attr is not CogModule
            ):
                try:
                    return attr()
                except Exception:
                    pass

        module_export = getattr(mod, "module", None) or getattr(mod, "Module", None)
        if isinstance(module_export, CogModule):
            return module_export

        return None

    def unload(self, name: str) -> bool:
        module = self._modules.get(name)
        if module is None:
            return False
        if module.cog_module is not None:
            try:
                module.cog_module.on_unload()
            except Exception:
                pass
        module.raw_module = None
        module.cog_module = None
        module.state = ModuleState.UNLOADED
        return True

    def activate(self, name: str) -> Module:
        module = self.load(name)
        if module.state == ModuleState.LOADED:
            if module.cog_module is not None:
                try:
                    module.cog_module.on_load()
                except Exception:
                    pass
            module.state = ModuleState.ACTIVE
        return module

    def get(self, name: str) -> Module | None:
        return self._modules.get(name)

    def get_active(self) -> list[Module]:
        return [m for m in self._modules.values() if m.state == ModuleState.ACTIVE]

    def _resolve_activation_order(self) -> list[Module]:
        discovered = [
            m
            for m in self._modules.values()
            if m.state not in (ModuleState.ERROR, ModuleState.UNLOADED)
        ]
        active_names: set[str] = set()
        for m in discovered:
            active_names.add(m.name)
        satisfied: set[str] = set()
        ordered: list[Module] = []
        remaining = list(discovered)
        for _ in range(len(remaining) + 1):
            progress = False
            next_remaining = []
            for mod in remaining:
                deps = mod.manifest.requires
                if all(d in satisfied or d not in active_names for d in deps):
                    ordered.append(mod)
                    satisfied.add(mod.name)
                    progress = True
                else:
                    next_remaining.append(mod)
            remaining = next_remaining
            if not remaining or not progress:
                break
        ordered.extend(remaining)
        return ordered

    def get_tools(self) -> dict[str, Any]:
        tools: dict[str, Any] = {}
        for mod in self.get_active():
            if mod.cog_module is not None:
                for tool in mod.cog_module.register_tools():
                    tools[tool.name] = tool
        return tools

    def get_verifiers(self) -> list[Any]:
        verifiers = []
        for mod in self.get_active():
            if mod.cog_module is not None:
                verifiers.extend(mod.cog_module.register_verifiers())
        return verifiers

    def get_prompt_extensions(self) -> list[str]:
        extensions = []
        for mod in self.get_active():
            if mod.cog_module is not None:
                extensions.extend(mod.cog_module.get_prompt_extensions())
        return extensions

    def all(self) -> dict[str, Module]:
        return dict(self._modules)

    def _load_manifest(self, path: Path) -> ModuleManifest:
        data = json.loads(path.read_text(encoding="utf-8"))
        return ModuleManifest.from_dict(data)
