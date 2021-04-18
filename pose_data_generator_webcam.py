import cv2
import numpy as np

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from tf_pose.common import CocoPart
cam = cv2.VideoCapture(1)
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

dataset_path = "C:\\Users\\jeongseokoon\\capstone\\tf-pose-estimation\\pose_data\\"

pose_class = "standing"

pose_id = 1

if __name__ == "__main__":
    w, h = model_wh("432x368") # default=0x0, Recommends : 432x368 or 656x368 or 1312x736 "
    
    e = TfPoseEstimator(
        get_graph_path("mobilenet_thin"), # "mobilenet_thin", "mobilenet_v2_large", "mobilenet_v2_small"
        target_size=(w, h),
        trt_bool=False,
    )

    count = 0
    dataset = []

    while True:
        ret_val, image = cam.read()

        humans = e.inference(
            image,
            resize_to_default=(w > 0 and h > 0),
            upsample_size=4.0,
        )

        key_input=cv2.waitKey(42)

        if (len(humans) > 0) and (key_input==32):
            x_data = np.zeros((18, 2), dtype=np.float16)
            for i in range(CocoPart.Background.value):
                if i in humans[0].body_parts.keys():
                    body_part = humans[0].body_parts[i]
                    x_data[i] = np.array([body_part.x, body_part.y], dtype=np.float16)

            print(x_data.shape)
            dataset.append(x_data)
            count += 1
            print('saved : ', count)

        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        cv2.imshow("tf-pose-estimation result", image)

    
        if cv2.waitKey(10) == 27:
            dataset = np.array(dataset)
            dataset = np.reshape(
                dataset, (dataset.shape[0], dataset.shape[1], dataset.shape[2], 1)
            )
            print(f"dataset_{pose_class} : ", dataset.shape)
            # np.save(
            #     dataset_path + pose_class + f"\\x_train_{pose_class}.npy",
            #     np.array(dataset),
            # )
            # y_dataset = np.full((dataset.shape[0],), pose_id)
            # print(y_dataset, y_dataset.shape)
            # np.save(
            #     dataset_path + pose_class + f"\\y_train_{pose_class}.npy",
            #     y_dataset,
            # )
            break

    cv2.destroyAllWindows()