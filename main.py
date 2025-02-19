# Justin Ortiz Reboot Script

import pexpect
import getpass
import sys
import os
from pathlib import Path
from dotenv import load_dotenv


# load env vars
env_file = Path('.env').resolve()
load_dotenv(env_file)

def getpassword():
    
    prompts = [r'Welcome to.*', r'\(.*@.*\) Password: ']

    results = 1    
    while results == 1:
        password = getpass.getpass('Enter password: ')
        
        print('Checking password')
        process.sendline(password)
        results = process.expect(prompts, timeout=5)

        if results == 1:
            print('Incorrectly typed password. Please try again. ')

    print(f"Successfully connected to {hostname}. Got welcome message.")
    
    return password


# TODO: Change input collection to command line.
#hostname = os.getenv('HOSTNAME')
#username = os.getenv('USERNAME')
username = input("Enter username: ")
hostname = input("Enter machine's hostname: ") # TODO: strip input of spaces
command1 = f'ssh {hostname}'

# start new process that establishes conn via ssh
process = pexpect.spawn(command=command1)
ssh_prompts = [r'\(.*@.*\) Password: ', r'The authenticity of host ([\s\S]*)']
# wait for password prompt

try:
    result1 = process.expect(ssh_prompts, timeout=5)
    
    if result1 == 1:
        print(f'Adding {hostname} to list of known machines.')
        process.sendline('Yes')
        process.expect(r'Warning ([\s\S]*)')
    
    password = getpassword()


except pexpect.exceptions.TIMEOUT:
    print(f'Could not connect to {hostname}.')
    process.close()
    sys.exit(1)
 


try:
    
    # wait for possible prompts
    prompts = [r'\[sudo\] password for .*', r'(W: molly-guard)([\s\S]*)'] # These didn't work: 'W\: molly\-guard .*', r'W: molly-guard.*'

    # expect new prompt after welcome message
    process.expect(r'\$ ') 
    print('Got new prompt. Sending reboot command.')
    process.sendline('sudo reboot')
    print('Sent reboot command.')
    
    index = process.expect(prompts)
    # prompted for sudo pw
    if index == 0: 
        process.sendline(password)
        print('Sent pw to reboot.')
        try:
            process.expect(prompts[1])
            print('Got mollyguard msg.')
            process.sendline(hostname)
            print('Sent hostname to mollyguard')
            try:
                process.expect(r'Connection to ([\s\S]*)')
                #print('print after: ', process.after.decode())
                print(f'Successfully rebooted {hostname}.')
            except pexpect.exceptions.TIMEOUT:
                print('Timed out waiting for reboot confirmation.')
                process.close()
                sys.exit(1)
        except pexpect.exceptions.TIMEOUT:
            print('Timed out waiting for mollyguard message.')
            process.close()
            sys.exit(1)
    
    # propmted for hostname
    elif index == 1: 
        process.sendline(hostname)
        try:
            process.expect(r'Connection to ([\s\S]*)')
            #int(process.after.decode())
            print(f'Successfully rebooted {hostname}.')
        except pexpect.exceptions.TIMEOUT:
            print('Timed out waiting for reboot confirmation.')
            process.close()
            sys.exit(1)

except pexpect.exceptions.TIMEOUT:
    print("Error occurred trying to reboot machine.")
    process.close()
    sys.exit(1)

process.close()

# # 11:10:20 systems06:~$ ssh rws098
# The authenticity of host 'rws098 (10.10.120.107)' can't be established.
# ED25519 key fingerprint is SHA256:esvdiKJVT03tM08QeX3eXEqssuxvKDGrborPpMZhYZo.
# This key is not known by any other names
# Are you sure you want to continue connecting (yes/no/[fingerprint])? 
# Warning: Permanently added 'rws098' (ED25519) to the list of known hosts.
# (jortiz@rws098) Password: 