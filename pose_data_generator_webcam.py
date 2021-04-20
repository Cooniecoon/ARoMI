import cv2
import numpy as np

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from tf_pose.common import CocoPart

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



cam = cv2.VideoCapture(0)
ret_val, image = cam.read()

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

class_id = {"sitting": 0, "standing": 1, "etc": 2}

dataset_path = "C:\\Users\\jeongseokoon\\projects\\ARoMI\\models\\classifier\\pose_data\\"

pose_class = "etc"

pose_id = 1

if __name__ == "__main__":
    w, h = model_wh("432x368") # default=0x0, Recommends : 432x368 or 656x368 or 1312x736 "
    
    e = TfPoseEstimator(
        get_graph_path("mobilenet_v2_large"), # "mobilenet_thin", "mobilenet_v2_large", "mobilenet_v2_small"
        target_size=(w, h),
        trt_bool=False,
    )

    count = 0
    dataset = []

    while True:
        ret_val, image = cam.read()
        image = cv2.resize(image, (432,368), interpolation=cv2.INTER_AREA)
        humans = e.inference(
            image,
            resize_to_default=(w > 0 and h > 0),
            upsample_size=4.0,
        )

        key_input=cv2.waitKey(42)

        if (len(humans) > 0) and (key_input==ord(' ')):

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
            # x_data=np.append(x_data,class_id[pose_class])
            print(x_data)
            dataset.append(x_data)
            count += 1
            print('saved : ', count)

        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        cv2.imshow("tf-pose-estimation result", image)

    
        if cv2.waitKey(10) == 27:
            dataset = np.array(dataset)
            # dataset = np.reshape(
            #     dataset, (1,dataset.shape[0], dataset.shape[1])
            # )
            print(f"dataset_{pose_class} : ", dataset.shape)
            # for save train dataset
            # np.save(
            #     dataset_path + pose_class + f"\\x_train_{pose_class}.npy",
            #     np.array(dataset),
            # )
            # for save test dataset
            np.save(
                dataset_path + f"\\testdata\\test_data.npy",
                np.array(dataset),
            )
            # y_dataset = np.full((dataset.shape[0],), pose_id)
            # print(y_dataset, y_dataset.shape)
            # np.save(
            #     dataset_path + pose_class + f"\\y_train_{pose_class}.npy",
            #     y_dataset,
            # )
            break

    cv2.destroyAllWindows()
    cam.release()