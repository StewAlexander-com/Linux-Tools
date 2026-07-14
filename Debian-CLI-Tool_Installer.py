#!/usr/bin/env python3

import subprocess
import os
import sys
import uuid
import shutil
from shutil import which

# Why do this in python instead of 
# bash? I don't use bash, second of all
# eventually I want to make this cross
# platform, and why not?

# Basically a learning tool 
# Tha vast majority of this
# Can be solved by a xargs call
# to a flat file list of apps, and a check if
# apt doesn't have it, try eget

file_pass = 'a'

# Verify Debian-based system via apt-get presence
is_debian = which("apt-get")

if is_debian:
    pass
else:
    sys.exit("This script requires a Debian-like system such as Ubuntu, Debian or Linux Mint")

#Ask if you want to install these files, if not quit the program

file_start = input("""\nDo you want to install the below files?:\n
>> chkservice - TUI systemd unit manager
>> htop - TUI top clone on steroids
>> nnn  - TUI file explorer
>> ncdu - TUI du clone, easily find what is taking up space
>> network-manager - Installs nmtui, a way to manage wireless network connections
>> ne - Nano clone, with some nice options 
>> hping3 - Ping on steroids, useful on solving network issues
>> nmap - Network mapping tool, insanely powerful
>> lynis - Linux security and configuration audit tool
>> apt-show-versions - Show the versions of software installed and what needs updating
>> vim - Vi Improved, editor par exelance for Linux
>> fish - Friendly Interactive Shell - many improvements over bash
>> tig - TUI Git tool
>> bmon - Bandwith monitor 
>> dnsutils - Installs dig, the DNS linux wonder-tool
>> most - pager like "less" and "more" with more options
>> eget (Github software installer)
>> lsd - ls clone that show nice icons if a nerdfont is installed
>> sd - sed clone with easier syntax
>> Lazygit - TUI git tool, works well in conjunction with tig
\n\"y\" or \"n\"?\n> """)

if file_start != 'n':
    pass
else:
    print("Quitting program")
    sys.exit()



# Check each program in PATH; install missing ones via apt
def check_programs():
    programs = ['chkservice','htop','nnn','ncdu','network-manager','ne','hping3','nmap','lynis','apt-show-versions','vim','fish','tig','bmon','dnsutils','most','curl']
    os.system('sudo apt update')
    for program in programs:
        if which(program) is None:
            print("\n>> \"" + program + '\" is not installed')
            install_program(program)
        else:
            print("- \"" + program + '\" is installed')
            

# Verify package exists in apt cache before installing
def install_program(program):
    try:
        output = subprocess.run(["apt-cache", "search",program], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if output.returncode == 0:
            os.system("sudo apt-get install -y " + program)
            print(f"{program} has been installed successfully.")
        else:
            print(f"{program} is not available via apt.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


# Install eget if missing; downloads verified GitHub release (no curl|sh)
def eget_installer():
    eget_exists = which("eget") is not None or os.path.exists('/usr/local/bin/eget') or os.path.exists('/usr/bin/eget')
    if eget_exists:
        print("- \"eget\" is installed", '\n')
        return

    print("Eget does not exist, installing from GitHub releases (no curl|sh)", '\n')
    import platform
    import tempfile
    import tarfile
    import json
    from pathlib import Path

    arch_map = {
        "x86_64": "amd64", "amd64": "amd64",
        "aarch64": "arm64", "arm64": "arm64",
        "armv7l": "arm", "i386": "386", "i686": "386",
    }
    arch = arch_map.get(platform.machine().lower())
    if not arch:
        print(f"Unsupported architecture: {platform.machine()}")
        return

    api = "https://api.github.com/repos/zyedidia/eget/releases/latest"
    with tempfile.TemporaryDirectory(prefix="eget-") as tmpdir:
        meta_path = os.path.join(tmpdir, "release.json")
        if os.system(
            f'curl --fail --location --silent --show-error '
            f'--connect-timeout 30 --max-time 120 -o "{meta_path}" "{api}"'
        ) != 0:
            print("Failed to fetch eget release metadata")
            return
        with open(meta_path, encoding="utf-8") as handle:
            release = json.load(handle)
        tag = release.get("tag_name", "").lstrip("v")
        asset_name = f"eget-{tag}-linux_{arch}.tar.gz"
        url = next(
            (a.get("browser_download_url") for a in release.get("assets", [])
             if a.get("name") == asset_name),
            None,
        )
        if not url:
            print(f"No release asset {asset_name}")
            return
        archive = os.path.join(tmpdir, asset_name)
        if os.system(
            f'curl --fail --location --silent --show-error '
            f'--connect-timeout 30 --max-time 120 -o "{archive}" "{url}"'
        ) != 0:
            print("Failed to download eget archive")
            return
        with tarfile.open(archive, "r:gz") as tar:
            member = next(
                (m for m in tar.getmembers() if Path(m.name).name == "eget" and m.isfile()),
                None,
            )
            if member is None:
                print("eget binary missing from archive")
                return
            # Reject path traversal in older Python without tar filter=
            if os.path.isabs(member.name) or ".." in Path(member.name).parts:
                print("Refusing unsafe tar member")
                return
            try:
                tar.extract(member, path=tmpdir, filter="data")
            except TypeError:
                tar.extract(member, path=tmpdir)
            extracted = os.path.join(tmpdir, member.name)
        # Basic ELF sanity check before privileged install
        with open(extracted, "rb") as handle:
            if handle.read(4) != b"\x7fELF":
                print("Refusing to install non-ELF eget binary")
                return
        os.chmod(extracted, 0o755)
        staged = os.path.join(os.getcwd(), "eget")
        shutil.copy2(extracted, staged)
        os.system(f'sudo mv "{staged}" /usr/local/bin/eget')
        # Post-install validation
        if which("eget") or os.path.exists("/usr/local/bin/eget"):
            print("eget installed and present on PATH")
        else:
            print("eget install may have failed validation")


# Download binaries from GitHub releases using eget
def eget_install():
    if eget_program == 'lsd':
        os.system("eget lsd-rs/lsd")
    elif eget_program == 'sd':
        os.system("eget chmln/sd")
    elif eget_program == 'lazygit':
        os.system("eget jesseduffield/lazygit")   
    else:
        print('Program not found\n')


# Move eget-downloaded binaries from current dir to PATH
def eget_copy():
    for eget_program in eget_programs:
        if os.path.exists(eget_program):
            os.system('sudo cp '+eget_program+' /usr/bin/')
            print("\nCopied \"" + eget_program + "\" to /usr/bin")
            pass
        else:
            pass

#run eget_installer()
eget_installer()


eget_programs = ['lsd','sd','lazygit']
for eget_program in eget_programs:
    if which(eget_program) is None:
        print("\n>> \"" + eget_program + '\" is not installed')
        eget_install(eget_program)
    else:
        print("- \"" + eget_program + '\" is installed')
        pass


#run eget_copy()
eget_copy()

#run check_programs()
check_programs()

#Press reuturn to quit
input('\n\nPress return to quit')
sys.exit()
