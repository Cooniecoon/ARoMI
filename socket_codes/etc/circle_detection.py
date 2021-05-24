import face_recognition
import cv2
import numpy as np
import socket
video_capture = cv2.VideoCapture(0)

# TCP_PORT = 7777
# TCP_IP='127.0.0.1'

# sssss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sssss.bind((TCP_IP, TCP_PORT))
# sssss.listen(True)
# neck_client, addr = sssss.accept()
print('listening')
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()


    dst = frame.copy()
    # r_plane = dst[:, :, 2]
    # cv2.imshow('redo', r_plane)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 120, param1 = 250, param2 = 100, minRadius = 80, maxRadius = 120)
    print(circles)
    if len(circles)>0:
        for i in circles[0][0]:
            print(i)
            cv2.circle(dst, (i[0], i[1]), i[2], (255, 255, 255), 5)



    # h,w=frame.shape[0],frame.shape[1]
    # y,x=((top+bottom)/2)/h,((left+right)/2)/w
    # # print(round(x,2),round(y,2))
    # x_str, y_str = "{0:0<4}".format(round(x,2)),"{0:0<4}".format(round(y,2))
    # msg=x_str+','+y_str
    # neck_client.send(msg.encode())
    # print(msg, len(msg))


        

    # Display the resulting image
    cv2.imshow('Video', dst)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # neck_client.close()
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()