# Linux Tools: 2026 Edition

The tools I put on almost every Linux / Debian host, with notes on what each one
replaces and what Debian actually calls it after you install it.

Install them one at a time, or all at once with
[`Lazy-Linux-Tool-Installer.py`](#installation).

## Looking for a replacement for something?

Most people arrive here wanting a better version of a command they already use,
so this is sorted by the command you already know. One recommendation per row;
alternatives are in the notes. The [full list](#what-i-typically-install) below
is grouped by category instead, for browsing.

| You already use | Try instead | Notes |
|---|---|---|
| `apt` | [nala](https://gitlab.com/volian/nala) | friendlier frontend |
| `awk` on CSV/JSON | [miller](https://github.com/johnkerl/miller) | Debian: `mlr` |
| `cat` | [bat](https://github.com/sharkdp/bat) | syntax highlighting; Debian: `batcat` |
| `cd` | [zoxide](https://github.com/ajeetdsouza/zoxide) | learns your habits |
| `df` | [duf](https://github.com/muesli/duf) | graphs |
| `dig` | [doggo](https://github.com/mr-karan/doggo) | DoH/DoT/DoQ; successor to `dog` |
| `docker` CLI | [lazydocker](https://github.com/jesseduffield/lazydocker) | TUI |
| `du` | [dust](https://github.com/bootandy/dust) | bar charts |
| `find` | [fd](https://github.com/sharkdp/fd) | Debian: `fdfind` |
| `git` at the CLI | [lazygit](https://github.com/jesseduffield/lazygit) | [tig](https://github.com/jonas/tig) is lighter; [delta](https://github.com/dandavison/delta) is a diff pager |
| `grep` | [ripgrep](https://github.com/BurntSushi/ripgrep) | Debian: `rg`; [rga](https://github.com/phiresky/ripgrep-all) searches PDFs and office docs |
| `less` / `more` | [most](https://www.jedsoft.org/most/) | multiple windows |
| `ls` | [eza](https://github.com/eza-community/eza) | [lsd](https://github.com/lsd-rs/lsd) also shows directory sizes |
| `make` as a task runner | [just](https://github.com/casey/just) | |
| `man` | [tldr](https://tldr.sh) | practical examples; [eg](https://github.com/srsudar/eg) is similar |
| `nano` / `vi` | [micro](https://github.com/micro-editor/micro) | [ne](https://github.com/vigna/ne) and [neovim](https://neovim.io) are heavier |
| `ping` | [gping](https://github.com/orf/gping) | live latency graph |
| `ps` | [procs](https://github.com/dalance/procs) | |
| `sed` for find/replace | [sd](https://github.com/chmln/sd) | simpler syntax |
| `ss` | [neoss](https://github.com/PabloLec/neoss) | TUI |
| `top` | [htop](https://htop.dev) | [btop](https://github.com/aristocratos/btop) and [bottom](https://github.com/ClementTsang/bottom) (`btm`) look nicer |
| `traceroute` | [mtr](https://www.bitwizard.nl/mtr/) | Debian: `mtr-tiny` |

## Installed it, but the command isn't found?

<details>
<summary>Debian and Ubuntu rename ten of these — bat, fd, bottom, miller, ripgrep, ripgrep-all, neovim, mtr, hping, NetworkManager</summary>

They are renamed to avoid clashing with existing packages. This catches almost
everyone at least once.

| Tool | apt package | What you actually type |
|---|---|---|
| bat | `bat` | **`batcat`** |
| fd | `fd-find` | **`fdfind`** |
| bottom | `bottom` | **`btm`** |
| miller | `miller` | **`mlr`** |
| ripgrep | `ripgrep` | **`rg`** |
| ripgrep-all | `ripgrep-all` | **`rga`** |
| neovim | `neovim` | **`nvim`** |
| mtr | `mtr-tiny` | **`mtr`** |
| hping | `hping3` | **`hping3`** |
| NetworkManager TUI | `network-manager` | **`nmtui`** |

If you would rather keep the upstream names, alias them in your shell:

```bash
echo 'alias bat=batcat' >> ~/.bashrc
echo 'alias fd=fdfind'  >> ~/.bashrc
source ~/.bashrc
```

</details>

#### Table of Contents

- [Linux Tools: 2026 Edition](#linux-tools-2026-edition)
  - [Looking for a replacement for something?](#looking-for-a-replacement-for-something)
  - [Installed it, but the command isn't found?](#installed-it-but-the-command-isnt-found)
  - [What I (_typically_) Install](#what-i-typically-install)
  - [Updates](#updates)
  - [Installation](#installation)
    - [One tool at a time](#one-tool-at-a-time)
    - [Or all of them at once](#or-all-of-them-at-once)
  - [Testing](#testing)
    - [Running Tests](#running-tests)
    - [Test Results](#test-results)
    - [Test Coverage](#test-coverage)
    - [Platform Independence](#platform-independence)
  - [Sometimes using two apps together can be helpful](#sometimes-using-two-apps-together-can-be-helpful)
  - [Sources](#sources)
  - [License](#license)

## What I (_typically_) Install


> **How to read this list:** Most entries are also installed by
> [`Lazy-Linux-Tool-Installer.py`](Lazy-Linux-Tool-Installer.py). A few are
> **reference-only** (configs, Windows-only, or too heavy) and are marked
> *not in the Lazy installer*.

Each category is collapsed. The tool names stay visible on every row, so you can scan or `Ctrl+F` the whole set without opening anything — click a row only when you want the descriptions.

<details>
<summary><b>Desktop GUI Apps</b> · 5 tools — geany, wireshark, Visual Studio Code, guake, tabby</summary>

- [**geany**](https://www.geany.org) -> GUI editor like "notepad++" for Windows
- [**wireshark**](https://www.wireshark.org) -> network packet analyzer
- [**Visual Studio Code**](https://code.visualstudio.com) -> via snap: ```sudo snap install --classic code``` (Lazy installer uses the same)
- [**guake**](https://github.com/Guake/guake) -> dropdown GUI terminal for Linux
- [**tabby**](https://tabby.sh) -> Modern cross-platform terminal (desktop app; GitHub releases are AppImage/`.deb`/tarballs, not a tiny static CLI) ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))

</details>

<details>
<summary><b>Terminal File Explorers</b> · 3 tools — xplr, nnn, lf</summary>

- [**xplr**](https://github.com/sayanarijit/xplr) -> Very graphical TUI file explorer, best on large screens (sayanarijit/xplr on GitHub)
- [🌟 **nnn**](https://github.com/jarun/nnn) -> Efficient and elegant
- [**lf**](https://github.com/gokcehan/lf) -> Cross-platform TUI file explorer (gokcehan/lf on GitHub)

</details>

<details>
<summary><b>LS-like Directory Viewers</b> · 2 tools — eza, lsd</summary>

- [**eza**](https://github.com/eza-community/eza) -> Modern `ls` replacement with colors and Git integration (successor to exa) ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))
- [🌟 **lsd**](https://github.com/lsd-rs/lsd) -> Another `ls` clone, cross-platform (Linux/macOS/Windows); can show directory sizes (lsd-rs/lsd) - _personal favorite_

</details>

<details>
<summary><b>Text Editors and Viewers</b> · 7 tools — micro, ne, vim, neovim, vimrc, bat, sublime text</summary>

- [**micro**](https://github.com/micro-editor/micro) -> Friendly terminal editor if you are not into vi/vim (micro-editor/micro)
- [**ne**](https://github.com/vigna/ne) -> Terminal editor (nano-like menus; Esc or F1)
- [🌟 **vim**](https://github.com/vim/vim) -> Vi Improved - _personal favorite_
- [**neovim**](https://neovim.io) -> Modern Vim-compatible editor (apt package `neovim`; command `nvim`) ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))
- [**vimrc**](https://github.com/amix/vimrc) -> Shared vim config (amix/vimrc) -> [⭐ **vim_awesome** based on this](https://github.com/ArthurChiao/vim_awesome) — _configs only; not installed by the Lazy installer_
- [**bat**](https://github.com/sharkdp/bat) -> `cat` clone with syntax highlighting / git integration ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)) — on Debian/Ubuntu apt the command is often **`batcat`**
- [**sublime text**](https://www.sublimetext.com) -> GUI editor — _manual install; not in the Lazy installer_

</details>

<details>
<summary><b>Process Explorers</b> · 5 tools — glances, htop, btop, bottom, system informer</summary>

- [**glances**](https://nicolargo.github.io/glances/) -> Lots of system info in one glance; cross-platform — _Lazy installer uses `pip3 install --user glances` (requires Python/pip already present)_
- [🌟 **htop**](https://htop.dev) -> Supercharged `top` clone — _personal favorite_
- [**btop**](https://github.com/aristocratos/btop) -> Fast TUI process/resource monitor ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))
- [**bottom**](https://github.com/ClementTsang/bottom) -> Cross-platform process monitor inspired by btop — command is **`btm`**
- [**system informer**](https://www.systeminformer.com/) -> **Windows-only** successor to Process Hacker — _listed for cross-platform awareness; not in the Lazy installer_

</details>

<details>
<summary><b>Network-Related Apps</b> · 10 tools — croc, network-manager, hping3, nmap, bmon, mtr, gping, doggo, neoss, zabbix</summary>

- [**croc**](https://github.com/schollz/croc) -> Securely send files between machines (cross-platform; schollz/croc)
- [**network-manager**](https://networkmanager.dev/) -> apt package that provides **`nmtui`** (terminal NetworkManager UI)
- [**hping3**](https://github.com/antirez/hping) -> Advanced ping/packet crafting — install via apt as **`hping3`** (upstream repo is `antirez/hping`)
- [**nmap**](https://nmap.org) -> Network scanner → related: [**ncrack**](https://github.com/nmap/ncrack) — _ncrack is not auto-installed_
- [**bmon**](https://github.com/tgraf/bmon) -> TUI network bandwidth monitor
- [**mtr**](https://www.bitwizard.nl/mtr/) -> Traceroute + ping (apt package is often `mtr-tiny`; command `mtr`)
- [**gping**](https://github.com/orf/gping) -> Ping with a live latency graph
- [**doggo**](https://github.com/mr-karan/doggo) -> Modern `dig` alternative (DoH/DoT/DoQ); actively maintained successor to [ogham/dog](https://github.com/ogham/dog)
- [**neoss**](https://github.com/PabloLec/neoss) -> User-friendly `ss` alternative with a TUI
- [**zabbix**](https://www.zabbix.com) -> Full monitoring stack — _not in the Lazy installer (much heavier than a CLI utility)_

</details>

<details>
<summary><b>Misc CLI Terminal Apps</b> · 32 tools — systemctl, ncdu, dust, duf, lynis, apt-show-versions, nala, fd, fish, starship, zoxide, atuin, tig, lazygit, delta, miller, most, tldr, lazydocker, json-tui, jc, visidata, eg, procs, sd, ripgrep, ripgrep-all, fzf, fastfetch, pandoc, hyperfine, just</summary>

- [**systemctl**](https://manpages.debian.org/stable/systemd/systemctl.1.en.html) -> Built-in **systemd** service manager (`systemctl status`, `systemctl list-units`, …) — _not installed by the script (already on systemd hosts); former wrapper `chkservice` is effectively unmaintained_
- [**ncdu**](https://dev.yorhel.nl/ncdu) -> Terminal disk/folder space viewer
- [**dust**](https://github.com/bootandy/dust) -> Friendlier `du` with bar charts ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))
- [**duf**](https://github.com/muesli/duf) -> Friendlier `df` with graphs
- [**lynis**](https://cisofy.com/lynis/) -> Linux security auditing by CISOfy ([GitHub](https://github.com/CISOfy/lynis))
- [**apt-show-versions**](https://tracker.debian.org/pkg/apt-show-versions) -> Show package versions / upgrades (`apt-show-versions -u`)
- [**nala**](https://gitlab.com/volian/nala) -> Friendlier apt frontend ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))
- [**fd**](https://github.com/sharkdp/fd) -> Friendlier `find` (sharkdp/fd); Debian/Ubuntu apt package `fd-find`, command often **`fdfind`**
- [**fish**](https://fishshell.com) -> Friendly interactive shell
- [**starship**](https://starship.rs) -> Cross-shell customizable prompt ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))
- [**zoxide**](https://github.com/ajeetdsouza/zoxide) -> Smarter `cd` that learns your habits ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))
- [**atuin**](https://github.com/atuinsh/atuin) -> Shell history search/sync across machines
- [**tig**](https://github.com/jonas/tig) -> TUI git client
- [**lazygit**](https://github.com/jesseduffield/lazygit) -> Simple TUI for git
- [**delta**](https://github.com/dandavison/delta) -> Syntax-highlighting pager for git diffs
- [**miller**](https://github.com/johnkerl/miller) -> awk/sed-like tool for CSV/JSON/etc. — command is **`mlr`**
- [**most**](https://www.jedsoft.org/most/) -> Pager with more features than less/more
- [**tldr**](https://tldr.sh) -> Simplified practical man pages ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)) — Lazy installer uses `pip3 install --user tldr`
- [**lazydocker**](https://github.com/jesseduffield/lazydocker) -> TUI for Docker
- [**json-tui**](https://github.com/ArthurSonzogni/json-tui) -> Terminal JSON viewer with table view
- [**jc**](https://github.com/kellyjonbrazil/jc) -> Convert common command output to JSON
- [**visidata**](https://www.visidata.org/) -> Interactive viewer for CSV and other tabular data — Lazy installer uses `pip3 install --user visidata`
- [**eg**](https://github.com/srsudar/eg) -> Useful command examples at the CLI (similar niche to [tldr](https://tldr.sh/))
- [**procs**](https://github.com/dalance/procs) -> Modern `ps` replacement
- [**sd**](https://github.com/chmln/sd) -> Simpler `sed`-like find/replace
- [**ripgrep**](https://github.com/BurntSushi/ripgrep) -> Fast recursive search — command is **`rg`** ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))
- [**ripgrep-all**](https://github.com/phiresky/ripgrep-all) -> ripgrep across PDFs, office docs, and other rich formats — command is **`rga`**
- [**fzf**](https://github.com/junegunn/fzf) -> Fuzzy finder for files, history, and pipelines
- [**fastfetch**](https://github.com/fastfetch-cli/fastfetch) -> Fast system-info display (neofetch-style) ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))
- [**pandoc**](https://pandoc.org) -> Universal document converter ([source thread](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/))
- [**hyperfine**](https://github.com/sharkdp/hyperfine) -> Command-line benchmarking
- [**just**](https://github.com/casey/just) -> Command runner / lightweight `make` alternative

</details>

---
## Updates

<details>
<summary>Version history, newest first</summary>

* 07/14/26 - Tagged [**v5.0.1**](https://github.com/StewAlexander-com/Linux-Tools/releases/tag/v5.0.1): forensic README accuracy pass; `--server` only skips real GUI apps (`xplr` is TUI again)
* 07/14/26 - Forensic README accuracy pass: fix misleading install claims, jc example, Debian command aliases, glances/tabby/systemctl notes; exclude only real GUI apps from `--server`
* 07/14/26 - Tagged [**v5.0.0**](https://github.com/StewAlexander-com/Linux-Tools/releases/tag/v5.0.0): secure eget/croc installs; README 2026 freshness; `dog` → `doggo`
* 07/14/26 - Security: removed curl|sh/bash for eget/croc; GitHub release downloads with ELF checks, croc SHA-256 verification, post-install probes, longer timeouts
* 07/14/26 - README freshness: 2026 edition; fixed moved/dead links; clarified README-only tools; synced repos (`lsd-rs/lsd`, `micro-editor/micro`)
* 12/02/25 - Added server/minimal mode (`--server`) and dry-run (`--dry-run`/`-n`)
* 12/02/25 - Renamed to Lazy-Linux-Tool-Installer.py; dataclasses/type hints; platform-independent test suite
* 12/02/25 - Replaced unavailable chkservice; added lazygit, delta, atuin, gping, hyperfine, just
* 09/06/25 - README formatting/link improvements; ripgrep-all description
* 03/18/25 - 2025 alternatives update: eza, neovim, tldr, zoxide, starship, dust, nala, fastfetch
* 11/19/23 - Readme consistency/readability
* 01/29/23 - Major installer improvements; added eget
* 11/05/22 - Tool names became links

</details>

---

## Installation

### One tool at a time

Nothing here requires the installer. Most entries are a single apt package, and
the ones that are not link to their own install instructions:

```bash
sudo apt install bat fd-find ripgrep fzf htop ncdu tldr
```

For tools published only as GitHub releases, [eget](https://github.com/zyedidia/eget)
fetches a binary from any repo in `owner/name` form:

```bash
eget schollz/croc
```

### Or all of them at once

[`Lazy-Linux-Tool-Installer.py`](Lazy-Linux-Tool-Installer.py) installs the **tool definitions in that script** (currently ~60 entries): checks PATH, installs missing tools via apt/pip/snap/eget (and a verified GitHub install for croc), and skips anything already present.

It does **not** install README reference-only items (vimrc configs, Sublime Text, System Informer, Zabbix, ncrack).

**Requires:** Debian-family OS (`apt-get`), `sudo`, `curl`, and network access. You will be prompted once for consent, then for sudo as needed.

### Quick Install (tracks `main`)

```bash
curl -O https://raw.githubusercontent.com/StewAlexander-com/Linux-Tools/main/Lazy-Linux-Tool-Installer.py && chmod +x Lazy-Linux-Tool-Installer.py && python3 Lazy-Linux-Tool-Installer.py
```

### Pin to release v5.0.1

```bash
curl -O https://raw.githubusercontent.com/StewAlexander-com/Linux-Tools/v5.0.1/Lazy-Linux-Tool-Installer.py && chmod +x Lazy-Linux-Tool-Installer.py && python3 Lazy-Linux-Tool-Installer.py
```

### Download and Run

```bash
# Latest main
curl -O https://raw.githubusercontent.com/StewAlexander-com/Linux-Tools/main/Lazy-Linux-Tool-Installer.py
# Or pin: curl -O https://raw.githubusercontent.com/StewAlexander-com/Linux-Tools/v5.0.1/Lazy-Linux-Tool-Installer.py

chmod +x Lazy-Linux-Tool-Installer.py
python3 Lazy-Linux-Tool-Installer.py
```

### Options

- **Default**: Install CLI + desktop GUI tools defined in the script
- **`--server`**: Skip desktop GUI apps only (`geany`, `wireshark`, `code`/VS Code, `guake`, `tabby`). TUI tools such as `xplr`/`htop`/`nnn` still install
- **`--dry-run` / `-n`**: Preview actions; make no changes
- **`--help`**: Show all options

**Examples:**
```bash
python3 Lazy-Linux-Tool-Installer.py --server           # headless-friendly set
python3 Lazy-Linux-Tool-Installer.py --dry-run          # preview
python3 Lazy-Linux-Tool-Installer.py --server --dry-run # preview server set
```

> **Security note:** The installer does not use `curl | sh` or `curl | bash` for eget or croc. It downloads GitHub release artifacts, applies binary sanity checks, verifies croc’s published SHA-256 checksums, and runs simple post-install probes for those binaries.

---

## Testing

<details>
<summary>How to run the test suite, and what it covers (for contributors)</summary>

`test_lazy_linux_tool_installer.py` is a mocked unit-test suite for `Lazy-Linux-Tool-Installer.py` (no real package installs).

### Running Tests

From the `Linux-Tools` directory:

```bash
python3 -m unittest test_lazy_linux_tool_installer
python3 -m unittest test_lazy_linux_tool_installer -v
python3 -m unittest test_lazy_linux_tool_installer.TestSystemChecker -v
```

### Test Results

**Current Status:** ✅ All tests passing

```
Ran 46 tests in 0.008s
OK
```

### Test Coverage

- **SystemChecker** — Debian-like detection, command availability, root check, curl/sudo requirements
- **Installer** — command runner/timeouts, apt/pip/eget/snap paths, curl|sh regression guard
- **ToolManager** — tool definitions, categories, install routing
- **User consent** — retries and KeyboardInterrupt handling
- **Main** — system-check failure and consent decline paths (argv-safe under `unittest`)

### Platform Independence

Tests mock subprocess/filesystem side effects so they can run on Linux, macOS, or Windows without installing packages. They are **not** end-to-end install tests on a live Debian host.

</details>

---

## Sometimes using two apps together can be helpful

* `jc` + `json-tui` (pretty JSON table view):
```bash
sudo lsof -i | jc --lsof -p | json-tui
```

* Interactive file picking with ripgrep + fzf:
```bash
rg --files | fzf
```

* Faster navigation + richer prompts: `zoxide` with `starship` (each needs its own shell init hook; see their docs).

---
## Sources
1. [Linux CLI Tool Upgrades/Alternatives — r/selfhosted](https://www.reddit.com/r/selfhosted/comments/1fg3cou/linux_cli_tool_upgradesalternatives/)
2. [eget](https://github.com/zyedidia/eget)
3. [doggo](https://github.com/mr-karan/doggo)
4. [NetworkManager](https://networkmanager.dev/)
5. [micro editor](https://github.com/micro-editor/micro)
6. [jc docs — lsof parser](https://kellyjonbrazil.github.io/jc/docs/parsers/lsof.html)

---
## License

[MIT](LICENSE). Use it, fork it, ship it.
