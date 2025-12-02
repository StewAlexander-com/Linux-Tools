# Linux Tools: 2025 Edition

List of Linux Tools I put on almost every Linux / Debian host

## Use Eget to download apps from Github
* [Click here to download eget](https://github.com/zyedidia/eget), then type ```$ eget schollz/croc```
* Change "schollz/croc" to any github repo discussed below …


#### Table of Contents
  
- [Linux Tools: 2025 Edition](#linux-tools-2025-edition)
  - [Use Eget to download apps from Github](#use-eget-to-download-apps-from-github)
      - [Table of Contents](#table-of-contents)
  - [What I (_typically_) Install](#what-i-typically-install)
    - [Desktop GUI Apps](#desktop-gui-apps)
    - [Terminal File Explorers](#terminal-file-explorers)
    - [LS-like Directory Viewers](#ls-like-directory-viewers)
    - [Text Editors and Viewers](#text-editors-and-viewers)
    - [Process Explorers](#process-explorers)
    - [Network-Related Apps](#network-related-apps)
    - [Misc CLI Terminal Apps](#misc-cli-terminal-apps)
  - [Updates](#updates)
  - [Installation](#installation)
  - [Testing](#testing)
    - [Running Tests](#running-tests)
    - [Test Results](#test-results)
    - [Test Coverage](#test-coverage)
    - [Platform Independence](#platform-independence)
  - [Sometimes using two apps together can be helpful](#sometimes-using-two-apps-together-can-be-helpful)
  - [Sources](#sources)

## What I (_typically_) Install

### Desktop GUI Apps
- [**geany**](https://www.geany.org) -> GUI editor/ like "notepad++" for Windows
- [**wireshark**](https://www.wireshark.org) -> network packet reviewer
- [**Visual Studio Code**](https://code.visualstudio.com) -> (```sudo snap install --classic code```)
- [**guake**](https://github.com/Guake/guake) -> GUI terminal client for linux, more options than the built in terminal
- [**tabby**](https://tabby.sh) -> Modern, feature-rich terminal emulator with excellent cross-platform support [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)

---
### Terminal File Explorers
- [**xplr**](https://github.com/sayanarijit/xplr) -> Very graphical, best on large screens (sayanarijit/xplr on Github)
- [🌟 **nnn**](https://github.com/jarun/nnn) -> Efficient and elegant
- [**lf**](https://github.com/gokcehan/lf) -> Cross platform (best for Windows, _imho_) (gokcehan/lf on Github)
---

### LS-like Directory Viewers 
- [**eza**](https://github.com/eza-community/eza) -> Modern replacement for ls with more features, colors and Git integration (successor to exa) [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [🌟 **lsd**](https://github.com/lsd-rs/lsd) -> Another ls clone, cross-platform (works on Linux, Mac Win) can also show directory sizes (Peltoche/lsd GitHub) - _personal favorite_

----

### Text Editors and Viewers
- [**micro**](https://github.com/zyedidia/micro) -> For those new to Linux, or aren't into _vi_ or _vim_ (/zyedidia/micro on Github)
- [**ne**](https://ne.di.unimi.it) -> Terminal editor (like nano / code highlighting, "esc" or F1 for menus)
- [🌟 **vim**](https://github.com/vim/vim) -> VI editor with tons of extras - _personal favorite_
- [**neovim**](https://neovim.io) -> Text editor that can be configured to mirror VS Code, with a lot of plugins and extensibility [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**vimrc**](https://github.com/amix/vimrc) -> config script for vim (from Github amix/vimrc) -> [⭐ _Try out **vim_awesome** based on this_](https://github.com/ArthurChiao/vim_awesome)
- [**bat**](https://github.com/sharkdp/bat) -> "cat" clone with syntax highlighting, git integration and other features [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**sublime text**](https://www.sublimetext.com) -> Sophisticated text editor for code, markup and prose with slick UI and amazing performance

---
### Process Explorers 
- [**glances**](https://nicolargo.github.io/glances/) -> Lots of system info in one "glance", cross-platform (available for Windows) --_installs python_
- [🌟 **htop**](https://htop.dev) -> Supercharged _top_ clone — _personal favorite_
- [**btop**](https://github.com/aristocratos/btop) -> TUI CLI graphics, fast, less dependencies than _Glances_ [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**bottom**](https://github.com/ClementTsang/bottom) -> A _**btop**_ inspired process monitor, _cross platform_
- [**system informer**](https://www.systeminformer.com/) -> Official successor to Process Hacker - a powerful, multi-purpose tool to monitor system resources and detect malware

---
### Network-Related Apps
- [**croc**](https://github.com/schollz/croc) -> Seamlessly and securely send files between 2 systems (_cross platform_ runs on PC, MAC, Linux, Debian etc) (schollz/croc on Github)
- [**network-manager**](https://wiki.gnome.org/Projects/NetworkManager) -> installs **nmtui** Terminal Network Manager app (set IPs, etc)
- [**hping3**](https://github.com/antirez/hping) -> check if something is on the network, way more powerful than "ping"
- [**nmap**](https://nmap.org) -> Network scanner -> [_Check out **ncrack** for a network authentication tool_](https://github.com/nmap/ncrack)
- [**bmon**](https://github.com/tgraf/bmon) -> TUI network bandwidth monitor
- [**mtr**](https://www.bitwizard.nl/mtr/) -> Traceroute and ping in one, great for network troubleshooting
- [**gping**](https://github.com/orf/gping) -> Ping with a graph - visual ping tool that shows latency over time
- [**dog**](https://github.com/ogham/dog) -> ``` Dig ```
- [**neoss**](https://github.com/PabloLec/neoss) -- ```ss```
- [**zabbix**](https://www.zabbix.com) -> Free monitoring system for networks, servers, and applications that can monitor on-premises resources and cloud services
---
### Misc CLI Terminal Apps

- [**systemctl**](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) -> Built-in Linux _**systemd**_ service manager (use `systemctl status`, `systemctl list-units`, etc. for service management) - _Note: chkservice (TUI wrapper) is no longer available_
- [**ncdu**](https://dev.yorhel.nl/ncdu) -> Terminal disk and folder space viewer
- [**dust**](https://github.com/bootandy/dust) -> More intuitive version of du with bar chart visualization [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**duf**](https://github.com/muesli/duf) -> Disk utility TUI with pretty graphs (a better ```df```)
- [**lynis**](https://cisofy.com/lynis/) -> Linux security auditing by _**CISOFY**_
- [**apt-show-versions**](https://packages.debian.org/apt-show-versions) -> shows package versions / if needing upgrade ("$ apt-show-versions -u")
- [**nala**](https://gitlab.com/volian/nala) -> Frontend for apt with a more user-friendly interface and colored output [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**fd**](https://github.com/sharkdp/fd) -> Linux find clone with saner default options (PC, MAC, Linux, Debian, etc) (sharkdp/fd on Github)
- [**fish**](https://fishshell.com) -> "friendly interactive shell" beats the pants off of bash, ([Fishshell.com](https://fishshell.com))
- [**starship**](https://starship.rs) -> Customizable cross-shell prompt with extensive customization options [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**zoxide**](https://github.com/ajeetdsouza/zoxide) -> Smarter cd command that learns your habits and helps you navigate faster [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**atuin**](https://github.com/atuinsh/atuin) -> Magical shell history - search, sync, and backup your command history across machines
- [**tig**](https://github.com/jonas/tig) -> TUI client for git (jonas/tig on Github)
- [**lazygit**](https://github.com/jesseduffield/lazygit) -> Simple terminal UI for git commands, great for interactive git workflows (jesseduffield/lazygit on Github)
- [**delta**](https://github.com/dandavison/delta) -> Syntax-highlighting pager for git, diff, grep, and blame output - makes git diffs beautiful
- [**miller**](https://github.com/johnkerl/miller) -> Does about everything awk and sed does for json/csv/etc files (johnkerl/miller on Github) 
- [**most**](https://www.jedsoft.org/most/) -> Linux pager, better than "less" or "more"
- [**tldr**](https://tldr.sh) -> Simplified man pages that just tell you what you need to know with practical examples [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**lazydocker**](https://github.com/jesseduffield/lazydocker) -> TUI terminal software for Docker containers (jesseduffield/lazydocker on Github)
- [**json-tui**](https://github.com/ArthurSonzogni/json-tui) -> Easy way to review json files, has a cool table view (ArthurSonzogni/json-tui Github)
- [**jc**](https://github.com/kellyjonbrazil/jc) -> Shows common Linux command output in json format (kellyjonbrazil/jc on Github)
- [**visidata**](https://www.visidata.org/) -> Reading CSV files or other large data sets ([visidata.org](https://www.visidata.org/))
- [**eg**](https://github.com/srsudar/eg) -> [TLDR.sh](https://tldr.sh/) like tool that helps with Linux commands (srsudar/eg on Github)
- [**procs**](https://github.com/dalance/procs) -> ps replacement
- [**sd**](https://github.com/chmln/sd) -> sed replacement
- [**ripgrep**](https://github.com/BurntSushi/ripgrep) -> Extremely fast text search tool that respects gitignore rules [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**ripgrep-all**](https://github.com/phiresky/ripgrep-all) -> A grep tool with improvements on speed and document formats
- [**fzf**](https://github.com/junegunn/fzf) -> A command-line fuzzy finder that enhances search and navigation in the terminal. Ideal for quickly finding files, command history, git, and more (junegunn/fzf on GitHub)
- [**fastfetch**](https://github.com/fastfetch-cli/fastfetch) -> Faster, more feature-rich neofetch alternative for system information display [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**pandoc**](https://pandoc.org) -> Universal document converter that can convert between various markup formats [8](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
- [**hyperfine**](https://github.com/sharkdp/hyperfine) -> Command-line benchmarking tool - measure and compare command execution times
- [**just**](https://github.com/casey/just) -> Command runner - a better alternative to make, with simpler syntax and no dependencies
---
## Updates
* 12/02/25 - Added server/minimal mode (--server) and dry-run flag (--dry-run/-n) to installer; server mode excludes GUI tools for headless servers; dry-run mode previews installations without making changes
* 12/02/25 - Renamed to Lazy-Linux-Tool-Installer.py for clarity; improved user experience with clearer output and friendly messages; refactored with Python 3 best practices (type hints, dataclasses, structured classes); added comprehensive test suite with platform-independent tests; fixed hanging issues and improved error handling
* 12/02/25 - Verified all links and replaced unavailable chkservice; added quality tools: lazygit, delta, atuin, gping, hyperfine, just
* 09/06/25 - README formatting and links improvements; improved ripgrep-all description
* 03/18/25 - Major 2025 update with latest alternatives: eza (exa successor), neovim, tldr, zoxide, starship, dust, nala, fastfetch
* 11/19/23 - Updated Readme for consistency and readability
* 01/29/23 - Huge improvements to the linux installer, added ```eget```
* 11/05/22 - Now the apps at the left are links to where you can get these tools (_happy holidays 🥳_)!

---
## Installation

If you just want to install these tools all at once, I created a **Lazy-Linux-Tool-Installer** to do it automatically. It checks which tools you already have, installs the missing ones, and organizes everything by category - perfect for lazy users who want everything set up with minimal effort!

### Quick Install (One-Liner) 🚀

```bash
curl -O https://raw.githubusercontent.com/StewAlexander-com/Linux-Tools/main/Lazy-Linux-Tool-Installer.py && chmod +x Lazy-Linux-Tool-Installer.py && python3 Lazy-Linux-Tool-Installer.py
```

### Download and Run

```bash
# Download
curl -O https://raw.githubusercontent.com/StewAlexander-com/Linux-Tools/main/Lazy-Linux-Tool-Installer.py
# Or: wget https://raw.githubusercontent.com/StewAlexander-com/Linux-Tools/main/Lazy-Linux-Tool-Installer.py

# Make executable and run
chmod +x Lazy-Linux-Tool-Installer.py
python3 Lazy-Linux-Tool-Installer.py
```

### Options

- **Default**: Installs all tools (GUI + CLI)
- **`--server`**: Server mode - only CLI tools (no GUI apps)
- **`--dry-run` or `-n`**: Preview what would be installed (no changes)
- **`--help`**: Show all options

**Examples:**
```bash
python3 Lazy-Linux-Tool-Installer.py --server          # Server install
python3 Lazy-Linux-Tool-Installer.py --dry-run         # Preview
python3 Lazy-Linux-Tool-Installer.py --server --dry-run # Preview server install
```

The script will check your system, show what it will install, ask for confirmation, then install everything automatically. Perfect for lazy users! 🚀

---

## Testing

The `Lazy-Linux-Tool-Installer.py` script includes a comprehensive test suite (`test_lazy_linux_tool_installer.py`) that ensures code quality and reliability.

### Running Tests

To run all tests:
```bash
python3 -m unittest test_lazy_linux_tool_installer
```

To run with verbose output:
```bash
python3 -m unittest test_lazy_linux_tool_installer -v
```

To run a specific test class:
```bash
python3 -m unittest test_lazy_linux_tool_installer.TestSystemChecker -v
```

### Test Results

**Current Status:** ✅ All tests passing

```
Ran 41 tests in 0.011s
OK
```

### Test Coverage

The test suite includes:

- **SystemChecker Tests** - Validates system compatibility checks (Debian-like detection, command availability, root user detection)
- **Installer Tests** - Tests command execution, timeout handling, file not found errors, and installation methods (apt, pip, eget, snap)
- **ToolManager Tests** - Verifies tool definitions, category organization, installation status checks, and tool installation logic
- **User Consent Tests** - Ensures proper handling of user input with retry limits and keyboard interrupt handling
- **Main Function Tests** - Validates the main execution flow, system check failures, and user consent scenarios

### Platform Independence

All tests are **platform-independent** and use extensive mocking to avoid:
- Actual system modifications
- Real package installations
- OS-specific command dependencies
- Network operations

Tests can be run on any platform (Linux, macOS, Windows) without requiring actual tool installations or system changes.

---
## Sometimes using two apps together can be helpful

* Using jc and json-tui together can produce some pretty results, the top of the picture shows the table view output of
```sudo jc -p lsof -i |json-tui```
(the bottom showing the standard ```lsof -i```)
image

* Another powerful combination is using ripgrep with fzf for interactive file searching:
```rg --files | fzf```

* For terminal productivity, combining zoxide with starship creates an efficient navigation experience with informative prompts.

---
## Sources
1. [Top Embedded Linux Alternatives in 2025 — Slashdot](https://slashdot.org/software/p/Embedded-Linux/alternatives)
2. [Top Linux Mint Alternatives in 2025 — Slashdot](https://slashdot.org/software/p/Linux-Mint/alternatives)
6. [Debian running on Android (March 2025 update) — r/linux](https://www.reddit.com/r/linux/comments/1j6iqek/debian_running_on_android_march_2025_update/)
7. [Security update for libxml2 SUSE-SU-2025:0348-1 — SUSE](https://www.suse.com/support/update/announcement/2025/suse-su-20250348-1/)
8. [Linux CLI Tool Upgrades/Alternatives — r/selfhosted](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
