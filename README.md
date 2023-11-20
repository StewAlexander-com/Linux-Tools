# Linux-Tools
List of Linux Tools I put on almost every Linux / Debian host

## Use Eget to download apps from Github
* [Click here to download eget](https://github.com/zyedidia/eget), then type ```$ eget schollz/croc``` to download croc (which copies files between systems)
* Change "schollz/croc" to any github repo discussed below …


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
- [**geany**](https://www.geany.org)-> GUI editor/ like “notepad++” for Windows
- [**wireshark**](https://www.wireshark.org)--> network packet reviewer
- [**visual Studio Code**](https://code.visualstudio.com) --> (```sudo snap install --classic code```) _Microsoft Visual Studio Code IDE_ for Linux
- [**guake**](http://guake-project.org)-> GUI terminal client for linux, more options than the built in terminal

---
### Terminal File Explorers
- [**xplr**](https://github.com/sayanarijit/xplr) --> Very graphical, best on large screens (sayanarijit/xplr on Github)
- [🌟 **nnn**](https://github.com/jarun/nnn)--> Efficient and elegant (```!``` drops to the command prompt) -  _personal favorite_
- [**lf**](https://github.com/gokcehan/lf)--> Cross platform (best for Windows, _imho_) (gokcehan/lf on Github)
---

### LS like Directory Viewers 
- [**exa**](https://the.exa.website)--> ls-like file / directory lister, adds colors and more to the standard ls output ([Exa website link](https://the.exa.website/))
- [🌟 **lsd**](https://github.com/Peltoche/lsd)-> Another ls clone, cross-platform (works on Linux, Mac Win) can also show directory sizes (Peltoche/lsd GitHub) - _personal favorite_

----

### Text Editors and Viewers
- [**micro**](https://github.com/zyedidia/micro)--> For those new to Linux, or aren’t into _vi_ or _vim_ (/zyedidia/micro on Github)
- [**ne**](https://ne.di.unimi.it)--> Terminal editor (like nano / code highlighting, "esc" or F1 for menus)
- [🌟 **vim**](https://github.com/vim/vim)--> VI editor with tons of extras - _personal favorite_
- [**vimrc**](https://github.com/amix/vimrc)--> config script for vim (from Github amix/vimrc) --> [⭐ _Try out **vim_awesome** based on this_](https://github.com/ArthurChiao/vim_awesome)
- [**bat**](https://github.com/sharkdp/bat)--> "cat" clone with colors and other features (sharkdp/bat on Github)

---
### Process Explorers 
- [**glances**](https://nicolargo.github.io/glances/) --> Lots of system info in one "glance", cross-platform (available for Windows) --_installs python_
- [🌟 **htop**](https://htop.dev) --> Supercharged _top_ clone — _personal favorite_
- [**btop**](https://github.com/aristocratos/btop)--> TUI CLI graphics, fast, less dependencies than _Glances_ (aristocratos/btop on Github)
- [**bottom**](https://github.com/ClementTsang/bottom) --> A _**btop**_ inspired process monitor, _cross platform_

---
### Network Related Apps
- [**croc**](https://github.com/schollz/croc)--> Seemlessly and securely send files between 2 systems (_cross platform_ runs on PC, MAC, Linux, Debian etc) (schollz/croc on Github)
- [**network-manager**](https://wiki.gnome.org/Projects/NetworkManager)--> installs **nmtui** Terminal Network Manager app (set IPs, etc)
- [**hping3**](http://www.hping.org)--> check if something is on the network, way more powerful than "ping"
- [**nmap**](https://nmap.org)-> Network scanner --> [_Check out **ncrack** for a network authentication tool_](https://github.com/nmap/ncrack)
- [**bmon**](https://github.com/tgraf/bmon)-> TUI network bandwidth monitor
- [**mtr**](https://www.bitwizard.nl/mtr/)--> Traceroute and ping in one, great for network troubleshooting
- [**dog**](https://github.com/ogham/dog)--> ``` Dig ``` clone DNS explorer with a TUI (/ogham/dog on Github)
- [**neoss**](https://github.com/PabloLec/neoss) -- ```ss``` clone, shows socket statisitcs in an easy to search TUI (PabloLec/neoss on Github)
---
### Misc CLI Terminal Apps

- [**chkservice**](https://github.com/linuxenko/chkservice)--> TUI Linux _**systemd**_ service review from the terminal (_linuxenko/chkservice_ on Github)
- [**ncdu**](https://dev.yorhel.nl/ncdu)--> Terminal disk and folder space viewer
- [**lynis**](https://cisofy.com/lynis/)--> Linux security auditing by _**CISOFY**_
- [**apt-show-versions**](https://packages.ubuntu.com/source/focal/apt-show-versions)--> shows package versions / if needing upgrade ("$ apt-show-versions -u")
- [**fd**](https://github.com/sharkdp/fd)--> Linux find clone with saner defualt options (PC, MAC, Linux, Debian, etc) (sharkdp/fd on Github)
- [**fish**](https://fishshell.com) --> "friendly interactive shell" beats the pants off of bash, ([Fishshell.com](https://fishshell.com))
- [**tig**](https://github.com/jonas/tig)--> TUI client for git (jonas/tig on Github)
- [**miller**](https://github.com/johnkerl/miller) --> Does about everything awk and sed does for json/csv/etc files (johnkerl/miller on Github) 
- [**most**](https://www.makeuseof.com/most-linux-pager/)--> Linux pager, better than "less" or "more"
- [**lazydocker**](https://github.com/jesseduffield/lazydocker) --> TUI terminal software for Docker containers (jesseduffield/lazydocker on Github)
- [**json-tui**](https://github.com/ArthurSonzogni/json-tui)--> Easy way to review json files, has a cool table view (ArthurSonzogni/json-tui Github)
- [**jc**](https://github.com/kellyjonbrazil/jc)--> Shows common Linux command output in json format (kellyjonbrazil/jc on Github)
- [**duf**](https://github.com/muesli/duf) --> Disk utility TUI (aka a ```df``` clone, muesli/duf on Github)
- [**visidata**](https://www.visidata.org/) --> Reading CSV files or other large data sets ([visidata.org](https://www.visidata.org/))
- [**eg**](https://github.com/srsudar/eg) --> [TLDR.sh](https://tldr.sh/) like tool that helps with Linux commands (srsudar/eg on Github)
- [**procs**](https://github.com/dalance/procs) --> A ```ps ``` process explorer clone with a GUI (dalance/procs on Github)
- [**sd**](https://github.com/chmln/sd) --> A ```sed ``` search & replace clone with saner syntax (/chmln/sd on Github)
- [**ripgrep-all**](https://github.com//phiresky/ripgrep-all) --> A ```grep ``` clone but faster, and can search pdfs, csv, zip, .gz etc, _cross platform_ (/phiresky/ripgrep-all on Github)
- [**fzf**](https://github.com/junegunn/fzf) --> A command-line fuzzy finder that enhances search and navigation in the terminal. Ideal for quickly finding files, command history, git, and more (junegunn/fzf on GitHub)
---
## Updates
* 11/19/23 - Updated Readme for consistency and readability
* 01/29/23 - Huge improvements to the linux installer, added ```eget``` as a software installer
* 11/05/22 - Now the apps at the left are links to where you can get these tools (_happy holidays 🥳_)!

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
