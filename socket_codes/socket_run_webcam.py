import cv2
import numpy as np
import socket
import json
from time import time
import tensorflow as tf
from socket_funcs import *

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from tf_pose.common import CocoPart

from models.classifier.model import import_PoseClassifier,import_FacER

with open('message_code.json', 'r') as f:
    messages = json.load(f)

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
    x_data = np.zeros((36), dtype=np.float16)
    for i in range(CocoPart.Background.value * 2):
        if i//2 in human.body_parts.keys():
            body_part = human.body_parts[i//2]
            if i%2==0:
                x_data[i]=body_part.x
            elif i%2==1:
                x_data[i]=body_part.y
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

if __name__ == "__main__":
    # camera
    

    w, h = model_wh("432x368") # default=0x0, Recommends : 432x368 or 656x368 or 1312x736 "
    e = TfPoseEstimator(
        get_graph_path("mobilenet_v2_large"), # "mobilenet_thin", "mobilenet_v2_large", "mobilenet_v2_small"
        target_size=(w, h),
        trt_bool=False,
    )

    time_0=time()

    print('model loaded')
    TCP_IP = "ec2-3-36-119-109.ap-northeast-2.compute.amazonaws.com"
    TCP_PORT_img = 5555
    ssss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssss.bind((TCP_IP, TCP_PORT_img))
    ssss.listen(True)
    cam_client, addr = ssss.accept()
    print("camera connected")
    print('\n\nstart\n\n')
    while True:
        print('receive image')
        image = recv_img_from(cam_client)
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

        image_all = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)


        # cv2.imshow("tf-pose-estimation result All", image_all)

        # if cv2.waitKey(1) == 27:
        #     break

    cv2.destroyAllWindows()