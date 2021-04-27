import socket
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
from collections import deque


from socket_funcs import *

with open('message_code.json', 'r') as f:
    messages = json.load(f)

a1 = deque([0]*200)
ax = plt.axes(xlim=(0, 30), ylim=(0, 50))


line, = plt.plot(a1)
plt.ion()
plt.ylim([0,50])
plt.show()

# 연결할 서버(수신단)의 ip주소와 port번호
TCP_IP = "ec2-13-209-8-64.ap-northeast-2.compute.amazonaws.com"
TCP_PORT = 1997

# 송신을 위한 socket 준비
aws_server = socket.socket()
aws_server.connect((TCP_IP, TCP_PORT))
a=[]
while True:
    fps=aws_server.recv(4)
    msg=messages['roger']
    aws_server.send(msg.encode())
    fps=float(fps.decode())

    a1.appendleft(fps)
    datatoplot = a1.pop()
    line.set_ydata(a1)
    plt.draw()
    plt.pause(0.0001) 

aws_server.close()
