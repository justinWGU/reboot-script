# Justin Ortiz Reboot Script

import subprocess


# collect password
password = input("Enter password: ")

# collect hostname
hostname = input("Enter machine's hostname: ")
command1 = f'ssh {hostname}'

# call process. Ssh into machine then reboot
process = subprocess.Popen(
    args=command1,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# send password to process
stdout, stderr = process.communicate(input=password)
if not stderr:
    print(f"Successfully ssh'd into machine. {stdout}")

command2 = 'sudo -S reboot'
process = subprocess.Popen(
    args=command2,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# send password to process
stdout, stderr = process.communicate(input=password)
if not stderr:
    print(f'Successfully rebooted machine. {stdout}')

# Output success