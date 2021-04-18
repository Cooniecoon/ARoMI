import cv2
import numpy as np

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

cam = cv2.VideoCapture(0)
ret_val, image = cam.read()

BODY_PARTS={
    'Nose' : 0,
    'Neck' : 1,
    'RShoulder' : 2,
    'RElbow' : 3,
    'RWrist' : 4,
    'LShoulder' : 5,
    'LElbow' : 6,
    'LWrist' : 7,
    'RHip' : 8,
    'RKnee' : 9,
    'RAnkle' : 10,
    'LHip' : 11,
    'LKnee' : 12,
    'LAnkle' : 13,
    'REye' : 14,
    'LEye' : 15,
    'REar' : 16,
    'LEar' : 17,
    'Background' : 18
}

if __name__ == "__main__":
    w, h = model_wh("432x368") # default=0x0, Recommends : 432x368 or 656x368 or 1312x736 "
    
    e = TfPoseEstimator(
        get_graph_path("mobilenet_thin"), # "mobilenet_thin", "mobilenet_v2_large", "mobilenet_v2_small"
        target_size=(w, h),
        trt_bool=False,
    )
       

    while True:
        ret_val, image = cam.read()

        humans = e.inference(
            image,
            resize_to_default=(w > 0 and h > 0),
            upsample_size=4.0,
        )

        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        
        if len(humans)>0:
            Body_Parts=humans[0].body_parts

            if (BODY_PARTS['Lear'] in Body_Parts.keys()) and (BODY_PARTS['Rear'] in Body_Parts.keys()) and (BODY_PARTS['nose'] in Body_Parts.keys()):
                # print('L : ',Body_Parts[BODY_PARTS['L_ear']],'    :    R : ',Body_Parts[BODY_PARTS['R_ear']])
                print('Eye Contact')
            else : 
                print('Look Elsewhere')W

            cv2.imshow("tf-pose-estimation result", image)
        
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()