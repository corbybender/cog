from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult


class HomebrewTool(Tool):
    name = "macos.homebrew"
    description = "Manage packages with Homebrew"
    required_permissions = ["shell.execute"]

    def execute(self, action: str, package: str = "", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        if package:
            command = f"brew {action} {package}"
        else:
            command = f"brew {action}"
        result = shell.execute(command=command, timeout=300)
        return result


class MacOSTool(Tool):
    name = "macos.defaults"
    description = "Manage macOS defaults system"
    required_permissions = ["shell.execute"]

    def execute(self, domain: str, key: str, value: str = "", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        if value:
            command = f"defaults write {domain} {key} {value}"
        else:
            command = f"defaults read {domain} {key}"
        result = shell.execute(command=command, timeout=30)
        return result


class SpotlightTool(Tool):
    name = "macos.spotlight"
    description = "Search files using Spotlight"
    required_permissions = ["shell.execute"]

    def execute(self, query: str, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"mdfind '{query}'"
        result = shell.execute(command=command, timeout=60)
        return result


class CogOSMac(CogModule):
    name = "cog-os-mac"
    version = "1.0.0"
    description = "macOS operating system expertise"

    def register_tools(self) -> list[Tool]:
        return [
            HomebrewTool(),
            MacOSTool(),
            SpotlightTool(),
        ]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## macOS Operating System Expertise",
            "",
            "You understand macOS including:",
            "",
            "### Shell (Zsh is default in macOS Catalina+)",
            "- Zsh syntax and features",
            "- Oh My Zsh framework",
            "- Zsh plugins and themes",
            "- Bash compatibility",
            "- Shell configuration (.zshrc, .bash_profile)",
            "- Environment variables",
            "- Path management",
            "",
            "### Homebrew Package Manager",
            "- brew install (install packages)",
            "- brew uninstall (remove packages)",
            "- brew update (update formulas)",
            "- brew upgrade (upgrade packages)",
            "- brew list (installed packages)",
            "- brew search (find packages)",
            "- brew services (manage services)",
            "- caskroom (GUI applications)",
            "",
            "### macOS File System",
            "- Root directory /",
            "- User home ~ (/Users/username)",
            "- Desktop ~/Desktop",
            "- Documents ~/Documents",
            "- Applications /Applications",
            "- Unix-style permissions",
            "- Case-insensitive by default",
            "- Extended attributes (@)",
            "- Resource forks",
            "",
            "### macOS-Specific Tools",
            "- defaults (read/write preferences)",
            "- mdfind (Spotlight search)",
            "- mdls (metadata attributes)",
            "- open (open files/URLs)",
            "- pbcopy/pbpaste (clipboard)",
            "- screencapture (screenshots)",
            "- diskutil (disk management)",
            "- pmset (power management)",
            "",
            "### Development on macOS",
            "- Xcode and Command Line Tools",
            "- xcode-select (developer tools)",
            "- Homebrew for development tools",
            "- Node.js, Python, Ruby via brew",
            "- Git via brew or Xcode",
            "",
            "### macOS Services",
            "- launchctl (manage services)",
            "- launchd (service daemon)",
            "- Service management",
            "- Startup items",
            "",
            "### macOS Networking",
            "- ifconfig (network interfaces)",
            "- netstat (network statistics)",
            "- ping (network connectivity)",
            "- ssh (remote login)",
            "- scp (secure copy)",
            "",
            "### macOS Security",
            "- Gatekeeper (app security)",
            "- SIP (System Integrity Protection)",
            "- FileVault (disk encryption)",
            "- Keychain (password management)",
            "- Codesigning",
            "",
            "### macOS-Specific Patterns",
            "",
            "File operations:",
            "- Open: open file.txt",
            "- Copy to clipboard: cat file.txt | pbcopy",
            "- Paste from clipboard: pbpaste > file.txt",
            "- Screenshot: screencapture -x screen.png",
            "",
            "Development setup:",
            "- Install Xcode: xcode-select --install",
            "- Install brew: /bin/bash -c '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'",
            "- Install Node: brew install node",
            "",
            "### When Working with macOS",
            "- Use Zsh by default (check with echo $SHELL)",
            "- Use open command to open files",
            "- Use defaults for system preferences",
            "- Use Homebrew for package management",
            "- Respect macOS file system conventions",
            "- Consider case-insensitive filesystem",
            "- Use Unix-style paths",
            "- Be aware of extended attributes",
            "- Understand Gatekeeper and SIP",
        ]

    def get_capabilities(self) -> list[str]:
        return [
            "zsh",
            "bash",
            "homebrew",
            "macos_defaults",
            "spotlight",
            "macos_services",
            "xcode_tools",
            "macos_development",
            "macos_filesystem",
            "macos_networking",
            "keychain_access",
            "codesigning",
        ]


module = CogOSMac()
