import socket
import cv2
import numpy as np
import time

# socket 수신 버퍼를 읽어서 반환하는 함수
def recvall(sock, count):
    buf = b""
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)

    return buf


# 연결할 서버(수신단)의 ip주소와 port번호
TCP_IP = "192.168.35.139"
TCP_PORT = 6666

# 송신을 위한 socket 준비
sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

while True:
    start = time.time()
    newbuf = sock.recv(16)
    length = newbuf.decode()
    img_data = recvall(sock, int(length))
    data = np.frombuffer(img_data, dtype="uint8")
    image = cv2.imdecode(data, 1)
    cv2.imshow("CLIENT", image)

    dt = time.time() - start
    print("fps : {:.2f}".format(1 / dt))
    if cv2.waitKey(10) == 27:
        break
sock.close()
capture.release()
cv2.destroyAllWindows()
