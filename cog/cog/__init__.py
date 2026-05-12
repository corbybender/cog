"""CogOS - Cognitive Operating System."""

__version__ = "0.1.0"

from cog.kernel import Kernel, KernelConfig

class CogOS:
    def __init__(self, llm: str = "gpt-4o", api_key: str | None = None, base_url: str | None = None):
        provider = "openai"
        model = llm
        if "claude" in llm.lower():
            provider = "anthropic"
        elif "glm" in llm.lower():
            provider = "openai"
        self._config = KernelConfig(
            provider=provider,
            model=model,
            api_key=api_key,
            base_url=base_url,
            memory_backend="sqlite",
        )
        self._kernel = Kernel(self._config)
        self._kernel.start()

    def run(self, task: str, context: dict | None = None) -> dict:
        return self._kernel.run(task, context)

    def chat(self, message: str) -> dict:
        return self._kernel.chat(message)

    def think(self, task: str, **kwargs) -> dict:
        return self._kernel.run(task, kwargs if kwargs else None)

    @property
    def kernel(self) -> Kernel:
        return self._kernel
