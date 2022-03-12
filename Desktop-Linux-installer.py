#!/usr/bin/env python3
import os
import sys
import uuid
from shutil import which

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
>> guake
>> jc
>> geany
>> cdpr
>> exa
>> guake
>> python3
>> python3-pip
>> chromaterm 
>> visidata
\n""")

#Check if these programs exist [chkservice,htop,nnn,ncdu,network-manager,ne,hping3,nmap,lynis,apt-show-versions,vim,fish,tig,bmon,dnsutils,most], if not install them
def check_programs():
    programs = ['chkservice','htop','nnn','ncdu','network-manager','ne','hping3','nmap','lynis','apt-show-versions','vim','fish','tig','bmon','dnsutils','most', 'guake', 'jc', 'geany', 'cdpr', 'exa', 'guake', 'python3', 'python3-pip', 'chromaterm', 'visidata']
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
    elif program == 'guake':
        os.system('sudo apt-get install guake')
        print("\n")
    elif program == 'jc':
        os.system('sudo apt-get install jc')
        print("\n")
    elif program == 'geany':
        os.system('sudo apt-get install geany')
        print("\n")
    elif program == 'cdpr':
        os.system('sudo apt-get install cdpr')
        print("\n")
    elif program == 'exa':
        os.system('sudo apt-get install exa')
        print("\n")
    elif program == 'guake':
        os.system('sudo apt-get install guake')
        print("\n")
    elif program == 'python3':
        os.system('sudo apt-get install python3')
        print("\n")
    elif program == 'python3-pip':
        os.system('sudo apt-get install python3-pip')
        print("\n")
    elif program == 'chromaterm':
        os.system('pip3 install chromaterm')
        print("\n")
    elif program == 'visidata':
        os.system('pip3 install visidata')
        print("\n")
    else:
        print('Program not found\n')

#run check_programs()
check_programs()

#Press reuturn to quit
input('\n\nPress return to quit')
sys.exit()

