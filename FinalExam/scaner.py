import os
import socket
import re
# import ssh
import json
import yaml

server_info = {'host':'', 'port':'', 'user':'pythonista', 'password':'letmein'}
host = '192.168.6.82'

def get_alt_open_ports(ip):
    ports = []
    try:
        res = os.system('which nmap')
        if not res == 0:
            ports = get_open_ports(ip)
        else:
            os.system('sudo nmap {} -p 4100-4200 | grep tcp > 1.txt'.format(ip))
            with open('1.txt', 'r') as f:
                text = f.read()
                patt = re.compile('([0-9]{1,5})')
                ports = patt.findall(text)
    except:
        print('error nmap')
        ports = get_open_ports(ip)
        #return ports
    finally:
        return ports

#  find available computers
def ping_computers():
    computers = []
    for i in xrange(70,90):
        host = '192.168.6.'+str(i)
        print(host)
        response = os.system('ping -c 1 ' + host)
        if response == 0:
            computers.append(host)
    return computers

# find open ports
def get_open_ports(ip):
    open_ports = []
    for port in xrange(4100,4200):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.01)
        try:
            sock.connect((ip, port))
        except:
            pass
        else:
            open_ports.append(str(port))
        sock.close()
    return open_ports

def get_struct_net():
    struct_net = {}
    for ip in  ping_computers():
        struct_net[ip] = get_alt_open_ports(ip)
    return struct_net

##########################################
struct_net = get_struct_net()
print(struct_net)
json.dump(struct_net, open('struct_net', 'w'))
##########################################



