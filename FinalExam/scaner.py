import os
import socket
import re


res = os.system('which nmap')
print res

def get_my_ip():
    pass

def get_alt_open_ports(ip):
    ports = []
    try:
        res = os.system('which nmap')
        if not res == 0:
            ports = get_open_ports(ip)
        else:
            os.system('nmap {} | grep ssh > 1.txt'.format(ip))
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
            open_ports.append(str(port))
        sock.close()
    return open_ports

def get_struct_net():
    struct_net = {}
    for ip in  ping_computers():
        struct_net[ip] = get_open_ports(ip)
    return struct_net
# struct_net = {x:y for x in ping_computers() for y in get_open_ports(x)}

# struct_net = get_struct_net()
# print(struct_net)
ip = get_my_ip()
print(ip)


print(get_alt_open_ports('192.168.56.101') )


