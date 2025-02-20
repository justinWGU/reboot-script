# Justin Ortiz Reboot Script

import argparse
import pexpect
import getpass
import sys
import os

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
parser = argparse.ArgumentParser(description="Parser to get hostname.")
parser.add_argument("hostname", type=str, help="The machine you want to reboot.")
args = parser.parse_args()
print(f"Hostname equals: {args.hostname}")

username = os.getlogin()
print(username)
hostname = str(args.hostname)
command1 = f'ssh {hostname}'

# start new process that establishes conn via ssh
process = pexpect.spawn(command=command1)
ssh_prompts = [r'\(.*@.*\) Password: ', r'The authenticity of host ([\s\S]*)']
# TODO: handle case where hostname is not found 

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

except pexpect.exceptions.EOF:
    print(f'Error occurred connecting to {hostname}.')
    print(process.before.decode())
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
    
    # send sudo pw if necessary, then hostname for molly-guard
    if index == 0: 
        
        process.sendline(password)
        print('Sent pw to reboot.')
        
        process.expect(prompts[1])

    # Send hostname to molly-guard
    print('Got mollyguard msg. Sending hostname.')
    process.sendline(hostname)

    process.expect(r'Connection to ([\s\S]*)')
    print(f'Successfully rebooted {hostname}.')
   

except pexpect.exceptions.TIMEOUT:
    print("Error occurred trying to reboot machine.")
    process.close()
    sys.exit(1)

finally:
    process.close()