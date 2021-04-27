import socket
import cv2
import numpy as np
import time
from socket_funcs import *




# 연결할 서버(수신단)의 ip주소와 port번호
TCP_IP = "127.0.0.1"
TCP_PORT = 1997

# 송신을 위한 socket 준비
cam_server = socket.socket()
cam_server.connect((TCP_IP, TCP_PORT))

while True:
    start = time.time()
    
    image = recv_img(cam_server)
    
    cv2.imshow("Received from server", image)
    send_image(image,cam_server,dsize=(640, 480))
    dt = time.time() - start
    print("fps : {:.2f}".format(1 / dt))
    if cv2.waitKey(10) == 27:
        break
cam_server.close()

cv2.destroyAllWindows()
