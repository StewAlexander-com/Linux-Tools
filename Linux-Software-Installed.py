#!/usr/bin/env python3
import os
import sys
import uuid
from shutil import which

#Check if the system is debian, else halt program
is_debian = which("apt-get")

if is_debian:
    pass
else:
    sys.exit("This script requires a Debian-like system such as Ubuntu, Debian or Linux Mint")

#Print checking if these programs are installed or not
print("""\nChecking if these programs are installed or not:\n
>> chkservice
>> htop
>> nnn
>> ncdu
>> network-manager
>> ne
>> hping3
>> nmap
>> lynis
>> apt-show-versions
>> vim
>> fish
>> tig
>> bmon
>> dnsutils
>> most
>> \n""")

#Check if these programs exist [chkservice,htop,nnn,ncdu,network-manager,ne,hping3,nmap,lynis,apt-show-versions,vim,fish,tig,bmon,dnsutils,most], if not install them
def check_programs():
    programs = ['chkservice','htop','nnn','ncdu','network-manager','ne','hping3','nmap','lynis','apt-show-versions','vim','fish','tig','bmon','dnsutils','most','curl']
    for program in programs:
        if which(program) is None:
            print("\n>> \"" + program + '\" is not installed')
            install_program(program)
        else:
            print("- \"" + program + '\" is installed')

#Install programs
def install_program(program):
    if program == 'chkservice':
        os.system('sudo apt-get install chkservice')
        print("\n")
    elif program == 'htop':
        os.system('sudo apt-get install htop')
        print("\n")
    elif program == 'nnn':
        os.system('sudo apt-get install nnn')
        print("\n")
    elif program == 'ncdu':
        os.system('sudo apt-get install ncdu')
        print("\n")
    elif program == 'network-manager':
        os.system('sudo apt-get install network-manager')
        print("\n")
    elif program == 'ne':
        os.system('sudo apt-get install ne')
        print("\n")
    elif program == 'hping3':
        os.system('sudo apt-get install hping3')
        print("\n")
    elif program == 'nmap':
        os.system('sudo apt-get install nmap')
        print("\n")
    elif program == 'lynis':
        os.system('sudo apt-get install lynis')
        print("\n")
    elif program == 'apt-show-versions':
        os.system('sudo apt-get install apt-show-versions')
        print("\n")
    elif program == 'vim':
        os.system('sudo apt-get install vim')
        print("\n")
    elif program == 'fish':
        os.system('sudo apt-get install fish')
        print("\n")
    elif program == 'tig':
        os.system('sudo apt-get install tig')
        print("\n")
    elif program == 'bmon':
        os.system('sudo apt-get install bmon')
        print("\n")
    elif program == 'dnsutils':
        os.system('sudo apt-get install dnsutils')
        print("\n")
    elif program == 'most':
        os.system('sudo apt-get install most')
        print("\n")
    elif program == 'curl':
        os.system('sudo apt-get install curl')    
    else:
        print('Program not found\n')

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
        print("Eget already installed",'\n')
        pass

# Check if eget programs are instaled or not
def check_eget_programs():
    eget_programs = ['lsd']
    for eget_program in eget_programs:
        if which(eget_program) is None:
            print("\n>> \"" + eget_program + '\" is not installed')
            eget_install(eget_program)
        else:
            print("- \"" + eget_program + '\" is installed')
            pass

#Install eget programs from github source
def eget_install(eget_program):
    if eget_program == 'lsd':
        os.system("eget Peltoche/lsd ")
    else:
        print('Program not found\n')

#run eget_installer()
eget_installer

#run check_programs()
check_programs()

# Check if eget GitHub related programs are installed or not




#Press reuturn to quit
input('\n\nPress return to quit')
sys.exit()

