# Linux-Tools
List of Linux Tools I put on almost every Linux / Debian host
## What I (_typically_) Install:
- **geany** --> GUI editor/ notepad++ like
- **chkservice** --> TUI Linux service review from the terminal
- **htop** --> TUI supercharged top - shows processes and cpu info
- **nnn** --> Terminal file explorer (! drops to the command prompt)
- **ncdu** --> Terminal disk and folder space viewer
- **network-manager**  --> installs **nmtui** Terminal Network Manager app (set IPs, etc)
- **ne** --> Terminal editor (like nano / code highlighting, "esc" or F1 for menus)
- **hping3** --> check if something is on the network, way more powerful than "ping"
- **nmap** --> Network scanner
- **wireshark** --> network packet reviewer
- **lynis** --> Linux security auditing 
- **apt-show-versions** --> shows package versions / if needing upgrade ("$ apt-show-versions -u")
- **vim** --> VI editor with tons of extras
- **vimrc** --> config script for vim (from Github amix/vimrc)
- **bat** --> "cat" clone with colors and other features (sharkdp/bat on Github)
- **fd** --> Linux find clone with saner defualt options (PC, MAC, Linux, Debian, etc) (sharkdp/fd on Github)
- **fish** --> "friendly interactive shell" beats the pants off of bash, ([Fishshell.com](https://fishshell.com))
- **tig** --> TUI client for git
- **bmon** --> TUI network bandwidth monitor
- **dnsutils** --> installs "dig" for DNS troubleshooting
- **glances** --> like "htop" or "top" but more graphical, lots of sys info in one "glance" --installs python
- **python3** --> Development language
- **code** --> (sudo snap install --classic code) Visual Studio Code IDE for Linux
- **mtr** --> Traceroute and ping in one, great for network troubleshooting
- **ned** --> A clone of "sed" (search and or replace) with an easier syntax (nevdelap/ned on Github)
- **miller** --> Does about everything awk and sed do for json/csv/etc files (johnkerl/miller on Github) -- more complex than ned
- **most** --> Linux pager, better than "less" or "more"
- **guake** --> GUI terminal client for linux, more options than the built in terminal
- **lazydocker** --> TUI terminal software for Docker containers (jesseduffield/lazydocker on Github)
- **exa** --> ls-like file / directory lister, adds colors and more to the standard ls output (https://the.exa.website/)
- **lsd** --> Another ls clone, can show directory sizes (Peltoche/lsd GitHub)
- **json-tui** --> Easy way to review json files, has a cool table view (ArthurSonzogni/json-tui Github)
- **jc** --> Shows common Linux command output in json format 
- **duf** --> Disk utility TUI (muesli/duf on Github)
- **visidata** --> Reading CSV files or other large data sets ([visidata.org](https://www.visidata.org/))
- **croc** --> Seemlessly and securely send files between 2 systems (PC, MAC, Linux, Debian etc) (schollz/croc on Github)
----
* Using jc and json-tui together can produce some pretty results, the top of the picture shows the table view output of ```sudo jc -p lsof -i |json-tui``` 
(the bottom showing the standard ```lsof -i``` results)<br><br>
![image](https://user-images.githubusercontent.com/48565067/155399052-e619f001-f33b-4272-ab3e-3cd43019cc90.png)
----
## Python App "Linux-Sotware-Installer" (Last Updated in September 2022) available under this repo's ```releases``` sectopm
- Requires Python 3.x to run the script, and ```sudo``` access privileges
- Most of the tools require a Debian-like system such as Ubuntu to install (```croc``` by @schollz here on Github is an exception)
- Checks if the above terminal-only software exists, if not installs it
- If you want to migrate this to work on a different OS, just update the code replacing "apt-get" with the different package manager syntax
- Long term goal is to get some of these tools installed via other OS package managers like ```Homebrew``` for ```Mac```and or ```Scoop``` / ```Chocolatey``` for ```Windows```
### Output of "Linux-Software-Installer"
![image](https://user-images.githubusercontent.com/48565067/141710525-a3ccf69b-f2d1-48f3-9fc3-5350229be8a5.png)


