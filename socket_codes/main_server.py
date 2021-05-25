import socket
import cv2
import numpy as np
import time
import json

from socket_funcs import *

with open('message_code.json', 'r') as f:
    messages = json.load(f)

# messages={'roger':'r', 'pass':'p','chatbot':'c','break':'b'}
print('message code : ',messages)

with open('AWS_IP.txt', 'r') as f:
    TCP_IP = f.readline()
print(TCP_IP)
# eye contact checker
TCP_PORT_eyes = 1111
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_eyes))
s.listen(True)
eyes_client, addr = s.accept()
print("eye contact checker connected")

# image receiver
TCP_PORT_img = 2222
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_img))
s.listen(True)
img_client, addr = s.accept()
print("image  receiver connected")

# nose coordinate send
TCP_PORT_nose = 3333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_nose))
s.listen(True)
nose_client, addr = s.accept()
print("nose connected")

# FacER
TCP_PORT_FacER = 4444
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_FacER))
s.listen(True)
FacER_client, addr = s.accept()
print("FacER connected")

# pose
TCP_PORT_pose = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_pose))
s.listen(True)
pose_client, addr = s.accept()
print("pose classifier connected")

# camera node
TCP_PORT_cam = 6666
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_cam))
s.listen(True)
cam_client, addr = s.accept()
print("camera node connected")


# chatbot
TCP_PORT_chatbot = 7777
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_chatbot))
s.listen(True)
chatbot_client, addr = s.accept()
print("chatbot connected")


# HEAD
TCP_PORT_HEAD = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_HEAD))
s.listen(True)
head_client, addr = s.accept()
print("Robot head connected")


'''
h 행복
s 슬픔
n 중립
d 일상
b 인사
'''
while True:
    # 이미지 받아서 보내주기
    # cam -> img

    img=recv_img_from(cam_client)
    send_image_to(img,img_client,dsize=(432, 368))

    # nose_xy=recv_msg_from(nose_client)
    # print('nose_xy : ',nose_xy)
    # send_message_to(nose_xy,head_client)

    a2b(eyes_client,chatbot_client)

    # img=recv_img_from(img_client)
    # send_image_to(img,cam_client,dsize=(432, 368))

    nose_xy=recv_msg_from(nose_client)
    send_message_to(nose_xy,head_client)
    # print('nose_xy : ',nose_xy)

s.close()