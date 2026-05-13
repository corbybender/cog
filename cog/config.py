from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from cog.kernel import KernelConfig

CONFIG_FILENAME = "cog.yaml"
LOCAL_CONFIG_FILENAME = "cog.local.yaml"

_DEFAULTS: dict[str, Any] = {
    "modules_path": "modules",
    "memory_path": "cog_memory.db",
    "log_level": "INFO",
    "sandbox_enabled": False,
    "dry_run": False,
    "provider": None,
    "model": None,
    "api_key": None,
    "base_url": None,
    "max_agent_iterations": 20,
    "memory_backend": "mem0",
    "memory_user_id": "cogos-agent",
    "memory_agent_id": "cogos",
    "stream": True,
    "max_total_tokens": 0,
    "require_approval": False,
}

_ENV_MAP: dict[str, str] = {
    "provider": "COG_PROVIDER",
    "model": "COG_MODEL",
    "memory_backend": "COG_MEMORY_BACKEND",
    "modules_path": "COG_MODULES_PATH",
    "memory_path": "COG_MEMORY_PATH",
    "log_level": "COG_LOG_LEVEL",
    "max_agent_iterations": "COG_MAX_ITERATIONS",
    "memory_user_id": "COG_USER_ID",
    "memory_agent_id": "COG_AGENT_ID",
    "api_key": "COG_API_KEY",
    "base_url": "COG_BASE_URL",
    "stream": "COG_STREAM",
    "max_total_tokens": "COG_MAX_TOTAL_TOKENS",
    "require_approval": "COG_REQUIRE_APPROVAL",
}

_TYPE_COERCIONS: dict[str, type] = {
    "max_agent_iterations": int,
    "max_total_tokens": int,
    "sandbox_enabled": lambda v: str(v).lower() in ("true", "1", "yes"),
    "dry_run": lambda v: str(v).lower() in ("true", "1", "yes"),
    "stream": lambda v: str(v).lower() not in ("false", "0", "no"),
    "require_approval": lambda v: str(v).lower() in ("true", "1", "yes"),
}


def find_config_path(start: Path | None = None) -> Path | None:
    current = start or Path.cwd()
    current = current.resolve()
    for _ in range(20):
        candidate = current / CONFIG_FILENAME
        if candidate.exists():
            return candidate
        local = current / LOCAL_CONFIG_FILENAME
        if local.exists():
            return local
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def load_config_file(path: Path | None = None) -> dict[str, Any]:
    if path is None:
        found = find_config_path()
        if found is None:
            return {}
        path = found
    if not path.exists():
        return {}
    with open(path) as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def load_env_overrides() -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    for field_name, env_var in _ENV_MAP.items():
        value = os.environ.get(env_var)
        if value is not None:
            coercer = _TYPE_COERCIONS.get(field_name, str)
            try:
                overrides[field_name] = coercer(value)
            except (ValueError, TypeError):
                overrides[field_name] = value
    if os.environ.get("OPENAI_API_KEY") and "api_key" not in overrides:
        overrides["api_key"] = os.environ["OPENAI_API_KEY"]
        overrides.setdefault("provider", "openai")
    if os.environ.get("OPENAI_BASE_URL") and "base_url" not in overrides:
        overrides["base_url"] = os.environ["OPENAI_BASE_URL"]
    if os.environ.get("ANTHROPIC_API_KEY") and "provider" not in overrides:
        overrides["provider"] = "anthropic"
        if "api_key" not in overrides:
            overrides["api_key"] = os.environ["ANTHROPIC_API_KEY"]
    return overrides


def build_config(
    file_overrides: dict[str, Any] | None = None,
    cli_overrides: dict[str, Any] | None = None,
) -> KernelConfig:
    file_cfg = load_config_file()
    if file_overrides:
        file_cfg.update(file_overrides)
    env_cfg = load_env_overrides()
    cli_cfg = cli_overrides or {}

    merged: dict[str, Any] = {}
    for key in _DEFAULTS:
        if key in cli_cfg and cli_cfg[key] is not None:
            val = cli_cfg[key]
            coercer = _TYPE_COERCIONS.get(key)
            if coercer and isinstance(val, str):
                try:
                    val = coercer(val)
                except (ValueError, TypeError):
                    pass
            merged[key] = val
        elif key in env_cfg:
            merged[key] = env_cfg[key]
        elif key in file_cfg:
            merged[key] = file_cfg[key]
        else:
            merged[key] = _DEFAULTS[key]

    if "mem0_config" in file_cfg:
        merged["mem0_config"] = file_cfg["mem0_config"]

    for key in ("api_key", "base_url"):
        if key not in merged or merged[key] is None:
            if key in file_cfg:
                merged[key] = file_cfg[key]
            elif key in env_cfg:
                merged[key] = env_cfg[key]

    return KernelConfig(**merged)


def generate_default_config() -> str:
    return yaml.dump(
        {
            "provider": "openai",
            "model": "gpt-4o",
            "api_key": "YOUR_API_KEY_HERE",
            "base_url": None,
            "memory_backend": "mem0",
            "modules_path": "modules",
            "memory_path": "cog_memory.db",
            "log_level": "INFO",
            "max_agent_iterations": 20,
            "memory_user_id": "cogos-agent",
            "memory_agent_id": "cogos",
        },
        default_flow_style=False,
        sort_keys=True,
    )
