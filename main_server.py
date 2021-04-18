import socket
import cv2
import numpy as np
import time

messages={'roger':'a', 'pass':'b','chatbot':'c'}

def recv_check(sock):
    while True:
        msg=sock.recv(1).decode()
        if msg==messages['roger']:
            break

def a2b(a,b):
    msg=a.recv(1)
    if msg.decode()==messages['chatbot']:
        b.send(msg)
    else:
        b.send(messages['pass'].encode())

def send_image(img,sock,dsize):
    img=cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)

    # send image to client
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode(".jpg", img, encode_param)
    data = np.array(imgencode)
    stringData = data.tobytes()

    # String 형태로 변환한 이미지를 socket을 통해서 전송
    data_len = len(stringData)

    str_data_len = str(data_len).encode().ljust(16)
    sock.send(str_data_len)
    sock.send(stringData)
    recv_check(sock)


cam=cv2.VideoCapture(1)
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

    send_image(img,img_client,dsize=(432, 368))

    a2b(pose_client,chatbot_client)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
s.close()
ss.close()
sss.close()