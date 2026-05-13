"""CogOS - Cognitive Operating System."""

from __future__ import annotations

__version__ = "0.1.0"

from cog.kernel import Kernel, KernelConfig
from cog.providers.base import LLMProvider


class CogOS:
    """Primary entry point for CogOS.

    Supports three initialization modes:

    1. **Pass-through** — provide a pre-built LLMProvider directly.
       The host tool (Claude Code, Codex CLI, Gemini, etc.) builds its
       own provider and hands it to CogOS. No API keys or model names
       needed in CogOS config.

           from cog import CogOS
           from cog.providers.openai_provider import OpenAIProvider

           provider = OpenAIProvider(model="gpt-4o", api_key="sk-...")
           cog = CogOS(provider=provider)

    2. **String-based** — provide model name and API key.

           cog = CogOS(llm="gpt-4o", api_key="sk-...", base_url=None)

    3. **From environment** — auto-detect from COG_*, OPENAI_*, or
       ANTHROPIC_* env vars, with cog.yaml as fallback.

           cog = CogOS.from_env()
    """

    def __init__(
        self,
        provider: LLMProvider | None = None,
        *,
        llm: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        if provider is not None:
            self._kernel = Kernel()
            self._kernel.set_provider(provider)
            self._kernel.start()
            return

        if not llm:
            raise ValueError(
                "Provide either provider= (pass-through) or llm= and api_key=. "
                "See CogOS.from_env() for auto-detection from environment."
            )
        if not api_key:
            raise ValueError(
                "api_key is required when using string-based initialization. "
                "Use provider= to pass a pre-built LLMProvider, or set "
                "COG_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY."
            )
        provider_name = "openai"
        if "claude" in llm.lower():
            provider_name = "anthropic"
        config = KernelConfig(
            provider=provider_name,
            model=llm,
            api_key=api_key,
            base_url=base_url,
            memory_backend="sqlite",
        )
        self._kernel = Kernel(config)
        self._kernel.start()

    @classmethod
    def from_env(cls) -> CogOS:
        """Create CogOS from environment variables and cog.yaml.

        Resolution order: COG_* env vars > OPENAI_*/ANTHROPIC_* env vars
        > cog.yaml file. Raises ValueError if no configuration is found.
        """
        from cog.config import build_config

        config = build_config()
        if not config.provider or not config.model:
            raise ValueError(
                "No LLM configuration found. Set COG_PROVIDER and COG_MODEL "
                "env vars, create a cog.yaml file, or pass provider= explicitly."
            )
        instance = cls.__new__(cls)
        instance._kernel = Kernel(config)
        instance._kernel.start()
        return instance

    def run(self, task: str, context: dict | None = None) -> dict:
        return self._kernel.run(task, context)

    def chat(self, message: str) -> dict:
        return self._kernel.chat(message)

    def think(self, task: str, **kwargs) -> dict:
        return self._kernel.run(task, kwargs if kwargs else None)

    @property
    def kernel(self) -> Kernel:
        return self._kernel
