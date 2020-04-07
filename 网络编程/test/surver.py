from socket import *

sur=socket(AF_INET,SOCK_STREAM)
sur.bind(('',323))
sur.listen(5)
c,addr=sur.accept()
data=c.recv(1024)
print(str(data))
c.send('111'.encode('gb2312'))