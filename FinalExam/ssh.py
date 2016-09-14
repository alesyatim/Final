import paramiko
import re
import json
import yaml
import pickle
import scaner as scan

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
        stdin, stdout, stderr = ssh_conn.exec_command('grep -R password= *')
        data = stdout.read()
        pattern = re.compile('password=([a-zA-Z0-9]+)')
        return pattern.findall(data)

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


def save_backup(server_ip, ssh_port, login, password, mysql_pass, mysql_login='root'):
    info = {
        'ip':server_ip,
        'ssh_port':ssh_port,
        'login':login,
        'password':password,
        'login_mysql':mysql_login,
        'password_mysql':mysql_pass
    }
    pickle.dump(info, open('alesya_bin_backup.txt', 'w'))

def copy_db_file(username, password, server, ssh_port):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
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

def check_db(server_ip, ssh_port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, port=int(ssh_port), username=username, password=password)
        command = 'python db.py root exam'.format(username)
        stdin, stdout, stderr = ssh.exec_command(command)
    except:
        print('Error: ssh check db')
    finally:
        ssh.close()

if __name__ == "__main__" :
    struct_net = scan.ScanNet().get_struct_net()
    username = 'pythonista'
    password = 'letmein'
    ssh = SSH()

    password_mysql = ''
    server, ssh_port, ssh_con = ssh.find_server(username, password, struct_net)

    if server and ssh_port and ssh_con:
        save_server_info_json(server, ssh_port, username, password)
        passwords = ssh.find_password(ssh_con)
        if len(passwords) != 0:
            password_mysql = passwords[0]
        save_mysql_info_yaml(password_mysql)
        save_backup(server, ssh_port, username, password, password_mysql)

    check_db(server, ssh_port, username, password)



