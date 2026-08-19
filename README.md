# Linux Tools: 2026 Edition

Sixty-four command-line tools for Debian and Ubuntu. Each entry says what the
tool does, the command that installs it, and what you type to run it — which is
not always the same word.

- **Start with —** [the seven essentials](#start-here) · [a better tool for a classic command](#looking-for-a-replacement-for-something) · [when the command isn't found](#installed-it-but-the-command-isnt-found)
- **Browse by job —** [Files, search, disk](#files-search-and-disk-8) · [Shell & prompt](#shell-and-prompt-4) · [`ls` replacements](#ls-replacements-2) · [Editors](#text-editors-and-viewers-7) · [Monitors](#process-and-system-monitors-5) · [Network](#network-10) · [Git](#git-3) · [Data & documents](#data-and-documents-5) · [System & packages](#system-and-packages-6) · [Docs & benchmarks](#docs-containers-and-benchmarks-6) · [File explorers](#terminal-file-explorers-3) · [Desktop GUI](#desktop-gui-apps-5)

## Or install all of them at once ...

[`Lazy-Linux-Tool-Installer.py`](Lazy-Linux-Tool-Installer.py) skips anything you
already have. Works on Debian, Ubuntu, and anything built on them such as Mint
or Pop!_OS. You need `sudo` and `curl`.

```bash
curl -O https://raw.githubusercontent.com/StewAlexander-com/Linux-Tools/main/Lazy-Linux-Tool-Installer.py
chmod +x Lazy-Linux-Tool-Installer.py

python3 Lazy-Linux-Tool-Installer.py --dry-run   # preview, changes nothing
python3 Lazy-Linux-Tool-Installer.py             # go
```

Flags, pinning to a release, and the security notes are
[further down](#installer-options-and-notes).

## Start here

If you install nothing else, install these seven:

- **[bat](https://github.com/sharkdp/bat)** — read a file with colour and line numbers (a nicer `cat`)
- **[fd](https://github.com/sharkdp/fd)** — find files by name, quickly (a nicer `find`)
- **[ripgrep](https://github.com/BurntSushi/ripgrep)** — search inside files, very fast (a nicer `grep`)
- **[fzf](https://github.com/junegunn/fzf)** — type a few letters to pick from any list
- **[htop](https://htop.dev)** — see what is using CPU and memory (a nicer `top`)
- **[ncdu](https://dev.yorhel.nl/ncdu)** — find what is filling up the disk
- **[tldr](https://tldr.sh)** — short worked examples instead of long manual pages

```bash
sudo apt install bat fd-find ripgrep fzf htop ncdu tealdeer

# Three of those are typed differently from the package you install:
#   batcat   not  bat
#   fdfind   not  fd
#   tldr     is what tealdeer installs
```

Four more worth having. These are not in apt, so you fetch them straight from
the project's own downloads using a helper called
[eget](https://github.com/zyedidia/eget). eget is not in apt either, so install
it once, verifying the download against its published checksum:

```bash
curl -o eget.sh https://zyedidia.github.io/eget.sh
echo "0e64b8a3c13f531da005096cc364ac77835bda54276fedef6c62f3dbdc1ee919  eget.sh" | sha256sum -c
bash eget.sh
sudo mv eget /usr/local/bin/
```

Then:

- **[eza](https://github.com/eza-community/eza)** — `ls` with colour and git status
- **[zoxide](https://github.com/ajeetdsouza/zoxide)** — `cd` that learns your habits
- **[dust](https://github.com/bootandy/dust)** — `du` as a bar chart
- **[micro](https://github.com/micro-editor/micro)** — a friendly `nano` replacement

```bash
for r in eza-community/eza ajeetdsouza/zoxide bootandy/dust micro-editor/micro; do sudo eget --to /usr/local/bin "$r"; done
```

## Looking for a replacement for something?

Sorted by the older command being replaced, so you can look up whichever one
you have run into. One recommendation per row, with alternatives in the notes.
The [full list](#the-full-list) below is grouped by category instead, for
browsing.

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
| `man` | [tldr](https://tldr.sh) | practical examples; apt: `tealdeer`; [eg](https://github.com/srsudar/eg) is similar |
| `nano` / `vi` | [micro](https://github.com/micro-editor/micro) | [ne](https://github.com/vigna/ne) and [neovim](https://neovim.io) are heavier |
| `ping` | [gping](https://github.com/orf/gping) | live latency graph |
| `ps` | [procs](https://github.com/dalance/procs) | |
| `sed` for find/replace | [sd](https://github.com/chmln/sd) | simpler syntax |
| `ss` | [neoss](https://github.com/PabloLec/neoss) | TUI |
| `top` | [htop](https://htop.dev) | [btop](https://github.com/aristocratos/btop) and [bottom](https://github.com/ClementTsang/bottom) (`btm`) look nicer |
| `traceroute` | [mtr](https://www.bitwizard.nl/mtr/) | Debian: `mtr-tiny` |

## Installed it, but the command isn't found?

The name you install is often not the name you type, for three different
reasons. Only the first two are Debian's doing:

```text
# Debian renames these, and only these
bat           you type   batcat
fd            you type   fdfind

# These ship under a short name upstream, on every distro
ripgrep       you type   rg
ripgrep-all   you type   rga
miller        you type   mlr
bottom        you type   btm
neovim        you type   nvim

# Here it is the apt package name that differs, not the command
tldr          sudo apt install tealdeer
mtr           sudo apt install mtr-tiny
hping3        sudo apt install hping3
nmtui         sudo apt install network-manager
```

To keep the upstream names for the two Debian renames:

```bash
echo 'alias bat=batcat' >> ~/.bashrc
echo 'alias fd=fdfind'  >> ~/.bashrc
source ~/.bashrc
```

---

## The full list

Sixty-four tools in twelve groups. Every group starts with the command that
installs it. A few are listed for reference only, and say so.

The `eget` lines fetch a binary straight from a project's GitHub releases and
drop it on your PATH. They need eget itself, which is
[installed under Start here](#start-here).

### Files, search, and disk (8)

```bash
sudo apt install ncdu fd-find fzf ripgrep
for r in bootandy/dust muesli/duf phiresky/ripgrep-all chmln/sd; do sudo eget --to /usr/local/bin "$r"; done
```

- [**ncdu**](https://dev.yorhel.nl/ncdu) — Terminal disk/folder space viewer
- [**dust**](https://github.com/bootandy/dust) — Friendlier `du` with bar charts
- [**duf**](https://github.com/muesli/duf) — Friendlier `df` with graphs
- [**fd**](https://github.com/sharkdp/fd) — Friendlier `find` (sharkdp/fd); Debian/Ubuntu apt package `fd-find`, command often **`fdfind`**
- [**fzf**](https://github.com/junegunn/fzf) — Fuzzy finder for files, history, and pipelines
- [**ripgrep**](https://github.com/BurntSushi/ripgrep) — Fast recursive search — command is **`rg`**
- [**ripgrep-all**](https://github.com/phiresky/ripgrep-all) — ripgrep across PDFs, office docs, and other rich formats — command is **`rga`**
- [**sd**](https://github.com/chmln/sd) — Simpler `sed`-like find/replace

### Shell and prompt (4)

```bash
sudo apt install fish
for r in starship/starship ajeetdsouza/zoxide atuinsh/atuin; do sudo eget --to /usr/local/bin "$r"; done
```

- [**fish**](https://fishshell.com) — Friendly interactive shell
- [**starship**](https://starship.rs) — Cross-shell customizable prompt
- [**zoxide**](https://github.com/ajeetdsouza/zoxide) — Smarter `cd` that learns your habits
- [**atuin**](https://github.com/atuinsh/atuin) — Shell history search/sync across machines

### `ls` replacements (2)

```bash
for r in eza-community/eza lsd-rs/lsd; do sudo eget --to /usr/local/bin "$r"; done
```

- [**eza**](https://github.com/eza-community/eza) — Modern `ls` replacement with colors and Git integration (successor to exa)
- [🌟 **lsd**](https://github.com/lsd-rs/lsd) — Another `ls` clone, cross-platform (Linux/macOS/Windows); can show directory sizes (lsd-rs/lsd) - _personal favorite_

### Text editors and viewers (7)

```bash
sudo apt install bat ne neovim vim
sudo eget --to /usr/local/bin micro-editor/micro
```

- [**micro**](https://github.com/micro-editor/micro) — Friendly terminal editor if you are not into vi/vim (micro-editor/micro)
- [**ne**](https://github.com/vigna/ne) — Terminal editor (nano-like menus; Esc or F1)
- [🌟 **vim**](https://github.com/vim/vim) — Vi Improved - _personal favorite_
- [**neovim**](https://neovim.io) — Modern Vim-compatible editor (apt package `neovim`; command `nvim`)
- [**vimrc**](https://github.com/amix/vimrc) — Shared vim config (amix/vimrc); see [⭐ **vim_awesome** based on this](https://github.com/ArthurChiao/vim_awesome) — _configs only; not installed by the Lazy installer_
- [**bat**](https://github.com/sharkdp/bat) — `cat` clone with syntax highlighting / git integration — on Debian/Ubuntu apt the command is often **`batcat`**
- [**sublime text**](https://www.sublimetext.com) — GUI editor — _manual install; not in the Lazy installer_

### Process and system monitors (5)

```bash
sudo apt install htop
for r in aristocratos/btop ClementTsang/bottom; do sudo eget --to /usr/local/bin "$r"; done
pip3 install --user glances
```

- [**glances**](https://nicolargo.github.io/glances/) — Lots of system info in one glance; cross-platform — _Lazy installer uses `pip3 install --user glances` (requires Python/pip already present)_
- [🌟 **htop**](https://htop.dev) — Supercharged `top` clone — _personal favorite_
- [**btop**](https://github.com/aristocratos/btop) — Fast TUI process/resource monitor
- [**bottom**](https://github.com/ClementTsang/bottom) — Cross-platform process monitor inspired by btop — command is **`btm`**
- [**system informer**](https://www.systeminformer.com/) — **Windows-only** successor to Process Hacker — _listed for cross-platform awareness; not in the Lazy installer_

### Network (10)

```bash
sudo apt install bmon hping3 mtr-tiny network-manager nmap
for r in orf/gping mr-karan/doggo; do sudo eget --to /usr/local/bin "$r"; done
sudo eget --to /usr/local/bin schollz/croc   # installer verifies its SHA-256
sudo apt install npm && sudo npm install -g neoss   # neoss ships on npm, not a binary
```

- [**croc**](https://github.com/schollz/croc) — Securely send files between machines (cross-platform; schollz/croc)
- [**network-manager**](https://networkmanager.dev/) — apt package that provides **`nmtui`** (terminal NetworkManager UI)
- [**hping3**](https://github.com/antirez/hping) — Advanced ping/packet crafting — install via apt as **`hping3`** (upstream repo is `antirez/hping`)
- [**nmap**](https://nmap.org) — Network scanner → related: [**ncrack**](https://github.com/nmap/ncrack) — _ncrack is not auto-installed_
- [**bmon**](https://github.com/tgraf/bmon) — TUI network bandwidth monitor
- [**mtr**](https://www.bitwizard.nl/mtr/) — Traceroute + ping (apt package is often `mtr-tiny`; command `mtr`)
- [**gping**](https://github.com/orf/gping) — Ping with a live latency graph
- [**doggo**](https://github.com/mr-karan/doggo) — Modern `dig` alternative (DoH/DoT/DoQ); actively maintained successor to [ogham/dog](https://github.com/ogham/dog)
- [**neoss**](https://github.com/PabloLec/neoss) — User-friendly `ss` alternative with a TUI — installed with `npm install -g neoss`
- [**zabbix**](https://www.zabbix.com) — Full monitoring stack — _not in the Lazy installer (much heavier than a CLI utility)_

### Git (3)

```bash
sudo apt install tig
for r in jesseduffield/lazygit dandavison/delta; do sudo eget --to /usr/local/bin "$r"; done
```

- [**tig**](https://github.com/jonas/tig) — TUI git client
- [**lazygit**](https://github.com/jesseduffield/lazygit) — Simple TUI for git
- [**delta**](https://github.com/dandavison/delta) — Syntax-highlighting pager for git diffs

### Data and documents (5)

```bash
sudo apt install miller jc pandoc
sudo eget --to /usr/local/bin ArthurSonzogni/json-tui
pip3 install --user visidata
```

- [**miller**](https://github.com/johnkerl/miller) — awk/sed-like tool for CSV/JSON/etc. — command is **`mlr`**
- [**jc**](https://github.com/kellyjonbrazil/jc) — Convert common command output to JSON
- [**json-tui**](https://github.com/ArthurSonzogni/json-tui) — Terminal JSON viewer with table view
- [**visidata**](https://www.visidata.org/) — Interactive viewer for CSV and other tabular data — Lazy installer uses `pip3 install --user visidata`
- [**pandoc**](https://pandoc.org) — Universal document converter

### System and packages (6)

```bash
sudo apt install lynis apt-show-versions nala
for r in fastfetch-cli/fastfetch dalance/procs; do sudo eget --to /usr/local/bin "$r"; done
```

- [**systemctl**](https://manpages.debian.org/stable/systemd/systemctl.1.en.html) — Built-in **systemd** service manager (`systemctl status`, `systemctl list-units`, …) — _not installed by the script (already on systemd hosts); former wrapper `chkservice` is effectively unmaintained_
- [**lynis**](https://cisofy.com/lynis/) — Linux security auditing by CISOfy ([GitHub](https://github.com/CISOfy/lynis))
- [**apt-show-versions**](https://tracker.debian.org/pkg/apt-show-versions) — Show package versions / upgrades (`apt-show-versions -u`)
- [**nala**](https://gitlab.com/volian/nala) — Friendlier apt frontend
- [**fastfetch**](https://github.com/fastfetch-cli/fastfetch) — Fast system-info display (neofetch-style)
- [**procs**](https://github.com/dalance/procs) — Modern `ps` replacement

### Docs, containers, and benchmarks (6)

```bash
sudo apt install most
for r in jesseduffield/lazydocker sharkdp/hyperfine casey/just; do sudo eget --to /usr/local/bin "$r"; done
pip3 install --user eg
sudo apt install tealdeer                    # provides the tldr command
```

- [**tldr**](https://tldr.sh) — Simplified practical man pages — Lazy installer uses `pip3 install --user tldr`
- [**eg**](https://github.com/srsudar/eg) — Useful command examples at the CLI (similar niche to [tldr](https://tldr.sh/)) — installed with `pip3 install --user eg`
- [**most**](https://www.jedsoft.org/most/) — Pager with more features than less/more
- [**lazydocker**](https://github.com/jesseduffield/lazydocker) — TUI for Docker
- [**hyperfine**](https://github.com/sharkdp/hyperfine) — Command-line benchmarking
- [**just**](https://github.com/casey/just) — Command runner / lightweight `make` alternative

### Terminal file explorers (3)

```bash
sudo apt install nnn
for r in sayanarijit/xplr gokcehan/lf; do sudo eget --to /usr/local/bin "$r"; done
```

- [**xplr**](https://github.com/sayanarijit/xplr) — Very graphical TUI file explorer, best on large screens (sayanarijit/xplr on GitHub)
- [🌟 **nnn**](https://github.com/jarun/nnn) — Efficient and elegant
- [**lf**](https://github.com/gokcehan/lf) — Cross-platform TUI file explorer (gokcehan/lf on GitHub)

### Desktop GUI apps (5)

```bash
sudo apt install geany guake wireshark
sudo eget --to /usr/local/bin Eugeny/tabby
sudo snap install --classic code
```

- [**Visual Studio Code**](https://code.visualstudio.com) — via snap: ```sudo snap install --classic code``` (Lazy installer uses the same)
- [**geany**](https://www.geany.org) — GUI editor like "notepad++" for Windows
- [**wireshark**](https://www.wireshark.org) — network packet analyzer
- [**guake**](https://github.com/Guake/guake) — dropdown GUI terminal for Linux
- [**tabby**](https://tabby.sh) — Modern cross-platform terminal (desktop app; GitHub releases are AppImage/`.deb`/tarballs, not a tiny static CLI)
---
## Updates

<details>
<summary>Version history, newest first</summary>

* 08/19/26 - Tagged [**v5.1.0**](https://github.com/StewAlexander-com/Linux-Tools/releases/tag/v5.1.0): `neoss` and `eg` install again, new npm method, MIT license, README rebuilt for first-time visitors
* 08/19/26 - Fixed `neoss` (now npm) and `eg` (now pip): both were declared as eget tools, but eget could never fetch either one
* 08/19/26 - Added an opt-in test that asks GitHub whether every eget tool still ships a Linux binary, so this cannot go unnoticed again
* 08/19/26 - Working `eget` and `tldr` instructions: `eget` had no install steps and put binaries outside `PATH`; `tldr` is not in Debian stable, so `tealdeer` provides it
* 08/19/26 - README rebuilt around a first-time visitor: a "Start here" set, an install command per group, and the command names Debian actually gives you
* 08/19/26 - Added an MIT LICENSE
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

## Installer options and notes

`Lazy-Linux-Tool-Installer.py` routes each tool to apt, pip, snap, eget, or npm,
whichever suits it.

```bash
python3 Lazy-Linux-Tool-Installer.py --dry-run   # preview, changes nothing
python3 Lazy-Linux-Tool-Installer.py --server    # skip the five desktop GUI apps
python3 Lazy-Linux-Tool-Installer.py --help
```

Pin to a release rather than tracking `main`:

```bash
curl -O https://raw.githubusercontent.com/StewAlexander-com/Linux-Tools/v5.1.0/Lazy-Linux-Tool-Installer.py
```

It also needs network access, and prompts once for consent. It skips the five
entries this page lists for reference only: vimrc, Sublime Text, System
Informer, Zabbix, and ncrack. It does not pipe `curl` into a shell — release artifacts are
downloaded, sanity-checked, and croc's published SHA-256 is verified.

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

### Checking the eget tools against upstream

The mocked tests prove the installer calls `eget` correctly. They cannot prove
`eget` will find anything at the other end — a project can stop publishing
release binaries at any time, and that failure only shows up on a real machine.
One extra test asks GitHub whether every `eget` tool still ships a Linux binary.
It needs the network, so it is off unless you ask for it:

```bash
export GITHUB_TOKEN=$(gh auth token)   # optional, but avoids the 60/hour limit
LINUX_TOOLS_NETWORK_TESTS=1 python3 -m unittest test_lazy_linux_tool_installer
```

If the API budget is too low to check every tool, the test skips rather than
passing on a partial sweep.

### Test Results

**Current Status:** ✅ All tests passing

```
Ran 53 tests in 0.011s
OK (skipped=1)
```

The skip is the network test above, which stays out of the offline run.

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
