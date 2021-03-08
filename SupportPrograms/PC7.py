# Perform terminal commands via ssh
# Regards, Sam Macharia

import os,sys,paramiko

PC6 = '10.226.27.27'
name = 'nitta'
pswd = 'kinesin'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(hostname=PC6, username=name, password=pswd)
except:
    print("[!] Cannot connect to the SSH Server")
    exit()

commands = ["pwd","id","uname -a","df -h","ls Documents/Sam"]

for command in commands:
    print("="*50, command, "="*50)
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err:
        print(err)

input('Press Enter to Exit')