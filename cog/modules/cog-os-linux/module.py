from cog.cog_module import CogModule
from cog.tools.base import Tool, ToolResult


class LinuxPackageTool(Tool):
    name = "linux.package"
    description = "Manage Linux packages (apt/yum/dnf/pacman)"
    required_permissions = ["shell.execute"]

    def execute(self, action: str, package: str = "", **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        distro = self._detect_distro()
        
        if distro in ["ubuntu", "debian"]:
            cmd = self._apt_command(action, package)
        elif distro in ["centos", "rhel", "fedora"]:
            cmd = self._yum_command(action, package)
        elif distro == "arch":
            cmd = self._pacman_command(action, package)
        else:
            cmd = f"echo 'Unknown distribution'"
        
        result = shell.execute(command=cmd, timeout=300)
        return result

    def _detect_distro(self) -> str:
        from cog.tools.shell import ShellTool
        shell = ShellTool()
        result = shell.execute(command="cat /etc/os-release | grep ID_LIKE", timeout=5)
        output = result.output or ""
        
        if "debian" in output.lower():
            return "debian"
        elif "ubuntu" in output.lower():
            return "ubuntu"
        elif "rhel" in output.lower() or "centos" in output.lower():
            return "centos"
        elif "fedora" in output.lower():
            return "fedora"
        return "unknown"

    def _apt_command(self, action: str, package: str) -> str:
        if action == "install":
            return f"sudo apt-get install -y {package}"
        elif action == "remove":
            return f"sudo apt-get remove -y {package}"
        elif action == "update":
            return "sudo apt-get update"
        elif action == "upgrade":
            return "sudo apt-get upgrade -y"
        return f"apt-get {action} {package}"

    def _yum_command(self, action: str, package: str) -> str:
        if action == "install":
            return f"sudo yum install -y {package}"
        elif action == "remove":
            return f"sudo yum remove -y {package}"
        elif action == "update":
            return "sudo yum update -y"
        elif action == "upgrade":
            return "sudo yum upgrade -y"
        return f"yum {action} {package}"

    def _pacman_command(self, action: str, package: str) -> str:
        if action == "install":
            return f"sudo pacman -S {package}"
        elif action == "remove":
            return f"sudo pacman -R {package}"
        elif action == "update":
            return "sudo pacman -Syu"
        return f"pacman {action} {package}"


class SystemdTool(Tool):
    name = "linux.systemd"
    description = "Manage systemd services"
    required_permissions = ["shell.execute"]

    def execute(self, action: str, service: str, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        command = f"sudo systemctl {action} {service}"
        result = shell.execute(command=command, timeout=60)
        return result


class LinuxProcessTool(Tool):
    name = "linux.process"
    description = "Manage Linux processes"
    required_permissions = ["shell.execute"]

    def execute(self, action: str, target: str, **kwargs) -> ToolResult:
        from cog.tools.shell import ShellTool

        shell = ShellTool()
        
        if action == "list":
            command = "ps aux"
        elif action == "kill":
            command = f"kill {target}"
        elif action == "tree":
            command = "pstree"
        else:
            command = f"{action} {target}"
        
        result = shell.execute(command=command, timeout=30)
        return result


class CogOSLinux(CogModule):
    name = "cog-os-linux"
    version = "1.0.0"
    description = "Linux operating system expertise"

    def register_tools(self) -> list[Tool]:
        return [
            LinuxPackageTool(),
            SystemdTool(),
            LinuxProcessTool(),
        ]

    def get_prompt_extensions(self) -> list[str]:
        return [
            "## Linux Operating System Expertise",
            "",
            "You understand Linux operating systems including:",
            "",
            "### Shell (Bash/Zsh)",
            "- Bash scripting and syntax",
            "- Command chaining (&&, ||, ;)",
            "- Pipes and redirection",
            "- Variables and expansion",
            "- Functions and aliases",
            "- Shell configuration (.bashrc, .zshrc)",
            "- Environment variables",
            "",
            "### Linux Distributions",
            "",
            "**Debian/Ubuntu:**",
            "- apt, apt-get package management",
            "- dpkg for individual packages",
            "- /etc/apt/ configuration",
            "- .deb package files",
            "",
            "**Red Hat/CentOS/Fedora:**",
            "- yum, dnf package management",
            "- rpm for individual packages",
            "- /etc/yum.repos.d/ configuration",
            "- .rpm package files",
            "",
            "**Arch Linux:**",
            "- pacman package management",
            "- AUR (Arch User Repository)",
            "- /etc/pacman.conf/ configuration",
            "",
            "### File System",
            "- Root directory /",
            "- Home directories /home/user/",
            "- /etc for configuration",
            "- /var for variable data",
            "- /usr for programs",
            "- /opt for optional software",
            "- Unix permissions (chmod, chown)",
            "- Symbolic links (ln -s)",
            "- Hard links",
            "- Extended attributes",
            "",
            "### systemd (Service Management)",
            "- systemctl start/stop/restart",
            "- systemctl enable/disable",
            "- systemctl status",
            "- journalctl for logs",
            "- service files in /etc/systemd/system/",
            "",
            "### Package Management",
            "",
            "**Debian/Ubuntu:**",
            "- apt-get update (update package lists)",
            "- apt-get upgrade (upgrade packages)",
            "- apt-get install (install packages)",
            "- apt-get remove (remove packages)",
            "- dpkg -i (install .deb file)",
            "",
            "**Red Hat/CentOS/Fedora:**",
            "- yum update/update",
            "- yum install/remove",
            "- rpm -ivh (install .rpm file)",
            "- dnf (modern alternative to yum)",
            "",
            "**Arch Linux:**",
            "- pacman -Syu (sync, refresh, upgrade)",
            "- pacman -S (install)",
            "- pacman -R (remove)",
            "",
            "### User Management",
            "- useradd/adduser",
            "- usermod/modify user",
            "- userdel/delete user",
            "- /etc/passwd, /etc/shadow",
            "- Groups (groupadd, groupmod)",
            "- /etc/group",
            "- sudo configuration",
            "- visudo",
            "",
            "### Permissions",
            "- chmod (change mode)",
            "- chown (change owner)",
            "- chgrp (change group)",
            "- umask (default permissions)",
            "- sudo (execute as root)",
            "- su (switch user)",
            "",
            "### Process Management",
            "- ps (processes)",
            "- top/htop (process viewer)",
            "- kill (send signal)",
            "- killall (kill by name)",
            "- pkill (kill by pattern)",
            "- pgrep (find process)",
            "- nice/renice (priority)",
            "- nohup (ignore HUP)",
            "- & (background)",
            "",
            "### Networking",
            "- ip addr/ifconfig (interfaces)",
            "- ip route/route (routing)",
            "- ping (ICMP echo)",
            "- traceroute/traceroute (trace path)",
            "- netstat/ss (network stats)",
            "- ssh (secure shell)",
            "- scp/ rsync (copy)",
            "- wget/curl (download)",
            "- iptables (firewall)",
            "",
            "### Logs and Monitoring",
            "- journalctl (systemd logs)",
            "- /var/log/ (log files)",
            "- tail -f (follow logs)",
            "- grep (search logs)",
            "- dmesg (kernel messages)",
            "",
            "### Cron (Scheduled Tasks)",
            "- crontab -e (edit cron)",
            "- cron format (min hour day month dow)",
            "- /etc/cron.d/ (system cron)",
            "- systemctl status cron",
            "",
            "### Linux-Specific Tools",
            "- grep/egrep/fgrep (search)",
            "- sed/awk (text processing)",
            "- find/locate (search files)",
            "- tar/zip/gzip (archives)",
            "- ssh-keygen (SSH keys)",
            "- scp (secure copy)",
            "- rsync (sync files)",
            "- screen/tmux (terminal multiplexer)",
            "- man (manual pages)",
            "",
            "### When Working with Linux",
            "- Use absolute paths when scripting",
            "- Quote variables to prevent word splitting",
            "- Check command exit codes",
            "- Use sudo for root operations",
            "- Understand distribution differences",
            "- Respect the Unix philosophy",
            "- Use man pages for documentation",
            "- Test commands before production",
            "",
            "### Common Tasks",
            "",
            "Update system:",
            "- Debian: sudo apt-get update && sudo apt-get upgrade",
            "- Red Hat: sudo yum update",
            "- Arch: sudo pacman -Syu",
            "",
            "Install packages:",
            "- Debian: sudo apt-get install package",
            "- Red Hat: sudo yum install package",
            "- Arch: sudo pacman -S package",
            "",
            "Manage services:",
            "- sudo systemctl start service",
            "- sudo systemctl stop service",
            "- sudo systemctl restart service",
            "- sudo systemctl enable service (auto-start)",
            "",
            "Check logs:",
            "- journalctl -u service (specific service)",
            "- journalctl -f (follow logs)",
            "- tail -f /var/log/syslog",
            "",
            "Process management:",
            "- ps aux | grep process",
            "- kill PID",
            "- killall processname",
            "",
            "File permissions:",
            "- chmod +x script.sh (executable)",
            "- chmod 644 file (rw-r--r--)",
            "- chown user:group file",
            "",
            "Network troubleshooting:",
            "- ping host",
            "- traceroute host",
            "- mtr host (ping + traceroute)",
            "- netstat -tulpn (listening ports)",
            "- ss -tulpn (modern netstat)",
            "",
            "### Security Considerations",
            "- Use sudo sparingly",
            "- Keep system updated",
            "- Use strong passwords",
            "- Configure firewall (iptables/ufw)",
            "- Disable root SSH login",
            "- Use SSH keys instead of passwords",
            "- Monitor logs for suspicious activity",
            "- Regular security audits",
            "",
            "### Distribution-Specific Notes",
            "",
            "**Ubuntu/Debian:**",
            "- Use apt for package management",
            "- Non-free drivers in restricted repository",
            "- PPA for third-party software",
            "",
            "**CentOS/RHEL:**",
            "- Use yum/dnf for packages",
            "- SELinux enabled by default",
            "- firewalld for firewall management",
            "- EPEL repository for extra packages",
            "",
            "**Arch Linux:**",
            "- Rolling release model",
            "- AUR for community packages",
            "- Pacman is fast but unforgiving",
            "- Wiki is excellent documentation",
            "",
            "**Fedora:**",
            "- Cutting-edge software",
            "- dnf (newer than yum)",
            "- Wayland by default",
            "- SELinux enabled",
        ]

    def get_capabilities(self) -> list[str]:
        return [
            "bash_scripting",
            "linux_command_line",
            "package_management",
            "systemd_services",
            "process_management",
            "user_management",
            "permissions",
            "linux_networking",
            "log_management",
            "cron_scheduling",
            "ubuntu_debian",
            "centos_rhel",
            "fedora",
            "arch_linux",
            "shell_scripting",
            "linux_security",
            "linux_troubleshooting",
        ]


module = CogOSLinux()
