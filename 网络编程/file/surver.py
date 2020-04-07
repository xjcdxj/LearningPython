from socket import *
import os
from threading import Thread

# class Surver():
#     #surver对象
#     def __init__(self,client):
#         self.client=client
#     #接受客户端传的参数
#     def recvData(self):
#         pass
#     #打开文件的方法
#     def openFile(self):
#         pass
#     def send(self):
#
def upload(fileName,client):
    if fileName in os.listdir():
        f=open(fileName,'rb')
        while True:
            data = f.read(2048)
            if data==0:
                client.close()
            else:

                client.send(data)

def creat(client):
    clientSocket=client[0]
    addr=client[1]
    clientSocket.send('输入文件名：'.encode('gb2312'))
    ans=clientSocket.recv(1024).decode('gb2312')
    if ans==0:
        print('%sdisconnect'%str(addr))
    else:
        upload(ans,clientSocket)
        print('require:%s'%ans.decode('gb2312'))


def main():

    surverTcp=socket(AF_INET,SOCK_STREAM)
    surverTcp.bind(('',323))
    surverTcp.listen(5)
    clients=[]
    while True:
        client=surverTcp.accept()
        clients.append(client)
        t=Thread(target=creat,args=(client,))
        t.start()
        print(str(client[1]))

if __name__ == '__main__':
    main()
