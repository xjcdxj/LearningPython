from socket import *

cient=socket(AF_INET,SOCK_STREAM)
cient.connect(('10.139.205.243',323))
cient.send('234'.encode('gb2312'))
data=cient.recv(1024)
print(str(data))