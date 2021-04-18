import cv2
import numpy as np
import socket
from time import time

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from tf_pose.common import CocoPart

from classifier.model import import_classifier

messages={'roger':'r', 'pass':'p','chatbot':'c','break':'b'}

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

def recv_img(sock):
    newbuf = sock.recv(16)
    length = newbuf.decode()
    img_data = recvall(sock, int(length))
    data = np.frombuffer(img_data, dtype="uint8")
    image = cv2.imdecode(data, 1)
    return image

def get_face_crop_img(L_EAR_coordinate,R_EAR_coordinate,x_padding,y_padding,dsize):
    face_box_x=min(L_EAR_coordinate.x, R_EAR_coordinate.x)
    face_box_w=abs(L_EAR_coordinate.x-R_EAR_coordinate.x)
    face_box_y=min(L_EAR_coordinate.y, R_EAR_coordinate.y)
    face_box_h=abs(L_EAR_coordinate.y-R_EAR_coordinate.y)

    x1=int(face_box_x*original_img.shape[1])
    w=int(face_box_w*original_img.shape[1])
    x2=x1+w
    y1=int(face_box_y*original_img.shape[0])

    face_crop=original_img[max(0,y1-int(w)-y_padding):y1+int(w)+y_padding, x1-x_padding:x2+x_padding]
    face_crop_gray=cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
    face_box=cv2.resize(face_crop_gray, dsize, interpolation=cv2.INTER_AREA)
    return face_box

def get_pose_vector(human):
    x_data = np.zeros((18, 2), dtype=np.float16)
    for i in range(CocoPart.Background.value):
        if i in human.body_parts.keys():
            body_part = human.body_parts[i]
            x_data[i] = np.array([body_part.x, body_part.y], dtype=np.float16)
    return x_data

def get_human_box(human):
    xmin=2
    ymin=2
    xmax=0
    ymax=0
    for i in range(CocoPart.Background.value):
        if i in human.body_parts.keys():
            body_part = human.body_parts[i]
            vector = np.array([body_part.x, body_part.y], dtype=np.float16)
            xmin=min(xmin,vector[0])
            ymin=min(ymin,vector[1])
            xmax=max(xmax,vector[0])
            ymax=max(ymax,vector[1])
    return [xmin,ymin,xmax,ymax]

def get_area(xyxy):
    h=xyxy[2]-xyxy[0]
    w=xyxy[3]-xyxy[1]
    return w*h

BODY_PARTS={
    'Nose' : 0,
    'REye' : 14, 'LEye' : 15,
    'REar' : 16, 'LEar' : 17,
    'Neck' : 1,
    'RShoulder' : 2, 'RElbow' : 3, 'RWrist' : 4,
    'LShoulder' : 5, 'LElbow' : 6, 'LWrist' : 7,
    'RHip' : 8, 'RKnee' : 9, 'RAnkle' : 10,
    'LHip' : 11, 'LKnee' : 12, 'LAnkle' : 13,
    'Background' : 18
}
    
classifier_path = "C:\\Users\\jeongseokoon\\capstone\\tf-pose-estimation\\classifier\\model\\pose_classification.weight"

if __name__ == "__main__":

    classifier = import_classifier(output_shape=1)
    classifier.load_weights(classifier_path)
    
    w, h = model_wh("432x368") # default=0x0, Recommends : 432x368 or 656x368 or 1312x736 "
    e = TfPoseEstimator(
        get_graph_path("mobilenet_thin"), # "mobilenet_thin", "mobilenet_v2_large", "mobilenet_v2_small"
        target_size=(w, h),
        trt_bool=False,
    )
       
    # 연결할 서버(수신단)의 ip주소와 port번호 : pose
    TCP_IP = "127.0.0.1"
    TCP_PORT_pose = 4242

    # 송신을 위한 socket 준비
    sock_pose = socket.socket()
    sock_pose.connect((TCP_IP, TCP_PORT_pose))

    # 연결할 서버(수신단)의 ip주소와 port번호 : image
    TCP_IP = "127.0.0.1"
    TCP_PORT_img = 6666

    # 송신을 위한 socket 준비
    sock_img = socket.socket()
    sock_img.connect((TCP_IP, TCP_PORT_img))

    time_0=time()
    THRESHOLD_TIME=3 #seconds
    while True:
        image = recv_img(sock_img)
        original_img = image.copy()

        humans = e.inference(
            image,
            resize_to_default=(w > 0 and h > 0),
            upsample_size=4.0,
        )
        # if human detected
        if len(humans)>0:
            
            # Filtering Only Big Person            
            human_norm=0
            for human in humans:
                human_box=get_human_box(human)
                human_size=get_area(human_box)
                if human_size>human_norm:
                    human_norm=human_size
                    User=human
            Body_Parts=User.body_parts

            x_data = get_pose_vector(User)

            # print(x_data.reshape(1,x_data.shape[0], x_data.shape[1],1))
            preds = classifier.predict(
                        x_data.reshape(1,x_data.shape[0], x_data.shape[1],1)
                    ) #! pose classification

            if preds > 0.9:
                result = 'standing'
            else:
                result = 'sitting'
            # print('pose : ',result)

            L_EAR_CHECK=BODY_PARTS['LEar'] in Body_Parts.keys()
            R_EAR_CHECK=BODY_PARTS['REar'] in Body_Parts.keys()
            NOSE_CHECK=BODY_PARTS['Nose'] in Body_Parts.keys()

            
            if (L_EAR_CHECK and R_EAR_CHECK and NOSE_CHECK):
                dt=time()-time_0
                print('eye_contact_time : {0:.2f}'.format(dt))
                if dt > THRESHOLD_TIME:
                    time_0=time()
                    L_EAR_coordinate=Body_Parts[BODY_PARTS['LEar']]
                    R_EAR_coordinate=Body_Parts[BODY_PARTS['REar']]

                    face_box=get_face_crop_img(
                        L_EAR_coordinate, R_EAR_coordinate,
                        x_padding=15, y_padding=10,
                        dsize=(48,48)
                        )

                    cv2.imshow("_", face_box) #! face_box : input of FER

                    # print('Eye Contact') #! Chatbot Litsening
                    sock_pose.send(messages['chatbot'].encode())
                    # print('chatbot on')
                
            elif ((not L_EAR_CHECK or not R_EAR_CHECK) and NOSE_CHECK):
                # sock_pose.send(messages['pass'].encode())
                # print('Look Elsewhere')
                # print('chatbot off')
                time_0=time()
                pass

            image_single = TfPoseEstimator.draw_humans(image, [User], imgcopy=False)
            cv2.imshow("tf-pose-estimation result Filtered", image_single)

        sock_pose.send(messages['pass'].encode())


        image_all = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        cv2.imshow("tf-pose-estimation result All", image_all)

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()