import socket
import numpy as np
import time
from socket_funcs import *


# 수신에 사용될 내 ip와 내 port번호
TCP_IP = "ec2-13-209-8-64.ap-northeast-2.compute.amazonaws.com"
TCP_PORT = 6666

# TCP소켓 열고 수신 대기
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
cam_client, addr = s.accept()
print("connected")

# # 수신에 사용될 내 ip와 내 port번호
# TCP_IP = "ec2-13-209-8-64.ap-northeast-2.compute.amazonaws.com"
# TCP_PORT = 1997

# # TCP소켓 열고 수신 대기
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((TCP_IP, TCP_PORT))
# s.listen(True)
# fps_plotter, addr = s.accept()
# print("connected")




while True:
    start = time.time()
    
    image = recv_img_from(cam_client)
    
    send_image_to(image,cam_client,dsize=(300, 300))
    dt = time.time() - start
    print("fps : {:.2f}".format(1 / dt))


    # msg="{:.2f}".format(1 / dt)
    # fps_plotter.send(msg.encode())
    # recv_check(fps_plotter)
    
    if cv2.waitKey(10) == 27:
        break
cam_client.close()

