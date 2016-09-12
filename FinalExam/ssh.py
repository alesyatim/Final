import os, socket
import paramiko
import re

# username='pythonista', password='letmein'

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.56.101', port=22, username='pyautomation', password='111')
except:
    print('jhh')
else:
    stdin, stdout, stderr  = ssh.exec_command('ls -l | grep ^-')
    data = stdout.read()
    pattern = re.compile('[0-9]{2}:[0-9]{2}(.+)')
    files = pattern.findall(data)
    print(files)

    # scan dir for password
finally:
    ssh.close()

def read_file_by_line(name_file):
    with open(name_file, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            yield line


def read_file(name_file):
    t = []
    line_gen = read_file_by_line(name_file)
    for line in line_gen:
          t.append(line)
    return t

s = read_file('1.txt')
print s