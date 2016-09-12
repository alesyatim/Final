import os, socket
import paramiko
import re

# username='pythonista', password='letmein'
host = '192.168.6.82'
port = '4114'
user_mysql = 'root'
password_mysql = ''


try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, int(port), username='pythonista', password='letmein')
except:
    print('can not connect')
else:
    stdin, stdout, stderr  = ssh.exec_command('grep -R password= *')
    data = stdout.read()
    print(data)
    pattern = re.compile('password=([a-zA-Z0-9]+)')
    password = pattern.findall(data)
    print(password)


    # scan dir for password
finally:
    ssh.close()

def get_ssh_connector(post):
    conn = None
    try:
        conn = paramiko.ssh
    except:
        pass


