#!/usr/bin/env python3
"""
Linux Tools Installer - Desktop Edition
Installs tools from README.md with proper system checks and user consent.
"""

import subprocess
import os
import sys
import shutil
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class InstallMethod(Enum):
    """Installation methods for tools."""
    APT = "apt"
    PIP = "pip"
    EGET = "eget"
    SNAP = "snap"
    BUILTIN = "builtin"  # Already available (e.g., systemctl)
    MANUAL = "manual"  # Requires manual installation


@dataclass
class Tool:
    """Tool definition with installation details."""
    name: str
    command: str  # Command to check if installed
    method: InstallMethod
    package: str  # Package name for installation
    description: str
    category: str
    requires_root: bool = True
    github_repo: Optional[str] = None  # For eget installations
    classic: bool = False  # For snap installations


class SystemChecker:
    """Check system compatibility and requirements."""
    
    @staticmethod
    def is_debian_like() -> bool:
        """Check if system is Debian-based."""
        return shutil.which("apt-get") is not None
    
    @staticmethod
    def is_root() -> bool:
        """Check if running as root."""
        return os.geteuid() == 0
    
    @staticmethod
    def has_command(command: str) -> bool:
        """Check if command exists in PATH."""
        return shutil.which(command) is not None
    
    @staticmethod
    def check_system() -> Tuple[bool, Optional[str]]:
        """Comprehensive system check."""
        if not SystemChecker.is_debian_like():
            return False, "This script requires a Debian-based system (Ubuntu, Debian, Linux Mint)"
        
        if not SystemChecker.has_command("sudo"):
            return False, "sudo is required but not found"
        
        return True, None


class Installer:
    """Handle tool installation with different methods."""
    
    @staticmethod
    def run_command(cmd: List[str], check: bool = False, capture_output: bool = False, timeout: int = 30) -> subprocess.CompletedProcess:
        """Run command with proper error handling and timeout."""
        try:
            return subprocess.run(
                cmd,
                check=check,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
        except subprocess.TimeoutExpired:
            print(f"Command timed out after {timeout}s: {' '.join(cmd)}")
            return subprocess.CompletedProcess(cmd, 124)  # 124 is timeout exit code
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {' '.join(cmd)}")
            print(f"Error: {e}")
            return e
        except FileNotFoundError:
            print(f"Command not found: {cmd[0]}")
            return subprocess.CompletedProcess(cmd, 1)
    
    @staticmethod
    def install_via_apt(package: str) -> bool:
        """Install package via apt-get."""
        print(f"Installing {package} via apt...")
        result = Installer.run_command(
            ["sudo", "apt-get", "install", "-y", package],
            capture_output=True
        )
        return result.returncode == 0
    
    @staticmethod
    def install_via_pip(package: str) -> bool:
        """Install package via pip3."""
        print(f"Installing {package} via pip3...")
        result = Installer.run_command(
            ["pip3", "install", "--user", package],
            capture_output=True
        )
        return result.returncode == 0
    
    @staticmethod
    def install_via_snap(package: str, classic: bool = False) -> bool:
        """Install package via snap."""
        print(f"Installing {package} via snap...")
        cmd = ["sudo", "snap", "install"]
        if classic:
            cmd.append("--classic")
        cmd.append(package)
        result = Installer.run_command(cmd, capture_output=True)
        return result.returncode == 0
    
    @staticmethod
    def install_via_eget(repo: str, binary_name: str) -> bool:
        """Install package via eget from GitHub."""
        if not SystemChecker.has_command("eget"):
            print("eget not found, installing eget first...")
            if not Installer.install_eget():
                return False
        
        print(f"Installing {binary_name} via eget from {repo}...")
        result = Installer.run_command(
            ["eget", repo],
            capture_output=True
        )
        
        if result.returncode == 0 and os.path.exists(binary_name):
            # Move to /usr/local/bin (better than /usr/bin for user-installed tools)
            move_cmd = ["sudo", "mv", binary_name, "/usr/local/bin/"]
            move_result = Installer.run_command(move_cmd)
            return move_result.returncode == 0
        return False
    
    @staticmethod
    def install_eget() -> bool:
        """Install eget if not present."""
        print("Installing eget...")
        result = Installer.run_command(
            ["sh", "-c", "curl --connect-timeout 10 --max-time 30 https://zyedidia.github.io/eget.sh | sh"],
            capture_output=True,
            timeout=60  # Longer timeout for network operations
        )
        
        if result.returncode == 0 and os.path.exists("eget"):
            move_result = Installer.run_command(["sudo", "mv", "eget", "/usr/local/bin/"])
            return move_result.returncode == 0
        return False
    
    @staticmethod
    def install_croc() -> bool:
        """Install croc using official installer."""
        print("Installing croc...")
        result = Installer.run_command(
            ["sh", "-c", "curl --connect-timeout 10 --max-time 60 https://getcroc.schollz.com | bash"],
            capture_output=True,
            timeout=120  # Longer timeout for network operations
        )
        return result.returncode == 0
    
    @staticmethod
    def check_apt_available(package: str) -> bool:
        """Check if package is available in apt repositories."""
        result = Installer.run_command(
            ["apt-cache", "search", "--names-only", "^" + package + "$"],
            capture_output=True
        )
        return result.returncode == 0 and package in result.stdout


class ToolManager:
    """Manage tool definitions and installation."""
    
    # Define all tools from README.md
    TOOLS: Dict[str, Tool] = {
        # Desktop GUI Apps
        "geany": Tool("geany", "geany", InstallMethod.APT, "geany",
                     "GUI editor like notepad++", "Desktop GUI Apps"),
        "wireshark": Tool("wireshark", "wireshark", InstallMethod.APT, "wireshark",
                         "Network packet reviewer", "Desktop GUI Apps"),
        "code": Tool("code", "code", InstallMethod.SNAP, "code",
                    "Visual Studio Code", "Desktop GUI Apps", classic=True),
        "guake": Tool("guake", "guake", InstallMethod.APT, "guake",
                     "GUI terminal client", "Desktop GUI Apps"),
        "tabby": Tool("tabby", "tabby", InstallMethod.EGET, "tabby",
                     "Modern terminal emulator", "Desktop GUI Apps",
                     github_repo="Eugeny/tabby"),
        
        # Terminal File Explorers
        "xplr": Tool("xplr", "xplr", InstallMethod.EGET, "xplr",
                    "Very graphical file explorer", "Terminal File Explorers",
                    github_repo="sayanarijit/xplr"),
        "nnn": Tool("nnn", "nnn", InstallMethod.APT, "nnn",
                   "Efficient file explorer", "Terminal File Explorers"),
        "lf": Tool("lf", "lf", InstallMethod.EGET, "lf",
                  "Cross-platform file explorer", "Terminal File Explorers",
                  github_repo="gokcehan/lf"),
        
        # LS-like Directory Viewers
        "eza": Tool("eza", "eza", InstallMethod.EGET, "eza",
                   "Modern ls replacement (exa successor)", "LS-like Directory Viewers",
                   github_repo="eza-community/eza"),
        "lsd": Tool("lsd", "lsd", InstallMethod.EGET, "lsd",
                   "ls clone with icons", "LS-like Directory Viewers",
                   github_repo="Peltoche/lsd"),
        
        # Text Editors and Viewers
        "micro": Tool("micro", "micro", InstallMethod.EGET, "micro",
                     "User-friendly terminal editor", "Text Editors and Viewers",
                     github_repo="zyedidia/micro"),
        "ne": Tool("ne", "ne", InstallMethod.APT, "ne",
                  "Terminal editor like nano", "Text Editors and Viewers"),
        "vim": Tool("vim", "vim", InstallMethod.APT, "vim",
                   "VI editor with extras", "Text Editors and Viewers"),
        "nvim": Tool("nvim", "nvim", InstallMethod.APT, "neovim",
                    "Modern vim alternative", "Text Editors and Viewers"),
        "bat": Tool("bat", "batcat", InstallMethod.APT, "bat",
                   "cat clone with syntax highlighting", "Text Editors and Viewers"),
        
        # Process Explorers
        "glances": Tool("glances", "glances", InstallMethod.PIP, "glances",
                       "System info in one glance", "Process Explorers"),
        "htop": Tool("htop", "htop", InstallMethod.APT, "htop",
                    "Supercharged top clone", "Process Explorers"),
        "btop": Tool("btop", "btop", InstallMethod.EGET, "btop",
                    "TUI CLI graphics process monitor", "Process Explorers",
                    github_repo="aristocratos/btop"),
        "bottom": Tool("bottom", "btm", InstallMethod.EGET, "btm",
                      "btop-inspired process monitor", "Process Explorers",
                      github_repo="ClementTsang/bottom"),
        
        # Network-Related Apps
        "croc": Tool("croc", "croc", InstallMethod.MANUAL, "croc",
                    "Secure file transfer", "Network-Related Apps"),
        "network-manager": Tool("nmtui", "nmtui", InstallMethod.APT, "network-manager",
                               "Terminal Network Manager", "Network-Related Apps"),
        "hping3": Tool("hping3", "hping3", InstallMethod.APT, "hping3",
                      "Advanced ping tool", "Network-Related Apps"),
        "nmap": Tool("nmap", "nmap", InstallMethod.APT, "nmap",
                    "Network scanner", "Network-Related Apps"),
        "bmon": Tool("bmon", "bmon", InstallMethod.APT, "bmon",
                    "TUI network bandwidth monitor", "Network-Related Apps"),
        "mtr": Tool("mtr", "mtr", InstallMethod.APT, "mtr-tiny",
                   "Traceroute and ping combined", "Network-Related Apps"),
        "gping": Tool("gping", "gping", InstallMethod.EGET, "gping",
                     "Ping with graph", "Network-Related Apps",
                     github_repo="orf/gping"),
        "dog": Tool("dog", "dog", InstallMethod.EGET, "dog",
                   "Modern dig alternative", "Network-Related Apps",
                   github_repo="ogham/dog"),
        "neoss": Tool("neoss", "neoss", InstallMethod.EGET, "neoss",
                     "Modern ss alternative", "Network-Related Apps",
                     github_repo="PabloLec/neoss"),
        
        # Misc CLI Terminal Apps
        "systemctl": Tool("systemctl", "systemctl", InstallMethod.BUILTIN, "systemd",
                         "Built-in systemd service manager", "Misc CLI Terminal Apps",
                         requires_root=False),
        "ncdu": Tool("ncdu", "ncdu", InstallMethod.APT, "ncdu",
                    "Terminal disk space viewer", "Misc CLI Terminal Apps"),
        "dust": Tool("dust", "dust", InstallMethod.EGET, "dust",
                    "Intuitive du with bar charts", "Misc CLI Terminal Apps",
                    github_repo="bootandy/dust"),
        "duf": Tool("duf", "duf", InstallMethod.EGET, "duf",
                   "Disk utility with graphs", "Misc CLI Terminal Apps",
                   github_repo="muesli/duf"),
        "lynis": Tool("lynis", "lynis", InstallMethod.APT, "lynis",
                     "Linux security auditing", "Misc CLI Terminal Apps"),
        "apt-show-versions": Tool("apt-show-versions", "apt-show-versions",
                                 InstallMethod.APT, "apt-show-versions",
                                 "Show package versions", "Misc CLI Terminal Apps"),
        "nala": Tool("nala", "nala", InstallMethod.APT, "nala",
                    "User-friendly apt frontend", "Misc CLI Terminal Apps"),
        "fd": Tool("fd", "fdfind", InstallMethod.APT, "fd-find",
                  "Fast find alternative", "Misc CLI Terminal Apps"),
        "fish": Tool("fish", "fish", InstallMethod.APT, "fish",
                    "Friendly interactive shell", "Misc CLI Terminal Apps"),
        "starship": Tool("starship", "starship", InstallMethod.EGET, "starship",
                        "Customizable shell prompt", "Misc CLI Terminal Apps",
                        github_repo="starship/starship"),
        "zoxide": Tool("zoxide", "zoxide", InstallMethod.EGET, "zoxide",
                      "Smarter cd command", "Misc CLI Terminal Apps",
                      github_repo="ajeetdsouza/zoxide"),
        "atuin": Tool("atuin", "atuin", InstallMethod.EGET, "atuin",
                     "Magical shell history", "Misc CLI Terminal Apps",
                     github_repo="atuinsh/atuin"),
        "tig": Tool("tig", "tig", InstallMethod.APT, "tig",
                   "TUI git client", "Misc CLI Terminal Apps"),
        "lazygit": Tool("lazygit", "lazygit", InstallMethod.EGET, "lazygit",
                       "Simple terminal UI for git", "Misc CLI Terminal Apps",
                       github_repo="jesseduffield/lazygit"),
        "delta": Tool("delta", "delta", InstallMethod.EGET, "delta",
                     "Syntax-highlighting git pager", "Misc CLI Terminal Apps",
                     github_repo="dandavison/delta"),
        "miller": Tool("miller", "mlr", InstallMethod.APT, "miller",
                     "JSON/CSV processor", "Misc CLI Terminal Apps"),
        "most": Tool("most", "most", InstallMethod.APT, "most",
                    "Better pager than less/more", "Misc CLI Terminal Apps"),
        "tldr": Tool("tldr", "tldr", InstallMethod.PIP, "tldr",
                    "Simplified man pages", "Misc CLI Terminal Apps"),
        "lazydocker": Tool("lazydocker", "lazydocker", InstallMethod.EGET, "lazydocker",
                         "TUI Docker manager", "Misc CLI Terminal Apps",
                         github_repo="jesseduffield/lazydocker"),
        "json-tui": Tool("json-tui", "json-tui", InstallMethod.EGET, "json-tui",
                        "JSON file viewer", "Misc CLI Terminal Apps",
                        github_repo="ArthurSonzogni/json-tui"),
        "jc": Tool("jc", "jc", InstallMethod.APT, "jc",
                  "Parse command output to JSON", "Misc CLI Terminal Apps"),
        "visidata": Tool("visidata", "visidata", InstallMethod.PIP, "visidata",
                        "CSV/data viewer", "Misc CLI Terminal Apps"),
        "eg": Tool("eg", "eg", InstallMethod.EGET, "eg",
                  "TLDR-like command helper", "Misc CLI Terminal Apps",
                  github_repo="srsudar/eg"),
        "procs": Tool("procs", "procs", InstallMethod.EGET, "procs",
                     "Modern ps replacement", "Misc CLI Terminal Apps",
                     github_repo="dalance/procs"),
        "sd": Tool("sd", "sd", InstallMethod.EGET, "sd",
                  "Modern sed replacement", "Misc CLI Terminal Apps",
                  github_repo="chmln/sd"),
        "ripgrep": Tool("ripgrep", "rg", InstallMethod.APT, "ripgrep",
                       "Fast text search tool", "Misc CLI Terminal Apps"),
        "ripgrep-all": Tool("ripgrep-all", "rga", InstallMethod.EGET, "rga",
                           "ripgrep for all file types", "Misc CLI Terminal Apps",
                           github_repo="phiresky/ripgrep-all"),
        "fzf": Tool("fzf", "fzf", InstallMethod.APT, "fzf",
                   "Command-line fuzzy finder", "Misc CLI Terminal Apps"),
        "fastfetch": Tool("fastfetch", "fastfetch", InstallMethod.EGET, "fastfetch",
                         "System info display", "Misc CLI Terminal Apps",
                         github_repo="fastfetch-cli/fastfetch"),
        "pandoc": Tool("pandoc", "pandoc", InstallMethod.APT, "pandoc",
                      "Document converter", "Misc CLI Terminal Apps"),
        "hyperfine": Tool("hyperfine", "hyperfine", InstallMethod.EGET, "hyperfine",
                         "Command benchmarking tool", "Misc CLI Terminal Apps",
                         github_repo="sharkdp/hyperfine"),
        "just": Tool("just", "just", InstallMethod.EGET, "just",
                    "Command runner (make alternative)", "Misc CLI Terminal Apps",
                    github_repo="casey/just"),
    }
    
    @staticmethod
    def get_tools_by_category() -> Dict[str, List[Tool]]:
        """Group tools by category."""
        categories: Dict[str, List[Tool]] = {}
        for tool in ToolManager.TOOLS.values():
            if tool.category not in categories:
                categories[tool.category] = []
            categories[tool.category].append(tool)
        return categories
    
    @staticmethod
    def check_tool_installed(tool: Tool) -> bool:
        """Check if tool is installed."""
        return SystemChecker.has_command(tool.command)
    
    @staticmethod
    def install_tool(tool: Tool) -> bool:
        """Install a tool using its defined method."""
        if tool.method == InstallMethod.BUILTIN:
            print(f"✓ {tool.name} is built-in (no installation needed)")
            return True
        
        if tool.method == InstallMethod.APT:
            if Installer.check_apt_available(tool.package):
                return Installer.install_via_apt(tool.package)
            else:
                print(f"⚠ {tool.name} not available in apt repositories")
                return False
        
        elif tool.method == InstallMethod.PIP:
            return Installer.install_via_pip(tool.package)
        
        elif tool.method == InstallMethod.SNAP:
            return Installer.install_via_snap(tool.package, classic=tool.classic)
        
        elif tool.method == InstallMethod.EGET:
            if tool.github_repo:
                return Installer.install_via_eget(tool.github_repo, tool.command)
            else:
                print(f"⚠ {tool.name} missing GitHub repository information")
                return False
        
        elif tool.method == InstallMethod.MANUAL:
            if tool.name == "croc":
                return Installer.install_croc()
            print(f"⚠ {tool.name} requires manual installation")
            return False
        
        return False


def get_user_consent() -> bool:
    """Get user consent once upfront."""
    print("\n" + "="*70)
    print("Linux Tools Installer - Desktop Edition")
    print("="*70)
    print("\nThis script will check and install Linux tools from README.md")
    print("You will be prompted for sudo password when needed.")
    print("\nThe script will:")
    print("  • Check which tools are already installed")
    print("  • Install missing tools using appropriate methods (apt, pip, eget, snap)")
    print("  • Skip tools that are already installed")
    print("\n" + "="*70)
    
    max_attempts = 5
    attempts = 0
    
    while attempts < max_attempts:
        try:
            response = input("\nDo you want to proceed? [y/N]: ").strip().lower()
            if response in ('y', 'yes'):
                return True
            elif response in ('n', 'no', ''):
                return False
            else:
                attempts += 1
                if attempts < max_attempts:
                    print("Please enter 'y' for yes or 'n' for no")
                else:
                    print("Maximum attempts reached. Defaulting to 'no'.")
                    return False
        except (EOFError, KeyboardInterrupt):
            print("\n\nInterrupted by user. Exiting.")
            return False
    
    return False


def update_package_lists() -> bool:
    """Update apt package lists."""
    print("\nUpdating package lists...")
    result = Installer.run_command(
        ["sudo", "apt-get", "update"],
        capture_output=True
    )
    return result.returncode == 0


def main():
    """Main execution function."""
    # System check
    is_compatible, error_msg = SystemChecker.check_system()
    if not is_compatible:
        print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # Get user consent
    if not get_user_consent():
        print("\nInstallation cancelled by user.")
        sys.exit(0)
    
    # Update package lists
    update_package_lists()
    
    # Get tools by category for better organization
    tools_by_category = ToolManager.get_tools_by_category()
    
    # Track installation results
    installed_count = 0
    skipped_count = 0
    failed_count = 0
    
    print("\n" + "="*70)
    print("Checking and installing tools...")
    print("="*70 + "\n")
    
    # Process tools by category
    for category, tools in tools_by_category.items():
        print(f"\n[{category}]")
        print("-" * 70)
        
        for tool in sorted(tools, key=lambda t: t.name):
            if ToolManager.check_tool_installed(tool):
                print(f"✓ {tool.name:30} - Already installed")
                skipped_count += 1
            else:
                print(f"✗ {tool.name:30} - Not installed, installing...")
                if ToolManager.install_tool(tool):
                    print(f"  ✓ {tool.name} installed successfully")
                    installed_count += 1
                else:
                    print(f"  ✗ {tool.name} installation failed")
                    failed_count += 1
    
    # Summary
    print("\n" + "="*70)
    print("Installation Summary")
    print("="*70)
    print(f"Already installed: {skipped_count}")
    print(f"Newly installed:   {installed_count}")
    print(f"Failed:            {failed_count}")
    print("="*70)
    
    if failed_count > 0:
        print("\nSome tools failed to install. Check the output above for details.")
        print("Some tools may require manual installation or different methods.")
    
    input("\nPress Enter to exit...")
    sys.exit(0)


if __name__ == "__main__":
    main()
