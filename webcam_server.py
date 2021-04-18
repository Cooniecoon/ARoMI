import socket
import cv2
import numpy as np
import time


def recvall(sock, count):
    buf = b""
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)

    return buf

def recv_check():
    while True:
        msg=conn.recv(5).decode()
        print(msg)
        if msg=='roger':
            break

cam=cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)
_,img=cam.read()

# 수신에 사용될 내 ip와 내 port번호
TCP_IP = "127.0.0.1"
TCP_PORT = 4242

# TCP소켓 열고 수신 대기
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
conn, addr = s.accept()
print("connected")

while True:

    _,img=cam.read()
    img=cv2.resize(img, dsize=(432, 368), interpolation=cv2.INTER_AREA)
    # send image to client
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode(".jpg", img, encode_param)
    data = np.array(imgencode)
    stringData = data.tobytes()

    # String 형태로 변환한 이미지를 socket을 통해서 전송
    data_len = len(stringData)

    str_data_len = str(data_len).encode().ljust(16)

    conn.send(str_data_len)
    conn.send(stringData)
    recv_check()
    
    # cv2.imshow("SERVER", im0)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
s.close()