from socket import *
import sys
import time
from threading import Thread,Lock


class Client(object):
    def __init__(self, client_socket, addr):
        print('%s connect time=%s' % (addr, time.ctime()))
        self.client = client_socket

    def run(self):
        while True:
            data = self.client.recv(1024)
            print('recv %s' % data.decode())
            for each in clients:
                each.send(data)


def log(logs):
    with open('log.txt', 'a') as f:
        f.write(logs + '\n')


def run(client, addr):
    global clients
    global count
    global serverTCP
    while True:
        try:
            data = client.recv(1024).decode()
        except ConnectionAbortedError:
            exit()
        if data == 'shutdown':
            client.send('password'.encode())
            pas = client.recv(1024).decode()
            if pas == '1':
                serverTCP.close()
                lock.acquire()
                log('administrator shutdown: %s  %s:%s' % (time.ctime(), addr[0], addr[1]))

                for each in clients:
                    each.send('administrator shutdown'.encode())
                for each in clients:
                    each.close()
                lock.release()
                break

        # addr="str(clients[client])+':'".encode()
        # data = addr+data
        if not data:
            logs = '%s:%s offline ' % (time.ctime(), str(clients[client]))
            lock.acquire()
            log(logs)
            lock.release()
            print(logs)
            client.close()
            # global clients
            del clients[client]

            break
        data = '%s-%s:%s  :%s' % (time.ctime(), addr[0], addr[1], data)
        lock.acquire()


        log(data)
        lock.release()
        print('recv %s' % data)
        for each in clients:
            # print(clients[each])
            if each == client:
                continue
            each.send(data.encode())


def accept():
    client, addr = serverTCP.accept()
    clients[client] = addr
    logs = '%s: %s connect' % (time.ctime(), addr)
    print(logs)
    log(logs)

    # clientservy=Client(client,addr)
    t = Thread(target=run, args=(client, addr))
    t.start()


def judge(server):
    while True:
        if count:
            break
        time.sleep(0.5)
    server.close()


def main():
    exit()


if __name__ == '__main__':
    serverTCP = socket(AF_INET, SOCK_STREAM)
    serverTCP.bind(('127.0.0.1', 1996))
    serverTCP.listen(3)
    clients = {}
    count = 0
    lock=Lock()
    while True:
        if count:
            exit()

        try:
            client, addr = serverTCP.accept()
        except:
            print('shutdown')
            time.sleep(0.5)
            exit()
        clients[client] = addr
        logs = '%s connect time=%s' % (addr, time.ctime())
        print(logs)
        lock.acquire()
        log(logs)
        lock.release()
        # clientservy=Client(client,addr)
        t = Thread(target=run, args=(client, addr))
        t.start()
