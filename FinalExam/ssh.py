import os, socket
import paramiko
import re

# username='pythonista', password='letmein'
host = '192.168.6.82'
port = '4114'
user_mysql = 'root'
password_mysql = ''

struct_net = {"192.168.56.101": ['1', '16', '80', '111','222', '21', "22", "80", "111"]}

def get_ssh_con(host, port, username, password):
    ssh = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, int(port), username=username, password=password)
    except:
        print('ssh: can not connect')
        ssh.close()
        ssh = None
    finally:
        return ssh

# find server and port and ssh_connection
def find_server(username, password, struct_net):
    ssh = None
    for host,ports in struct_net.items():
        for port in ports:
            ssh = get_ssh_con(host, port, username, password)
            if ssh:
                return host, port, ssh
    return None, None, ssh

def find_password(user_mysql, ssh_conn):
    stdin, stdout, stderr = ssh_conn.exec_command('grep -R password= *')
    data = stdout.read()
    print(data)
    pattern = re.compile('password=([a-zA-Z0-9]+)')
    password = pattern.findall(data)
    return password

server, port, ssh = find_server('pyautomation', '111', struct_net)
password=find_password('root', ssh)
print(password)


