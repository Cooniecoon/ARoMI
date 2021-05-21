import socket

from socket_funcs import *


# 송신을 위한 socket 준비
TCP_PORT = 8888
TCP_IP='ec2-3-34-2-20.ap-northeast-2.compute.amazonaws.com'
sock_neck = socket.socket()
sock_neck.connect((TCP_IP, TCP_PORT))

print('connected')
while True:
    msg=sock_neck.recv(9)
    print('msg : ',msg.decode())
    x,y=msg.decode().split(',')
    x,y=float(x),float(y)
    print(f'x : {x},  y : {y}')
    if msg == None:
        break

sock_neck.close()