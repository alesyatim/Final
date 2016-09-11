import os
for i in range(1,10):
    host = '192.168.6.'+str(i)
    response = os.system('ping -c 1 ' + host)
    if response == 0:
        print(host + 'is up')
    else: print(host + 'is down')

HOST = '192.168.6.1'
PORT = ''