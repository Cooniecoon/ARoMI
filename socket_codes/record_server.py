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
t = 0
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

# classifier
TCP_PORT_classifier = 4444
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_classifier))
s.listen(True)
classifier_client, addr = s.accept()
print("classifier connected")


# camera node
TCP_PORT_cam = 6666
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_cam))
s.listen(True)
cam_client, addr = s.accept()
print("camera node connected")


while True:
    # 이미지 받아서 보내주기
    # cam -> img

    img=recv_img_from(cam_client)
    send_image_to(img,img_client,dsize=(432, 368))

    img_person=recv_img_from(img_client)
    send_image_to(img_person,cam_client,dsize=(432, 368))

    # img_people=recv_img_from(classifier_client)
    # send_image_to(img_people,cam_client,dsize=(432, 368))


s.close()