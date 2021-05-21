import cv2
import numpy as np
import socket
import json


def get_message_codes():
    with open('message_code.json', 'r') as f:
        messages = json.load(f)
    return messages
messages=get_message_codes()

# socket 수신 버퍼를 읽어서 반환하는 함수
def recvall(sock, count):
    buf = b""
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    msg=messages['roger']
    sock.send(msg.encode())
    return buf

def send_image_to(img,sock,dsize):
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

def recv_img_from(sock):
    newbuf = sock.recv(16)
    length = newbuf.decode()
    img_data = recvall(sock, int(length))
    data = np.frombuffer(img_data, dtype="uint8")
    image = cv2.imdecode(data, 1)
    return image

def send_message_to(msg,sock):
    data_len = len(msg)
    str_data_len = str(data_len).encode().ljust(16)
    sock.send(str_data_len)
    sock.send(msg.encode())
    recv_check(sock)

def recv_msg_from(sock):
    newbuf = sock.recv(16)
    length = newbuf.decode()
    print('length :',length)
    msg_data = recvall(sock, int(length))
    
    return msg_data.decode()

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

