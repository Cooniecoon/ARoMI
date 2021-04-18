import cv2
import numpy as np
import argparse


from tf_pose.common import CocoPart
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


class_id = {"sitting": 0, "standing": 1, "etc": 2}

dataset_path = "C:\\Users\\jeongseokoon\\capstone\\tf-pose-estimation\\pose_data\\"
pose_class = "etc"
pose_id = 2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pose-data-generator")
    parser.add_argument("--dir", type=str, default="")

    parser.add_argument(
        "--resize",
        type=str,
        default="0x0",
        help="if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ",
    )
    parser.add_argument(
        "--resize-out-ratio",
        type=float,
        default=4.0,
        help="if provided, resize heatmaps before they are post-processed. default=1.0",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="mobilenet_thin",
        help="cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small",
    )
    parser.add_argument(
        "--show-process",
        type=bool,
        default=False,
        help="for debug purpose, if enabled, speed for inference is dropped.",
    )

    parser.add_argument(
        "--tensorrt", type=str, default="False", help="for tensorrt process."
    )
    args = parser.parse_args()

    w, h = model_wh(args.resize)

    if w > 0 and h > 0:
        e = TfPoseEstimator(
            get_graph_path(args.model),
            target_size=(w, h),
            trt_bool=str2bool(args.tensorrt),
        )
    else:
        e = TfPoseEstimator(
            get_graph_path(args.model),
            target_size=(432, 368),
            trt_bool=str2bool(args.tensorrt),
        )

    cam = cv2.VideoCapture(args.camera)
    count = 1
    frame_gap = 5
    dataset = []
    while True:
        ret_val, image = cam.read()

        humans = e.inference(
            image,
            resize_to_default=(w > 0 and h > 0),
            upsample_size=args.resize_out_ratio,
        )

        if (len(humans) > 0) and (count % frame_gap == 0):
            x_data = np.empty((18, 2), dtype=np.float16)
            for i in range(CocoPart.Background.value):
                if i not in humans[0].body_parts.keys():
                    x_data[i] = 0.0

                else:
                    body_part = humans[0].body_parts[i]
                    x_data[i] = np.array([body_part.x, body_part.y], dtype=np.float16)
            dataset.append(x_data)

        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        cv2.putText(
            image,
            f"data: {len(dataset)}\nclass: {pose_class}",
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )
        cv2.imshow("tf-pose-estimation result", image)
        count += 1
        if cv2.waitKey(1) == 27:
            dataset = np.array(dataset)
            dataset = np.reshape(
                dataset, (dataset.shape[0], dataset.shape[1], dataset.shape[2], 1)
            )
            print(f"dataset_{pose_class} : ", dataset.shape)
            np.save(
                dataset_path + pose_class + f"\\x_train_{pose_class}.npy",
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