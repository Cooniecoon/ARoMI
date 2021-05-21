import socket

TCP_PORT = 7777
TCP_IP='127.0.0.1'


# 송신을 위한 socket 준비
sock_neck = socket.socket()
sock_neck.connect((TCP_IP, TCP_PORT))

print('connected')
while True:
    msg=sock_neck.recv(9)
    if msg == None:
        break
    # print(msg.decode())
    x,y=msg.decode().split(',')
    x,y=float(x),float(y)
    print(f'x : {x},  y : {y}')

sock_neck.close()