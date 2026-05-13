from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any

from cog.cog_logger import get_logger
from cog.permissions import Permission


class PermissionLevel(str, Enum):
    SAFE = "safe"  # No approval needed
    LOW = "low"  # Optional approval
    MEDIUM = "medium"  # Require approval once
    HIGH = "high"  # Require approval each time
    CRITICAL = "critical"  # Require explicit confirmation


@dataclass
class PermissionRequest:
    tool: str
    arguments: dict[str, Any]
    permissions: list[str]
    level: PermissionLevel
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool": self.tool,
            "arguments": self.arguments,
            "permissions": self.permissions,
            "level": self.level.value,
            "reason": self.reason,
        }


class PermissionManager:
    """Manage permissions and user approvals."""

    def __init__(self) -> None:
        self._logger = get_logger()
        self._approved_cache: dict[str, bool] = {}
        self._permission_levels: dict[str, PermissionLevel] = {
            "filesystem.read": PermissionLevel.SAFE,
            "filesystem.list": PermissionLevel.SAFE,
            "filesystem.search": PermissionLevel.SAFE,
            "filesystem.write": PermissionLevel.HIGH,
            "shell.execute": PermissionLevel.HIGH,
            "shell.sandbox": PermissionLevel.MEDIUM,
            "web.fetch": PermissionLevel.LOW,
            "web.search": PermissionLevel.LOW,
            "python.lint": PermissionLevel.LOW,
            "python.test": PermissionLevel.LOW,
            "git.status": PermissionLevel.SAFE,
            "git.log": PermissionLevel.SAFE,
            "git.diff": PermissionLevel.LOW,
            "git.branch": PermissionLevel.MEDIUM,
        }

    def get_permission_level(self, tool_name: str) -> PermissionLevel:
        """Get permission level for a tool."""
        return self._permission_levels.get(tool_name, PermissionLevel.MEDIUM)

    def classify_request(
        self, tool_name: str, arguments: dict[str, Any], permissions: list[str]
    ) -> PermissionRequest:
        """Classify a permission request."""
        level = self.get_permission_level(tool_name)

        # Check for dangerous patterns
        if tool_name == "shell.execute":
            command = arguments.get("command", "")
            if "rm -rf" in command or "mkfs" in command:
                level = PermissionLevel.CRITICAL

        reason = self._generate_reason(tool_name, arguments, level)

        return PermissionRequest(
            tool=tool_name,
            arguments=arguments,
            permissions=permissions,
            level=level,
            reason=reason,
        )

    def _generate_reason(
        self, tool_name: str, arguments: dict[str, Any], level: PermissionLevel
    ) -> str:
        """Generate human-readable reason for permission request."""
        if tool_name == "filesystem.write":
            path = arguments.get("path", "unknown")
            return f"Writing to file: {path}"
        elif tool_name == "shell.execute":
            command = arguments.get("command", "")
            return f"Executing shell command: {command[:100]}"
        elif tool_name == "git.branch":
            branch = arguments.get("name", "unknown")
            return f"Creating git branch: {branch}"
        return f"Using {tool_name}"

    def should_approve(self, request: PermissionRequest) -> bool:
        """Determine if request should be auto-approved."""
        if request.level == PermissionLevel.SAFE:
            return True

        # Check cache for previously approved
        cache_key = self._cache_key(request)
        if cache_key in self._approved_cache:
            return self._approved_cache[cache_key]

        return False

    def approve(self, request: PermissionRequest, remember: bool = False) -> None:
        """Approve a permission request."""
        if remember:
            cache_key = self._cache_key(request)
            self._approved_cache[cache_key] = True

    def deny(self, request: PermissionRequest, remember: bool = False) -> None:
        """Deny a permission request."""
        if remember:
            cache_key = self._cache_key(request)
            self._approved_cache[cache_key] = False

    def _cache_key(self, request: PermissionRequest) -> str:
        """Generate cache key for request."""
        return f"{request.tool}:{json.dumps(request.arguments, sort_keys=True)}"


class InteractivePermissionUI:
    """Interactive permission approval UI."""

    def __init__(self, manager: PermissionManager) -> None:
        self._manager = manager
        self._logger = get_logger()

    def request_approval(self, request: PermissionRequest) -> bool:
        """Request user approval interactively."""
        # Check if auto-approved
        if self._manager.should_approve(request):
            return True

        # Display approval prompt
        print()
        print("🔒 Permission Request")
        print(f"  Tool: {request.tool}")
        print(f"  Level: {request.level.value.upper()}")
        print(f"  Reason: {request.reason}")

        if request.arguments:
            args_str = json.dumps(request.arguments, indent=4)
            if len(args_str) > 200:
                args_str = args_str[:200] + "..."
            print(f"  Arguments: {args_str}")

        # Get user response
        try:
            response = self._get_user_response(request.level)

            if response == "yes":
                self._manager.approve(request, remember=request.level != PermissionLevel.CRITICAL)
                return True
            elif response == "always":
                self._manager.approve(request, remember=True)
                return True
            else:
                self._manager.deny(request, remember=False)
                return False

        except (EOFError, KeyboardInterrupt):
            print("\n❌ Approval cancelled")
            return False

    def _get_user_response(self, level: PermissionLevel) -> str:
        """Get user response based on permission level."""
        if level == PermissionLevel.CRITICAL:
            print("  Options: 'yes' to approve once, 'no' to deny")
            return input("  Approve? [yes/no] ").strip().lower()
        elif level == PermissionLevel.HIGH:
            print("  Options: 'yes' to approve once, 'no' to deny")
            return input("  Approve? [yes/no] ").strip().lower()
        elif level == PermissionLevel.MEDIUM:
            print("  Options: 'yes' to approve once, 'always' to remember, 'no' to deny")
            return input("  Approve? [yes/always/no] ").strip().lower()
        else:
            return "yes"  # Auto-approve for low level

    def show_permission_stats(self) -> None:
        """Show permission statistics."""
        total = len(self._manager._approved_cache)
        approved = sum(1 for v in self._manager._approved_cache.values() if v)
        print(f"\n📊 Permission Stats: {approved}/{total} cached approvals")


class AutoApprovePolicy:
    """Automatic approval policy based on rules."""

    def __init__(self, manager: PermissionManager) -> None:
        self._manager = manager

    def should_auto_approve(self, request: PermissionRequest) -> bool:
        """Determine if request should be auto-approved based on policy."""
        # Auto-approve filesystem operations in safe directories
        if request.tool == "filesystem.write":
            path = request.arguments.get("path", "")
            safe_paths = ["/tmp", "./tests", "./examples"]
            if any(path.startswith(p) for p in safe_paths):
                return True

        # Auto-approve git operations that don't modify history
        if request.tool in ["git.status", "git.log", "git.diff"]:
            return True

        # Auto-approve Python tools
        if request.tool in ["python.lint", "python.test"]:
            return True

        return False
