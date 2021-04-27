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

# 연결할 서버(수신단)의 ip주소와 port번호
TCP_IP = "ec2-13-209-8-64.ap-northeast-2.compute.amazonaws.com"
TCP_PORT = 6666

# 송신을 위한 socket 준비
aws_server = socket.socket()
aws_server.connect((TCP_IP, TCP_PORT))

while True:
    start = time.time()
    _,img=cam.read()

    send_image_to(img,aws_server,dsize=(432, 368))
    cv2.imshow("Original", img)

    img_recv=recv_img_from(aws_server)
    dt = time.time() - start
    cv2.putText(img_recv, text="fps : {:.2f}".format(1 / dt), org=(30, 30), 
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7, 
                        color=(255, 255, 0), thickness=2)

    cv2.imshow("Received from client", img_recv)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
s.close()
