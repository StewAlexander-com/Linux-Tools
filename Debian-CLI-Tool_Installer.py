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

#Check if the system is debian, else halt program
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



#Check if these programs exist [chkservice,htop,nnn,ncdu,network-manager,ne,hping3,nmap,lynis,apt-show-versions,vim,fish,tig,bmon,dnsutils,most], if not install them
def check_programs():
    programs = ['chkservice','htop','nnn','ncdu','network-manager','ne','hping3','nmap','lynis','apt-show-versions','vim','fish','tig','bmon','dnsutils','most','curl']
    os.system('sudo apt update')
    for program in programs:
        if which(program) is None:
            print("\n>> \"" + program + '\" is not installed')
            install_program(program)
        else:
            print("- \"" + program + '\" is installed')
            

# Check if program in list programs appears to be available in apt, if so download it
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


#Check if eget is installed, if not install eget
def eget_installer ():
#check if eget exists as a program
    eget_exists = os.path.exists('/usr/bin/eget')
    if not eget_exists:
       print("Eget does not exist, installing",'\n') 
       #install eget
       os.system("curl https://zyedidia.github.io/eget.sh | sh")
       #move eget to /usr/bin
       os.system("sudo mv eget /usr/bin/eget")
    else:
        print("- \"eget\" is is installed",'\n')
        pass

#Install eget programs from github source
def eget_install():
    if eget_program == 'lsd':
        os.system("eget Peltoche/lsd")
    elif eget_program == 'sd':
        os.system("eget chmln/sd")
    elif eget_program == 'lazygit':
        os.system("eget jesseduffield/lazygit")   
    else:
        print('Program not found\n')


#Copies the file downloaded via eget to the /usr/bin/

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
