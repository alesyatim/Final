import os
import socket


def get_my_ip():
    pass

#  find available computers
def ping_computers():
    computers = []
    for i in xrange(100,105):
        host = '192.168.56.'+str(i)
        response = os.system('ping -c 1 ' + host)
        if response == 0:
            computers.append(host)
    return computers

# find open ports
def get_open_ports(ip):
    open_ports = []
    for port in xrange(65536):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.01)
        try:
            sock.connect((ip, port))
        except:
            pass
        else:
            open_ports.append(port)
        sock.close()
    return open_ports

def get_struct_net():
    struct_net = {}
    for ip in  ping_computers():
        struct_net[ip] = get_open_ports(ip)
    return struct_net
# struct_net = {x:y for x in ping_computers() for y in get_open_ports(x)}

struct_net = get_struct_net()
print(struct_net)

HOST = '192.168.6.1'
PORT = ''