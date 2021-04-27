import socket
import cv2
import numpy as np
import time
from socket_funcs import *

with open('message_code.json', 'r') as f:
    messages = json.load(f)

cam=cv2.VideoCapture(0)
# cam.set(3,640)
# cam.set(4,480)
_,img=cam.read()

# 수신에 사용될 내 ip와 내 port번호
TCP_IP = "192.168.35.192"
TCP_PORT = 1997

# TCP소켓 열고 수신 대기
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
aws_client, addr = s.accept()
print("connected")

while True:
    start = time.time()
    _,img=cam.read()

    send_image_to(img,aws_client,dsize=(432, 368))
    cv2.imshow("Original", img)

    img_recv=recv_img_from(aws_client)
    dt = time.time() - start
    cv2.putText(img_recv, text="fps : {:.2f}".format(1 / dt), org=(30, 30), 
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7, 
                        color=(255, 255, 0), thickness=2)

    cv2.imshow("Received from client", img_recv)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
s.close()