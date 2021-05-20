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
with open('AWS_IP.txt', 'r') as f:
    TCP_IP = f.readline()
TCP_PORT_img = 5555

# 송신을 위한 socket 준비
sock_cam = socket.socket()
sock_cam.connect((TCP_IP, TCP_PORT_img))
print('connected')
while True:

    _,img=cam.read()
    send_image_to(img,sock_cam,dsize=(432, 368))

    img_body=recv_img_from(sock_cam)
    # img_face=recv_img_from(sock_cam)


    cv2.imshow('cam',img)
    cv2.imshow("camera node pose result", img_body)
    # cv2.imshow("camera node face result", img_face)
    if cv2.waitKey(1)==27:
        break