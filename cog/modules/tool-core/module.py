from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult


class ToolDryRunTool(Tool):
    name = "tool.dry_run"
    description = "Test a command without executing it (dry-run mode)"

    def execute(self, command: str, **kwargs) -> ToolResult:
        return ToolResult(
            success=True,
            output=f"[DRY RUN] Would execute: {command}",
            details={"command": command, "dry_run": True}
        )


class ToolCoreModule(CogModule):
    name = "tool-core"
    version = "1.0.0"
    description = "Core tool execution and command understanding foundations"

    def register_tools(self) -> list[Tool]:
        return [ToolDryRunTool()]

    def get_capabilities(self) -> list[str]:
        return ["command_execution", "tool_safety", "permission_handling", "dry_run"]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## Tool Core Foundations",
            "You understand tool execution fundamentals including:",
            "- Command structure and argument parsing",
            "- Shell execution and subprocess management",
            "- Permission models and security boundaries",
            "- Dry-run mode and safe execution patterns",
            "- Tool composition and chaining",
            "- Error handling and retry logic",
            "- Resource limits and timeouts",
            "",
            "When executing tools, always consider safety, permissions, and potential side effects."
        ]


module = ToolCoreModule()
