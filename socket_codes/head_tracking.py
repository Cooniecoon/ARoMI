



with open('AWS_IP.txt', 'r') as f:
    TCP_IP = f.readline()

TCP_PORT_pose = 5555

# 송신을 위한 socket 준비
sock_neck = socket.socket()
sock_neck.connect((TCP_IP, TCP_PORT_pose))

