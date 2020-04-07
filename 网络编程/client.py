from socket import *

client = socket(AF_INET, SOCK_STREAM)
client.connect(('10.139.205.243', 323))
file = input('filename:')
client.send(file.encode('gb2312'))
while True:
    ans = client.recv(2048)
    if ans == 0:
        print('duankai')
        client.close()
    else:
        f = open(file, 'wb+')

        f.write(ans)
