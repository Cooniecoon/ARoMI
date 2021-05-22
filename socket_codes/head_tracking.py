import socket

from socket_funcs import *


# 송신을 위한 socket 준비
TCP_PORT = 8888
TCP_IP='127.0.0.1'

sock_neck = socket.socket()
sock_neck.connect((TCP_IP, TCP_PORT))

print('connected')
while True:
    msg=sock_neck.recv(6)
    print('msg : ',msg.decode())
    x=float(x)
    if msg == None:
        break

sock_neck.close()