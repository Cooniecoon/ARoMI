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

cam=cv2.VideoCapture(0)
# cam.set(3,640)
# cam.set(4,480)
_,img=cam.read()


# chatbot
TCP_IP = "127.0.0.1"
TCP_PORT_chatbot = 2424
sss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sss.bind((TCP_IP, TCP_PORT_chatbot))
sss.listen(True)
chatbot_client, addr = sss.accept()
print("chatbot connected")

# pose
TCP_IP = "127.0.0.1"
TCP_PORT_pose = 4242
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_pose))
s.listen(True)
pose_client, addr = s.accept()
print("pose_classifier connected")

# image
TCP_IP = "127.0.0.1"
TCP_PORT_img = 6666
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind((TCP_IP, TCP_PORT_img))
ss.listen(True)
img_client, addr = ss.accept()
print("image connected")


while True:
    _,img=cam.read()

    send_image_to(img,img_client,dsize=(432, 368))

    a2b(pose_client,chatbot_client)

    if cv2.waitKey(1) == 27:
        break

s.close()
ss.close()
sss.close()
cv2.destroyAllWindows()
cam.release()