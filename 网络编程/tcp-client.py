from socket import *

client = socket(AF_INET, SOCK_STREAM)
client.connect(('192.138.137.1', 1337))
while True:
    x = input('send:')
    client.send(x.encode('gb2312'))
    if x == 'quit':
        break
client.close()
