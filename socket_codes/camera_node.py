import socket
import cv2
import numpy as np

from socket_funcs import *

with open('message_code.json', 'r') as f:
    messages = json.load(f)

# messages={'roger':'r', 'pass':'p','chatbot':'c','break':'b'}
print('message code : ',messages)

cam=cv2.VideoCapture(0)
# cam.set(3,640)
# cam.set(4,480)
TCP_IP = "127.0.0.1"
TCP_PORT_img = 5555

# 송신을 위한 socket 준비
sock_cam = socket.socket()
sock_cam.connect((TCP_IP, TCP_PORT_img))
print('connected')
while True:
    _,img=cam.read()
    cv2.imshow('cam',img)
    send_image_to(img,sock_cam,dsize=(432, 368))
    if cv2.waitKey(1)==27:
        break