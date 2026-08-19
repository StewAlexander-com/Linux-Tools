#!/usr/bin/env python3
"""
Lazy Linux Tool Installer
Automatically installs all Linux tools from README.md - perfect for lazy users!
Just run it and it handles everything: checking, installing, and organizing tools.
"""

import subprocess
import os
import sys
import shutil
import argparse
import hashlib
import json
import platform
import tempfile
import tarfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Network / command timeouts (seconds). Generous defaults for slow links.
CONNECT_TIMEOUT = 30
DOWNLOAD_MAX_TIME = 120
NETWORK_CMD_TIMEOUT = 180
DEFAULT_CMD_TIMEOUT = 60
VALIDATE_CMD_TIMEOUT = 20
INSTALL_BIN_DIR = "/usr/local/bin"
ELF_MAGIC = b"\x7fELF"
# Official eget.sh checksum from upstream README (may lag script updates).
# Prefer GitHub release binaries over the bootstrap script for this reason.
EGET_GITHUB_REPO = "zyedidia/eget"


class InstallMethod(Enum):
    """Installation methods for tools."""
    APT = "apt"
    PIP = "pip"
    EGET = "eget"
    SNAP = "snap"
    NPM = "npm"
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
    requires_gui: bool = False  # Whether tool requires GUI (excluded in server mode)


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

        if not SystemChecker.has_command("curl"):
            return False, "curl is required but not found"
        
        return True, None


class Installer:
    """Handle tool installation with different methods."""
    
    @staticmethod
    def run_command(cmd: List[str], check: bool = False, capture_output: bool = False, timeout: int = DEFAULT_CMD_TIMEOUT) -> subprocess.CompletedProcess:
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
            # Return CompletedProcess with timeout exit code (124) to avoid crashes
            print(f"Command timed out after {timeout}s: {' '.join(cmd)}")
            return subprocess.CompletedProcess(cmd, 124)
        except subprocess.CalledProcessError as e:
            # Return CompletedProcess with actual error code for consistency
            print(f"Error running command: {' '.join(cmd)}")
            print(f"Error: {e}")
            return subprocess.CompletedProcess(cmd, e.returncode)
        except FileNotFoundError:
            # Command missing from PATH - use standard exit code 127
            print(f"Command not found: {cmd[0]}")
            return subprocess.CompletedProcess(cmd, 127)

    @staticmethod
    def linux_goarch() -> Optional[str]:
        """Map platform.machine() to Go/eget arch names."""
        machine = platform.machine().lower()
        arch_map = {
            "x86_64": "amd64",
            "amd64": "amd64",
            "aarch64": "arm64",
            "arm64": "arm64",
            "armv7l": "arm",
            "armv6l": "arm",
            "i386": "386",
            "i686": "386",
        }
        return arch_map.get(machine)

    @staticmethod
    def sha256_file(path: str) -> str:
        """Compute SHA-256 hex digest of a file."""
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def download_file(url: str, dest: str, timeout: int = NETWORK_CMD_TIMEOUT) -> bool:
        """Download URL to dest via curl (no pipe-to-shell)."""
        result = Installer.run_command(
            [
                "curl",
                "--fail",
                "--location",
                "--silent",
                "--show-error",
                "--connect-timeout", str(CONNECT_TIMEOUT),
                "--max-time", str(DOWNLOAD_MAX_TIME),
                "--output", dest,
                url,
            ],
            capture_output=True,
            timeout=timeout,
        )
        return result.returncode == 0 and os.path.isfile(dest) and os.path.getsize(dest) > 0

    @staticmethod
    def fetch_latest_release_assets(repo: str) -> Tuple[Optional[str], List[dict]]:
        """Return (tag_name, assets) from GitHub latest release API."""
        api_url = f"https://api.github.com/repos/{repo}/releases/latest"
        with tempfile.NamedTemporaryFile(prefix="gh-release-", suffix=".json", delete=False) as tmp:
            json_path = tmp.name
        try:
            if not Installer.download_file(api_url, json_path):
                print(f"Failed to fetch release metadata for {repo}")
                return None, []
            with open(json_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            return data.get("tag_name"), data.get("assets") or []
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            print(f"Failed to parse release metadata for {repo}: {exc}")
            return None, []
        finally:
            try:
                os.unlink(json_path)
            except OSError:
                pass

    @staticmethod
    def is_plausible_binary(path: str) -> bool:
        """Reject non-files and non-ELF / non-script downloads before privilege move."""
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            return False
        try:
            with open(path, "rb") as handle:
                magic = handle.read(4)
        except OSError:
            return False
        # Linux ELF binaries (typical eget/croc artifacts) or scripts with shebang
        return magic == ELF_MAGIC or magic.startswith(b"#!")

    @staticmethod
    def install_binary_to_path(src_path: str, binary_name: str) -> bool:
        """Validate binary, then install into /usr/local/bin."""
        if not Installer.is_plausible_binary(src_path):
            print(f"Refusing to install {binary_name}: failed binary sanity check")
            return False
        try:
            os.chmod(src_path, 0o755)
        except OSError as exc:
            print(f"Could not chmod {src_path}: {exc}")
            return False
        dest = os.path.join(INSTALL_BIN_DIR, binary_name)
        move_result = Installer.run_command(
            ["sudo", "mv", src_path, dest],
            capture_output=True,
        )
        if move_result.returncode != 0:
            return False
        return Installer.validate_installed_command(binary_name)

    @staticmethod
    def validate_installed_command(command: str) -> bool:
        """Confirm command is on PATH and responds to a version/help probe."""
        if not SystemChecker.has_command(command):
            # PATH may not include INSTALL_BIN_DIR in this process yet
            candidate = os.path.join(INSTALL_BIN_DIR, command)
            if not os.path.isfile(candidate):
                print(f"Post-install check failed: {command} not found in PATH")
                return False
            invoke = candidate
        else:
            invoke = command

        for flag in ("--version", "-V", "-v", "version", "--help", "-h"):
            result = Installer.run_command(
                [invoke, flag],
                capture_output=True,
                timeout=VALIDATE_CMD_TIMEOUT,
            )
            if result.returncode == 124:
                continue
            output = ((result.stdout or "") + (result.stderr or "")).strip()
            # Accept success, or help/version text even when exit code is non-zero
            if result.returncode == 0 or (output and result.returncode in (0, 1, 2)):
                print(f"  ✓ Verified {command} responds to '{flag}'")
                return True

        print(f"Post-install check failed: {command} did not respond to version/help probes")
        return False

    @staticmethod
    def verify_checksum(path: str, expected_hex: str) -> bool:
        """Compare file SHA-256 to expected hex digest."""
        expected = expected_hex.strip().lower()
        actual = Installer.sha256_file(path).lower()
        if actual != expected:
            print(f"Checksum mismatch for {path}")
            print(f"  expected: {expected}")
            print(f"  actual:   {actual}")
            return False
        return True

    @staticmethod
    def parse_checksums_file(content: str) -> Dict[str, str]:
        """Parse 'hash  filename' lines into {basename: hash}."""
        mapping: Dict[str, str] = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            digest, name = parts[0], parts[-1]
            # Allow "hash *filename" (binary mode marker)
            name = name.lstrip("*")
            mapping[os.path.basename(name)] = digest
        return mapping
    
    @staticmethod
    def install_via_apt(package: str) -> bool:
        """Install package via apt-get."""
        print(f"Installing {package} via apt...")
        result = Installer.run_command(
            ["sudo", "apt-get", "install", "-y", package],
            capture_output=True,
            timeout=NETWORK_CMD_TIMEOUT,
        )
        return result.returncode == 0
    
    @staticmethod
    def install_via_pip(package: str) -> bool:
        """Install package via pip3."""
        print(f"Installing {package} via pip3...")
        result = Installer.run_command(
            ["pip3", "install", "--user", package],
            capture_output=True,
            timeout=NETWORK_CMD_TIMEOUT,
        )
        return result.returncode == 0
    
    @staticmethod
    def install_via_npm(package: str) -> bool:
        """Install a global npm package, pulling in npm itself if it is absent.

        Node is not part of a base Debian install, so the one tool that ships
        this way would otherwise fail on a clean machine with a bare
        "npm: not found".
        """
        if not SystemChecker.has_command("npm"):
            print("npm not found, installing npm first...")
            if not Installer.install_via_apt("npm"):
                print("Could not install npm")
                return False
        print(f"Installing {package} via npm...")
        result = Installer.run_command(
            ["sudo", "npm", "install", "-g", package],
            capture_output=True,
            timeout=NETWORK_CMD_TIMEOUT,
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
        result = Installer.run_command(cmd, capture_output=True, timeout=NETWORK_CMD_TIMEOUT)
        return result.returncode == 0
    
    @staticmethod
    def install_via_eget(repo: str, binary_name: str) -> bool:
        """Install package via eget from GitHub (eget verifies release checksums when present)."""
        if not SystemChecker.has_command("eget"):
            print("eget not found, installing eget first...")
            if not Installer.install_eget():
                return False
        
        print(f"Installing {binary_name} via eget from {repo}...")
        result = Installer.run_command(
            ["eget", repo],
            capture_output=True,
            timeout=NETWORK_CMD_TIMEOUT,
        )
        
        if result.returncode == 0 and os.path.exists(binary_name):
            return Installer.install_binary_to_path(binary_name, binary_name)
        print(f"eget did not produce expected binary '{binary_name}'")
        return False
    
    @staticmethod
    def install_eget() -> bool:
        """Install eget from GitHub release binary (no curl|sh)."""
        print("Installing eget from GitHub releases (verified download, no curl|sh)...")
        arch = Installer.linux_goarch()
        if not arch:
            print(f"Unsupported architecture for eget: {platform.machine()}")
            return False

        tag, assets = Installer.fetch_latest_release_assets(EGET_GITHUB_REPO)
        if not tag or not assets:
            return False

        version = tag.lstrip("v")
        asset_name = f"eget-{version}-linux_{arch}.tar.gz"
        asset = next((a for a in assets if a.get("name") == asset_name), None)
        if not asset or not asset.get("browser_download_url"):
            print(f"No eget release asset named {asset_name}")
            return False

        with tempfile.TemporaryDirectory(prefix="eget-install-") as tmpdir:
            archive_path = os.path.join(tmpdir, asset_name)
            if not Installer.download_file(asset["browser_download_url"], archive_path):
                print("Failed to download eget archive")
                return False

            # Optional per-asset checksum if upstream publishes one
            checksum_asset = next(
                (
                    a for a in assets
                    if a.get("name") in (f"{asset_name}.sha256", f"{asset_name}.sha256sum")
                ),
                None,
            )
            if checksum_asset and checksum_asset.get("browser_download_url"):
                checksum_path = os.path.join(tmpdir, checksum_asset["name"])
                if Installer.download_file(checksum_asset["browser_download_url"], checksum_path):
                    try:
                        with open(checksum_path, "r", encoding="utf-8") as handle:
                            expected = handle.read().split()[0]
                    except (OSError, IndexError):
                        print("Could not read eget checksum file")
                        return False
                    if not Installer.verify_checksum(archive_path, expected):
                        return False
                else:
                    print("Warning: could not download eget checksum; continuing with binary checks")

            try:
                with tarfile.open(archive_path, "r:gz") as tar:
                    # Find member named 'eget' (may be nested under a directory)
                    member = next(
                        (m for m in tar.getmembers() if Path(m.name).name == "eget" and m.isfile()),
                        None,
                    )
                    if member is None:
                        print("eget binary not found inside release archive")
                        return False
                    Installer._safe_tar_extract(tar, member, tmpdir)
                    extracted = os.path.join(tmpdir, member.name)
            except (tarfile.TarError, OSError) as exc:
                print(f"Failed to extract eget archive: {exc}")
                return False

            # Copy out of tempdir before it is deleted (install moves the file)
            staged = os.path.join(os.getcwd(), "eget")
            try:
                shutil.copy2(extracted, staged)
            except OSError as exc:
                print(f"Failed to stage eget binary: {exc}")
                return False

            return Installer.install_binary_to_path(staged, "eget")

    @staticmethod
    def _safe_tar_extract(tar: tarfile.TarFile, member: tarfile.TarInfo, dest_dir: str) -> None:
        """Extract one member; use data filter on Python 3.12+ to block path traversal."""
        try:
            tar.extract(member, path=dest_dir, filter="data")
        except TypeError:
            # Python < 3.12 has no filter= kwarg
            if os.path.isabs(member.name) or ".." in Path(member.name).parts:
                raise tarfile.TarError(f"Refusing unsafe tar member path: {member.name}")
            tar.extract(member, path=dest_dir)
    
    @staticmethod
    def install_croc() -> bool:
        """Install croc from GitHub releases with checksum verification (no curl|bash)."""
        print("Installing croc from GitHub releases with checksum verification...")
        arch = Installer.linux_goarch()
        if not arch:
            print(f"Unsupported architecture for croc: {platform.machine()}")
            return False

        # croc asset naming uses 64bit/ARM64 style labels
        arch_to_croc = {
            "amd64": "64bit",
            "386": "32bit",
            "arm64": "ARM64",
            "arm": "ARM",
        }
        croc_arch = arch_to_croc.get(arch)
        if not croc_arch:
            print(f"No croc asset mapping for arch {arch}")
            return False

        tag, assets = Installer.fetch_latest_release_assets("schollz/croc")
        if not tag or not assets:
            return False

        asset_name = f"croc_{tag}_Linux-{croc_arch}.tar.gz"
        checksum_name = f"croc_{tag}_checksums.txt"
        asset = next((a for a in assets if a.get("name") == asset_name), None)
        checksum_asset = next((a for a in assets if a.get("name") == checksum_name), None)
        if not asset or not asset.get("browser_download_url"):
            print(f"No croc release asset named {asset_name}")
            return False
        if not checksum_asset or not checksum_asset.get("browser_download_url"):
            print(f"No croc checksum file {checksum_name}; refusing unsigned install")
            return False

        with tempfile.TemporaryDirectory(prefix="croc-install-") as tmpdir:
            archive_path = os.path.join(tmpdir, asset_name)
            checksum_path = os.path.join(tmpdir, checksum_name)
            if not Installer.download_file(asset["browser_download_url"], archive_path):
                print("Failed to download croc archive")
                return False
            if not Installer.download_file(checksum_asset["browser_download_url"], checksum_path):
                print("Failed to download croc checksums")
                return False

            try:
                with open(checksum_path, "r", encoding="utf-8") as handle:
                    checksums = Installer.parse_checksums_file(handle.read())
            except OSError as exc:
                print(f"Failed to read croc checksums: {exc}")
                return False

            expected = checksums.get(asset_name)
            if not expected:
                print(f"Checksum entry missing for {asset_name}")
                return False
            if not Installer.verify_checksum(archive_path, expected):
                return False

            try:
                with tarfile.open(archive_path, "r:gz") as tar:
                    member = next(
                        (m for m in tar.getmembers() if Path(m.name).name == "croc" and m.isfile()),
                        None,
                    )
                    if member is None:
                        print("croc binary not found inside release archive")
                        return False
                    Installer._safe_tar_extract(tar, member, tmpdir)
                    extracted = os.path.join(tmpdir, member.name)
            except (tarfile.TarError, OSError) as exc:
                print(f"Failed to extract croc archive: {exc}")
                return False

            staged = os.path.join(os.getcwd(), "croc")
            try:
                shutil.copy2(extracted, staged)
            except OSError as exc:
                print(f"Failed to stage croc binary: {exc}")
                return False

            return Installer.install_binary_to_path(staged, "croc")
    
    @staticmethod
    def check_apt_available(package: str) -> bool:
        """Check if package is available in apt repositories."""
        # Regex anchors (^$) ensure exact match, not substring
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
                     "GUI editor like notepad++", "Desktop GUI Apps", requires_gui=True),
        "wireshark": Tool("wireshark", "wireshark", InstallMethod.APT, "wireshark",
                         "Network packet reviewer", "Desktop GUI Apps", requires_gui=True),
        "code": Tool("code", "code", InstallMethod.SNAP, "code",
                    "Visual Studio Code", "Desktop GUI Apps", classic=True, requires_gui=True),
        "guake": Tool("guake", "guake", InstallMethod.APT, "guake",
                     "GUI terminal client", "Desktop GUI Apps", requires_gui=True),
        "tabby": Tool("tabby", "tabby", InstallMethod.EGET, "tabby",
                     "Modern terminal emulator", "Desktop GUI Apps",
                     github_repo="Eugeny/tabby", requires_gui=True),
        
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
                   github_repo="lsd-rs/lsd"),
        
        # Text Editors and Viewers
        "micro": Tool("micro", "micro", InstallMethod.EGET, "micro",
                     "User-friendly terminal editor", "Text Editors and Viewers",
                     github_repo="micro-editor/micro"),
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
        "doggo": Tool("doggo", "doggo", InstallMethod.EGET, "doggo",
                   "Modern dig alternative (dog successor)", "Network-Related Apps",
                   github_repo="mr-karan/doggo"),
        # Published on npm, not as a GitHub release binary: the project is
        # TypeScript and has never attached an asset to any of its releases.
        "neoss": Tool("neoss", "neoss", InstallMethod.NPM, "neoss",
                     "Modern ss alternative", "Network-Related Apps"),
        
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
        # Distributed on PyPI; the GitHub project cuts no releases at all.
        "eg": Tool("eg", "eg", InstallMethod.PIP, "eg",
                  "TLDR-like command helper", "Misc CLI Terminal Apps"),
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
    def get_tools_by_category(server_mode: bool = False) -> Dict[str, List[Tool]]:
        """Group tools by category, optionally filtering out GUI tools for server mode."""
        categories: Dict[str, List[Tool]] = {}
        for tool in ToolManager.TOOLS.values():
            # Skip GUI tools in server mode
            if server_mode and tool.requires_gui:
                continue
            if tool.category not in categories:
                categories[tool.category] = []
            categories[tool.category].append(tool)
        return categories
    
    @staticmethod
    def check_tool_installed(tool: Tool) -> bool:
        """Check if tool is installed."""
        return SystemChecker.has_command(tool.command)
    
    @staticmethod
    def install_tool(tool: Tool, dry_run: bool = False) -> bool:
        """Install a tool using its defined method."""
        if tool.method == InstallMethod.BUILTIN:
            print(f"✓ {tool.name} is built-in (no installation needed)")
            return True
        
        if dry_run:
            # In dry-run mode, just show what would be done
            if tool.method == InstallMethod.APT:
                print(f"[DRY RUN] Would install {tool.package} via apt")
            elif tool.method == InstallMethod.PIP:
                print(f"[DRY RUN] Would install {tool.package} via pip3")
            elif tool.method == InstallMethod.SNAP:
                classic_str = " (classic)" if tool.classic else ""
                print(f"[DRY RUN] Would install {tool.package} via snap{classic_str}")
            elif tool.method == InstallMethod.NPM:
                print(f"[DRY RUN] Would install {tool.package} via npm")
            elif tool.method == InstallMethod.EGET:
                print(f"[DRY RUN] Would install {tool.command} via eget from {tool.github_repo}")
            elif tool.method == InstallMethod.MANUAL:
                print(f"[DRY RUN] Would install {tool.name} manually")
            return True  # Pretend success in dry-run mode

        ok = False
        if tool.method == InstallMethod.APT:
            if Installer.check_apt_available(tool.package):
                ok = Installer.install_via_apt(tool.package)
            else:
                print(f"⚠ {tool.name} not available in apt repositories")
                return False
        
        elif tool.method == InstallMethod.PIP:
            ok = Installer.install_via_pip(tool.package)
        
        elif tool.method == InstallMethod.SNAP:
            ok = Installer.install_via_snap(tool.package, classic=tool.classic)

        elif tool.method == InstallMethod.NPM:
            ok = Installer.install_via_npm(tool.package)
        
        elif tool.method == InstallMethod.EGET:
            if tool.github_repo:
                # install_via_eget already validates the binary post-install
                return Installer.install_via_eget(tool.github_repo, tool.command)
            print(f"⚠ {tool.name} missing GitHub repository information")
            return False
        
        elif tool.method == InstallMethod.MANUAL:
            if tool.name == "croc":
                # install_croc already validates the binary post-install
                return Installer.install_croc()
            print(f"⚠ {tool.name} requires manual installation")
            return False
        
        else:
            return False

        if not ok:
            return False
        # Package managers already verify packages; only soft-check PATH visibility.
        # Hard version probes belong to binary installs (eget/croc) via install_binary_to_path.
        if SystemChecker.has_command(tool.command):
            print(f"  ✓ {tool.command} is available in PATH")
        else:
            print(f"  ⚠ {tool.command} not yet visible in PATH (may need a new shell session)")
        return True


def get_user_consent(server_mode: bool = False, dry_run: bool = False) -> bool:
    """Get user consent once upfront - simple and clear for lazy users."""
    print("\n" + "="*70)
    print("🚀 Lazy Linux Tool Installer")
    print("="*70)
    
    mode_info = []
    if server_mode:
        mode_info.append("🔧 SERVER MODE (CLI tools only, no GUI)")
    if dry_run:
        mode_info.append("👀 DRY RUN (preview only, no changes)")
    
    if mode_info:
        print("\n" + " | ".join(mode_info))
    
    print("\nThis script will automatically install all Linux tools from README.md")
    print("Perfect for lazy users - just say 'yes' and it handles everything!")
    print("\nWhat it does:")
    print("  ✓ Checks which tools you already have")
    if dry_run:
        print("  👀 Shows what would be installed (DRY RUN - no changes)")
    else:
        print("  ✓ Installs missing tools automatically (apt, pip, eget, snap, npm)")
    print("  ✓ Skips tools that are already installed")
    print("  ✓ Organizes everything by category")
    if server_mode:
        print("  🔧 Excludes GUI tools (server-friendly)")
    if not dry_run:
        print("\nYou'll be prompted for your sudo password when needed.")
    print("="*70)
    
    # Limit retries to prevent infinite loops on invalid input
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
            # Handle Ctrl+C and EOF gracefully without crashing
            print("\n\nInterrupted by user. Exiting.")
            return False
    
    return False


def update_package_lists(dry_run: bool = False) -> bool:
    """Update apt package lists."""
    if dry_run:
        print("\n[DRY RUN] Would update package lists (apt-get update)")
        return True
    print("\nUpdating package lists...")
    result = Installer.run_command(
        ["sudo", "apt-get", "update"],
        capture_output=True,
        timeout=NETWORK_CMD_TIMEOUT,
    )
    return result.returncode == 0


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Lazy Linux Tool Installer - Automatically install Linux tools from README.md",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Install all tools (default)
  %(prog)s --server           # Install only CLI tools (no GUI)
  %(prog)s --dry-run          # Preview what would be installed
  %(prog)s --server --dry-run # Preview server installation
        """
    )
    parser.add_argument(
        "--server",
        action="store_true",
        help="Server/minimal mode: only install CLI tools (exclude GUI applications)"
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Dry run mode: show what would be installed without making changes"
    )
    return parser.parse_args()


def main():
    """Main execution function."""
    # Parse command-line arguments
    args = parse_arguments()
    server_mode = args.server
    dry_run = args.dry_run
    
    # System check
    is_compatible, error_msg = SystemChecker.check_system()
    if not is_compatible:
        print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)
    
    # Get user consent
    if not get_user_consent(server_mode=server_mode, dry_run=dry_run):
        print("\nInstallation cancelled by user.")
        sys.exit(0)
    
    # Update package lists
    update_package_lists(dry_run=dry_run)
    
    # Get tools by category for better organization
    tools_by_category = ToolManager.get_tools_by_category(server_mode=server_mode)
    
    # Track installation results
    installed_count = 0
    skipped_count = 0
    failed_count = 0
    
    print("\n" + "="*70)
    if dry_run:
        print("👀 DRY RUN: Previewing what would be installed...")
    else:
        print("🔍 Checking and installing tools...")
    print("="*70 + "\n")
    
    # Process tools by category
    for category, tools in tools_by_category.items():
        print(f"\n📦 [{category}]")
        print("-" * 70)
        
        # Sort alphabetically for consistent output
        for tool in sorted(tools, key=lambda t: t.name):
            if ToolManager.check_tool_installed(tool):
                print(f"✓ {tool.name:30} - Already installed")
                skipped_count += 1
            else:
                print(f"✗ {tool.name:30} - Not installed, {'would install' if dry_run else 'installing'}...")
                if ToolManager.install_tool(tool, dry_run=dry_run):
                    if dry_run:
                        print(f"  ✓ {tool.name} would be installed successfully")
                    else:
                        print(f"  ✓ {tool.name} installed successfully")
                    installed_count += 1
                else:
                    print(f"  ✗ {tool.name} installation failed")
                    failed_count += 1
    
    # Summary - clear and friendly for lazy users
    print("\n" + "="*70)
    if dry_run:
        print("👀 DRY RUN Complete!")
    else:
        print("✨ Installation Complete!")
    print("="*70)
    print(f"✓ Already installed: {skipped_count}")
    if dry_run:
        print(f"👀 Would install:      {installed_count}")
    else:
        print(f"✓ Newly installed:   {installed_count}")
    if failed_count > 0:
        print(f"⚠ Failed:            {failed_count}")
    else:
        print(f"✓ Failed:            {failed_count}")
    print("="*70)
    
    if dry_run:
        print("\n👀 This was a DRY RUN - no changes were made.")
        print("   Run without --dry-run to actually install the tools.")
    elif failed_count > 0:
        print("\n⚠ Some tools failed to install. Check the output above for details.")
        print("   Some tools may require manual installation or different methods.")
    else:
        print("\n🎉 All tools installed successfully! You're all set!")
    
    print("\n💡 Tip: You can run this script again anytime to check for updates.")
    if not dry_run:
        input("\nPress Enter to exit...")
    sys.exit(0)


if __name__ == "__main__":
    main()
