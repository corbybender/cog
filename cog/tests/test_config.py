from __future__ import annotations

import os
import tempfile
from pathlib import Path

from cog.config import (
    build_config,
    find_config_path,
    generate_default_config,
    load_config_file,
    load_env_overrides,
)
from cog.kernel import KernelConfig


class TestConfigFile:
    def test_load_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = Path(tmpdir) / "cog.yaml"
            cfg_path.write_text(
                "provider: anthropic\nmodel: claude-sonnet-4-20250514\nmemory_backend: sqlite\n"
            )
            data = load_config_file(cfg_path)
            assert data["provider"] == "anthropic"
            assert data["model"] == "claude-sonnet-4-20250514"
            assert data["memory_backend"] == "sqlite"

    def test_load_missing_returns_empty(self) -> None:
        data = load_config_file(Path("/nonexistent/cog.yaml"))
        assert data == {}

    def test_find_config_in_current_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = Path(tmpdir) / "cog.yaml"
            cfg_path.write_text("provider: openai\n")
            found = find_config_path(Path(tmpdir))
            assert found is not None
            assert found.name == "cog.yaml"

    def test_find_config_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            found = find_config_path(Path(tmpdir))
            assert found is None


class TestConfigMerge:
    def test_defaults_only(self) -> None:
        config = build_config(
            file_overrides={
                "provider": "openai",
                "model": "gpt-4o",
                "memory_backend": "mem0",
            }
        )
        assert config.provider == "openai"
        assert config.model == "gpt-4o"
        assert config.memory_backend == "mem0"
        assert config.max_agent_iterations == 20
        assert config.max_agent_iterations == 20

    def test_file_overrides_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = Path(tmpdir) / "cog.yaml"
            cfg_path.write_text("provider: anthropic\nmodel: claude-haiku\n")
            data = load_config_file(cfg_path)
            config = build_config(file_overrides=data)
            assert config.provider == "anthropic"
            assert config.model == "claude-haiku"

    def test_cli_overrides_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = Path(tmpdir) / "cog.yaml"
            cfg_path.write_text("provider: anthropic\nmodel: claude-haiku\n")
            data = load_config_file(cfg_path)
            config = build_config(
                file_overrides=data,
                cli_overrides={"provider": "openai", "model": "gpt-4o"},
            )
            assert config.provider == "openai"
            assert config.model == "gpt-4o"

    def test_env_overrides(self) -> None:
        old = os.environ.get("COG_PROVIDER")
        os.environ["COG_PROVIDER"] = "anthropic"
        try:
            config = build_config()
            assert config.provider == "anthropic"
        finally:
            if old is None:
                os.environ.pop("COG_PROVIDER", None)
            else:
                os.environ["COG_PROVIDER"] = old

    def test_cli_wins_over_env(self) -> None:
        old = os.environ.get("COG_PROVIDER")
        os.environ["COG_PROVIDER"] = "anthropic"
        try:
            config = build_config(cli_overrides={"provider": "openai"})
            assert config.provider == "openai"
        finally:
            if old is None:
                os.environ.pop("COG_PROVIDER", None)
            else:
                os.environ["COG_PROVIDER"] = old

    def test_type_coercion(self) -> None:
        config = build_config(cli_overrides={"max_agent_iterations": "5"})
        assert config.max_agent_iterations == 5
        assert isinstance(config.max_agent_iterations, int)

    def test_mem0_config_from_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = Path(tmpdir) / "cog.yaml"
            cfg_path.write_text("provider: openai\nmem0_config:\n  foo: bar\n")
            data = load_config_file(cfg_path)
            config = build_config(file_overrides=data)
            assert config.mem0_config == {"foo": "bar"}

    def test_full_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = Path(tmpdir) / "cog.yaml"
            cfg_path.write_text("model: from-file\nmax_agent_iterations: 10\n")
            data = load_config_file(cfg_path)
            old_model = os.environ.get("COG_MODEL")
            os.environ["COG_MODEL"] = "from-env"
            try:
                config = build_config(
                    file_overrides=data,
                    cli_overrides={"model": "from-cli"},
                )
                assert config.model == "from-cli"
                assert config.max_agent_iterations == 10
            finally:
                if old_model is None:
                    os.environ.pop("COG_MODEL", None)
                else:
                    os.environ["COG_MODEL"] = old_model


class TestGenerateConfig:
    def test_generates_valid_yaml(self) -> None:
        content = generate_default_config()
        import yaml

        data = yaml.safe_load(content)
        assert data["provider"] == "openai"
        assert data["model"] == "gpt-4o"
        assert data["memory_backend"] == "mem0"

    def test_init_command(self) -> None:
        from cog.cli import cmd_init
        import argparse

        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "cog.yaml"
            args = argparse.Namespace(output=str(out), force=False)
            cmd_init(args)
            assert out.exists()
            content = out.read_text()
            assert "openai" in content
