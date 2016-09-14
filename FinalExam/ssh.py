import os, socket
import paramiko
import re
import json
import yaml


host = '192.168.6.82'
port = '4114'
user_mysql = 'root'
password_mysql = ''

struct_net = {'192.168.56.101': ['22', '80', '111'], '192.168.56.102': ['22', '80', '111']}

class SSH(object):
    def __init__(self):
        self.ssh = None

    def get_ssh_con(self, host, port, username, password):
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
            self.ssh = ssh
            return ssh

    # find server and port and ssh_connection
    def find_server(self,username, password, struct_net):
        ssh = None
        for host, ports in struct_net.items():
            for port in ports:
                ssh = self.get_ssh_con(host, port, username, password)
                if ssh:
                    return host, port, ssh
        return None, None, ssh

    def find_password(self, ssh_conn, user_mysql='root'):
        passwords=[]
        stdin, stdout, stderr = ssh_conn.exec_command('grep -R password= *')
        data = stdout.read()
        print(data)
        pattern = re.compile('password=([a-zA-Z0-9]+)')
        passwords = pattern.findall(data)
        return passwords

def save_server_info_json(server_ip, ssh_port, login, password):
    info = {
        'ip':server_ip,
        'ssh_port':ssh_port,
        'login':login,
        'password':password
    }
    json.dump(info, open('alesya_server.json', 'w'))

def save_mysql_info_yaml(mysql_pass, mysql_login='root'):
    info = {
        'login':mysql_login,
        'password':mysql_pass
    }
    yaml.dump(info, open('alesya_sql.yaml', 'w'))

def copy_db_file(username, password, server, ssh_port):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.load_host_keys(os.path.expanduser(os.path.join('~', '.ssh', 'known_hosts')))
        ssh.connect(server, port=int(ssh_port), username=username, password=password)
        sftp = ssh.open_sftp()
        path = '/home/{}/db.py'.format(username)
        sftp.put('db.py', path)
        sftp.close()
        ssh.close()
        return True
    except:
        print('Err: ssh copy file')
        ssh.close()
        return False

def check_db():
    pass


if __name__ == "__main__" :
    ssh = SSH()
    username = 'pythonista'
    password = 'letmein'
    password_mysql = ''
    server, ssh_port, ssh_con = ssh.find_server(username, password, struct_net)

    print(server, ssh_port, ssh_con)
    if server and ssh_port and ssh_con:
        save_server_info_json(server, ssh_port, username, password) # save server info
        passwords = ssh.find_password(ssh_con)
        if len(passwords) != 0:
            password_mysql = passwords[0]
        save_mysql_info_yaml(password_mysql)




    print(ssh_con)
    print(copy_db_file(username, password, server, ssh_port))





    #print(passw)

    #
    # for ip, ports in struct_net.items():
    #     ssh = None
    #     for port in ports:
    #         ssh = SSH(ip, port, username, password)
    #
    #         print(ssh_con)
    #

    # ssh = SSH()

# def get_ssh_con(host, port, username, password):
#     ssh = None
#     try:
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(host, int(port), username=username, password=password)
#     except:
#         print('ssh: can not connect')
#         ssh.close()
#         ssh = None
#     finally:
#         return ssh
#
# # find server and port and ssh_connection
# def find_server(username, password, struct_net):
#     ssh = None
#     for host,ports in struct_net.items():
#         for port in ports:
#             ssh = get_ssh_con(host, port, username, password)
#             if ssh:
#                 return host, port, ssh
#     return None, None, ssh
#
# def find_password(user_mysql, ssh_conn):
#     stdin, stdout, stderr = ssh_conn.exec_command('grep -R password= *')
#     data = stdout.read()
#     print(data)
#     pattern = re.compile('password=([a-zA-Z0-9]+)')
#     password = pattern.findall(data)
#     return password
#
# server, port, ssh = find_server('pyautomation', '111', struct_net)
# password=find_password('root', ssh)
# print(password)


