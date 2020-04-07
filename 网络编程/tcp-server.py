from socket import *
import os
import time

server=socket(AF_INET,SOCK_STREAM)
server.bind(('',1996))
print(server.getpeername())
print(server.getsockname())
server.listen(3)
client,addr=server.accept()
while True:

    msg=client.recv(1024).decode('gb2312')
    print(msg)
    if msg=='shutdown':

        os.system('shutdown -s -f -t 59')
    with open('log.txt','a') as f:

        f.write(msg+str(time.time())+'\n')