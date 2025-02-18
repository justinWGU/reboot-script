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


# securely get pw
password = getpass.getpass('Enter password: ')

# TODO: Change input collection to command line.
#hostname = os.getenv('HOSTNAME')
#username = os.getenv('USERNAME')
username = input("Enter username: ")
hostname = input("Enter machine's hostname: ")
command1 = f'ssh {hostname}'

# start new process that establishes conn via ssh
process = pexpect.spawn(command=command1)

# wait for password prompt
try:
    process.expect(r'\(.*@.*\) Password: ', timeout=5)
    print("Password prompt found.")
    #print((process.after.decode()))

# TODO: Make function for catching exceptions. 
except pexpect.exceptions.TIMEOUT:
    print("Password prompt not found. Closing connection and exiting program.")
    process.close()
    sys.exit(1)
 

# Send password to conn via ssh
process.sendline(password)

# TODO: Need to update to handle incorrect pw entries. 
try:
    process.expect(r'Welcome to.*')
    print(f"Successfully connected to {hostname}.")
    #print((process.after.decode()))

except pexpect.exceptions.TIMEOUT:
    print(f"Timed out trying to connect to {hostname}")
    process.close()
    sys.exit(1)

# expect new prompt after welcome message
process.expect(r'\$ ') 
process.sendline('sudo reboot')

# wait for possible prompts
prompts = [r'\[sudo\] password for .*', r'(W: molly-guard)([\s\S]*)'] # These didn't work: 'W\: molly\-guard .*', r'W: molly-guard.*'

try:
    index = process.expect(prompts)
    #print((process.after.decode()))

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
    print("Timed out after sudo password prompt.")
    process.close()
    sys.exit(1)

process.close()