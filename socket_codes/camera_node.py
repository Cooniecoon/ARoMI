import socket
import cv2
import numpy as np
import time
from socket_funcs import *

def cali(source):

    rms = 0.438197
    fx = 458.049323
    fy = 458.049323
    cx = 320.000000
    cy = 240.000000
    k1 = -0.392772
    k2 = 0.165115
    p1 = 0.000704
    p2 = 0.000992

    hfov = 69.9
    vfov = 55.3

    # A (Intrinsic Parameters) [fc, skew*fx, cx], [0, fy, cy], [0, 0, 1]
    K = np.array([[fx, 0., cx],
                [0,  fy, cy],
                [0,   0,  1]])

    # Distortion Coefficients(kc) - 1st, 2nd
    d = np.array([k1, k2, p1, p2, 0]) # just use first two terms

    image = source
    img = cv2.resize(image, (640, 480), interpolation=cv2.INTER_LINEAR)
    h, w = img.shape[:2]

    # undistort
    newcamera, roi = cv2.getOptimalNewCameraMatrix(K, d, (w,h), 0)
    newimg = cv2.undistort(img, K, d, None, newcamera)
    img = cv2.resize(newimg, (640, 480), interpolation=cv2.INTER_LINEAR)

    return img

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
    t=time.time()
    _,img=cam.read()
    img=cali(img)

    send_image_to(img,sock_cam,dsize=(432, 368))
    # img_body=recv_img_from(sock_cam)
    # cv2.imshow("camera node pose result", img_body)

    # cv2.imshow('cam',img)

    dt=time.time()-t
    print(f'fps : {1/dt:.2f}')
    if cv2.waitKey(1)==27:
        break