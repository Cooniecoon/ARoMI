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

# camera
with open('AWS_IP.txt', 'r') as f:
    TCP_IP = f.readline()

print(TCP_IP)
TCP_PORT_img = 5555
ssss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssss.bind((TCP_IP, TCP_PORT_img))
ssss.listen(True)
cam_client, addr = ssss.accept()
print("camera connected")

# chatbot
TCP_PORT_chatbot = 2424
sss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sss.bind((TCP_IP, TCP_PORT_chatbot))
sss.listen(True)
chatbot_client, addr = sss.accept()
print("chatbot connected")

# pose
TCP_PORT_pose = 4242
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_pose))
s.listen(True)
pose_client, addr = s.accept()
print("pose_classifier connected")

# image
TCP_PORT_img = 6666
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind((TCP_IP, TCP_PORT_img))
ss.listen(True)
img_client, addr = ss.accept()
print("image connected")


while True:
    # 이미지 받아서 보내주기
    # cam -> img

    img=recv_img_from(cam_client)

    send_image_to(img,img_client,dsize=(432, 368))

    a2b(pose_client,chatbot_client)

    img=recv_img_from(img_client)
    send_image_to(img,cam_client,dsize=(432, 368))


s.close()
ss.close()
sss.close()
ssss.close()