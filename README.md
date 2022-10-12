# Linux-Tools
List of Linux Tools I put on almost every Linux / Debian host

#### Table of Contents
  
  * [Desktop GUI Apps](#desktop-gui-apps)
  * [Terminal File Explorers](#terminal-file-explorers)
  * [LS like Directory Viewers](#ls-like-directory-viewers)
  * [Text Editors and Viewers](#text-editors-and-viewers)
  * [Process Explorers](#process-explorers)
  * [Network Related Apps](#network-related-apps)
  * [Misc CLI Terminal Apps](#misc-cli-terminal-apps)
  * [Software Installer App](#software-installer-app)

## What I (_typically_) Install:

### Desktop GUI Apps
- **geany** --> GUI editor/ like “notepad++” for Windows
- **wireshark** --> network packet reviewer
- **code** --> (```sudo snap install --classic code```) _Microsoft Visual Studio Code IDE_ for Linux
- **guake** --> GUI terminal client for linux, more options than the built in terminal

---
### Terminal File Explorers
- **xplr** --> Very graphical, best on large screens (sayanarijit/xplr on Github)
- 🌟 **nnn** --> Efficient and elegant (```!``` drops to the command prompt) -  _personal favorite_
- **lf** --> Cross platform (best for Windows, _imho_) (gokcehan/lf on Github)
---

### LS like Directory Viewers 
- **exa** --> ls-like file / directory lister, adds colors and more to the standard ls output ([Exa website link](https://the.exa.website/))
- 🌟 **lsd** --> Another ls clone, cross-platform (works on Linux, Mac Win) can also show directory sizes (Peltoche/lsd GitHub) - _personal favorite_

----

### Text Editors and Viewers
- **micro** --> For those new to Linux, or aren’t into _vi_ or _vim_ (/zyedidia/micro on Github)
- **ne** --> Terminal editor (like nano / code highlighting, "esc" or F1 for menus)
- 🌟 **vim** --> VI editor with tons of extras - _personal favorite_
- **vimrc** --> config script for vim (from Github amix/vimrc)
- **bat** --> "cat" clone with colors and other features (sharkdp/bat on Github)

---
### Process Explorers 
- **glances** --> Lots of system info in one "glance", cross-platform (available for Windows) --_installs python_
- 🌟 **htop** --> Supercharged _top_ clone — _personal favorite_

---
### Network Related Apps
- **croc** --> Seemlessly and securely send files between 2 systems (PC, MAC, Linux, Debian etc) (schollz/croc on Github)
- **network-manager**  --> installs **nmtui** Terminal Network Manager app (set IPs, etc)
- **hping3** --> check if something is on the network, way more powerful than "ping"
- **nmap** --> Network scanner
- **bmon** --> TUI network bandwidth monitor
- **mtr** --> Traceroute and ping in one, great for network troubleshooting
- **dog** --> ``` Dig ``` clone DNS explorer with a TUI (/ogham/dog on Github)

---
### Misc CLI Terminal Apps

- **chkservice** --> TUI Linux service review from the terminal
- **ncdu** --> Terminal disk and folder space viewer
- **lynis** --> Linux security auditing 
- **apt-show-versions** --> shows package versions / if needing upgrade ("$ apt-show-versions -u")
- **fd** --> Linux find clone with saner defualt options (PC, MAC, Linux, Debian, etc) (sharkdp/fd on Github)
- **fish** --> "friendly interactive shell" beats the pants off of bash, ([Fishshell.com](https://fishshell.com))
- **tig** --> TUI client for git
- **python3** --> Development language
- **ned** --> A clone of "sed" (search and or replace) with an easier syntax (nevdelap/ned on Github)
- **miller** --> Does about everything awk and sed do for json/csv/etc files (johnkerl/miller on Github) -- more complex than ned
- **most** --> Linux pager, better than "less" or "more"
- **lazydocker** --> TUI terminal software for Docker containers (jesseduffield/lazydocker on Github)
- **json-tui** --> Easy way to review json files, has a cool table view (ArthurSonzogni/json-tui Github)
- **jc** --> Shows common Linux command output in json format 
- **duf** --> Disk utility TUI (aka a ```df``` clone (muesli/duf on Github)
- **visidata** --> Reading CSV files or other large data sets ([visidata.org](https://www.visidata.org/))
- **eg** --> [TLDR.sh](https://tldr.sh/) like tool that helps with Linux commands (srsudar/eg on Github)
- **procs** --> A ```ps ``` process explorer clone with a GUI (dalance/procs on Github)
- **sd** --> A ```sed ``` search & replace clone with saner syntax (/chmln/sd on Github)
- **ripgrep-all** - A ```grep ``` clone but faster, and can search pdfs, csv, zip, .gz etc (/phiresky/ripgrep-all)

---
## Sometimes using 2 apps together can be helpful

* Using jc and json-tui together can produce some pretty results, the top of the picture shows the table view output of ```sudo jc -p lsof -i |json-tui``` 
(the bottom showing the standard ```lsof -i``` results)<br><br>
![image](https://user-images.githubusercontent.com/48565067/155399052-e619f001-f33b-4272-ab3e-3cd43019cc90.png)
----
## Software Installer App 
### "Linux-Sotware-Installer" (_Last Updated in October 2022_) available under this repo's ```releases``` section
- Requires Python 3.x to run the script, and ```sudo``` access privileges
- Most of the tools require a Debian-like system such as Ubuntu to install (```croc``` by @schollz here on Github is an exception)
- Checks if the above software exists, if not installs it
- If you want to migrate this to work on a different OS, just update the code replacing "apt-get" with the different package manager syntax
- Long term goal is to get some of these tools installed via other OS package managers like ```Homebrew``` for ```Mac```and or ```Scoop``` / ```Chocolatey``` for ```Windows```
### Output of "Linux-Software-Installer"
![image](https://user-images.githubusercontent.com/48565067/141710525-a3ccf69b-f2d1-48f3-9fc3-5350229be8a5.png)
