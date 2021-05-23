import socket

from socket_funcs import *


# 송신을 위한 socket 준비
TCP_PORT = 8888
with open('AWS_IP.txt', 'r') as f:
    TCP_IP = f.readline()

sock_neck = socket.socket()
sock_neck.connect((TCP_IP, TCP_PORT))

print('connected')
while True:
    # msg=sock_neck.recv(6)
    msg=recv_msg_from(sock_neck)
    print('msg : ',msg)
    if msg != '':
        x=float(msg)
        print('x : ',x)
    if msg == None:
        break

sock_neck.close()