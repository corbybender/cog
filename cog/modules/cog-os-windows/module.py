from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult


class PowerShellTool(Tool):
    name = "windows.powershell"
    description = "Execute PowerShell commands"
    required_permissions = ["shell.execute"]

    def execute(self, command: str, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        full_command = f"powershell.exe -Command '{command}'"
        result = shell.execute(command=full_command, **kwargs)
        return result


class WindowsServiceTool(Tool):
    name = "windows.service"
    description = "Manage Windows services"
    required_permissions = ["shell.execute"]

    def execute(self, action: str, service: str, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"powershell.exe -Command '{action}-Service {service}'"
        result = shell.execute(command=command, timeout=60)
        return result


class WindowsRegistryTool(Tool):
    name = "windows.registry"
    description = "Query Windows registry"
    required_permissions = ["shell.execute"]

    def execute(self, path: str, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"reg query '{path}'"
        result = shell.execute(command=command, timeout=30)
        return result


class CogOSWindows(CogModule):
    name = "cog-os-windows"
    version = "1.0.0"
    description = "Windows operating system expertise"

    def register_tools(self) -> list[Tool]:
        return [
            PowerShellTool(),
            WindowsServiceTool(),
            WindowsRegistryTool(),
        ]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## Windows Operating System Expertise",
            "",
            "You understand Windows operating systems including:",
            "",
            "### PowerShell (ps1)",
            "- Cmdlets (Verb-Noun convention)",
            "- Pipelines (|)",
            "- Variables ($var)",
            "- Functions and scripts",
            "- Modules and snap-ins",
            "- Remoting (Enter-PSSession)",
            "- WMI and CIM",
            "- Active Directory cmdlets",
            "- Windows Management",
            "",
            "### Command Prompt (cmd)",
            "- Basic commands (dir, cd, copy, del)",
            "- Batch files (.bat)",
            "- Environment variables",
            "- Command redirection (>, >>)",
            "- Command chaining (&, &&, ||)",
            "",
            "### File System",
            "- Drive letters (C:, D:, etc.)",
            "- UNC paths (\\\\server\\share)",
            "- File permissions (ACLs)",
            "- Hidden files and system files",
            "- Short filenames (8.3 format)",
            "",
            "### Windows Registry",
            "- Registry hives (HKLM, HKCU, etc.)",
            "- Registry keys and values",
            "- reg.exe commands",
            "- Registry editing safety",
            "",
            "### Windows Services",
            "- Service control (sc.exe)",
            "- Service management",
            "- Service status and configuration",
            "- Automatic vs manual startup",
            "",
            "### Windows Networking",
            "- IP configuration (ipconfig)",
            "- Network diagnostics (ping, tracert)",
            "- Firewall rules (netsh)",
            "- Network shares (net use)",
            "- Remote Desktop (mstsc)",
            "",
            "### Windows-specific Patterns",
            "- Path separators: \\ (backslash)",
            "- Case-insensitive file system",
            "- Executable extensions: .exe, .bat, .ps1",
            "- Environment variables: %VAR% or $env:VAR",
            "- Line endings: CRLF (\\r\\n)",
            "",
            "### Common Tasks",
            "",
            "File operations:",
            "- PowerShell: Get-ChildItem, Set-Location, Copy-Item",
            "- CMD: dir, cd, copy, xcopy",
            "",
            "System information:",
            "- systeminfo",
            "- Get-ComputerInfo",
            "- wmic",
            "",
            "Process management:",
            "- Get-Process, Stop-Process",
            "- tasklist, taskkill",
            "",
            "### Security Considerations",
            "- UAC (User Account Control)",
            "- Execution policy (Set-ExecutionPolicy)",
            "- Administrator privileges",
            "- Windows Defender",
            "- Firewall rules",
            "",
            "### When Working with Windows",
            "- Use PowerShell for complex tasks",
            "- Use CMD for simple operations",
            "- Respect Windows file system conventions",
            "- Handle backslashes correctly in paths",
            "- Consider UAC and permissions",
            "- Use proper Windows line endings",
        ]

    def get_capabilities(self) -> list[str]:
        return [
            "powershell",
            "cmd",
            "windows_registry",
            "windows_services",
            "active_directory",
            "windows_filesystem",
            "windows_networking",
            "windows_security",
            "batch_scripts",
            "powershell_scripts",
        ]


module = CogOSWindows()
