from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult


class GitStatusTool(Tool):
    name = "git.status"
    description = "Show git working tree status"
    required_permissions = ["shell.execute"]

    def execute(self, *args, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        return ShellTool().execute(command="git status --short", timeout=30)


class GitLogTool(Tool):
    name = "git.log"
    description = "Show git commit history"
    required_permissions = ["shell.execute"]

    def execute(self, *args, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        n = kwargs.get("count", 10)
        return ShellTool().execute(command=f"git log --oneline -{n}", timeout=30)


class GitDiffTool(Tool):
    name = "git.diff"
    description = "Show git diff of changes"
    required_permissions = ["shell.execute"]

    def execute(self, *args, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        target = kwargs.get("target", "")
        cmd = f"git diff {target}".strip()
        return ShellTool().execute(command=cmd, timeout=30)


class GitBranchTool(Tool):
    name = "git.branch"
    description = "List or manage git branches"
    required_permissions = ["shell.execute"]

    def execute(self, *args, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        action = kwargs.get("action", "list")
        if action == "list":
            return ShellTool().execute(command="git branch -a", timeout=30)
        name = kwargs.get("name", "")
        if not name:
            return ToolResult(success=False, output="", error="Branch name required")
        if action == "create":
            return ShellTool().execute(command=f"git branch {name}", timeout=30)
        return ToolResult(success=False, output="", error=f"Unknown action: {action}")


class CogGit(CogModule):
    name = "cog-git"
    version = "1.0.0"
    description = "Git operations module"

    def register_tools(self) -> list[Tool]:
        return [GitStatusTool(), GitLogTool(), GitDiffTool(), GitBranchTool()]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "Git Expertise: You can inspect git repositories using git.status, git.log, "
            "git.diff, and git.branch tools. Use these to understand project history "
            "and changes before making modifications."
        ]

    def get_capabilities(self) -> list[str]:
        return ["git_status", "git_log", "git_diff", "git_commit", "git_branch"]

    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass


module = CogGit()
