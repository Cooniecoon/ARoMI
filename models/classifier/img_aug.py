import imgaug as ia
from imgaug import augmenters as iaa
from os import listdir
import shutil as sh
import os
import cv2
import numpy as np


def xywh2xyxy(bbox, Width, Height):
    x_cen = bbox[1]
    y_cen = bbox[2]
    w = bbox[3]
    h = bbox[4]
    x_min = x_cen - w / 2
    y_min = y_cen - h / 2
    x_max = x_cen + w / 2
    y_max = y_cen + h / 2

    xyxy = [
        int(x_min * Width),
        int(y_min * Height),
        int(x_max * Width),
        int(y_max * Height),
    ]
    return xyxy


def xyxy2xywh(x_min, y_min, x_max, y_max):
    x_cen = float((x_min + x_max)) / 2 / Width
    y_cen = float((y_min + y_max)) / 2 / Height
    w = float((x_max - x_min)) / Width
    h = float((y_max - y_min)) / Height
    return x_cen, y_cen, w, h


def read_annotation(txt_file: str):

    bounding_box_list = []

    if "txt" in txt_file.lower():
        with open(txt_file, mode="rt") as txt:
            info = txt.readlines()

    for obj in info:
        bbox = obj.split("\n")
        bbox = bbox[0]
        bbox = bbox.split(" ")

        object_label = int(bbox[0])
        x_cen = float(bbox[1])
        y_cen = float(bbox[2])
        w = float(bbox[3])
        h = float(bbox[4])
        bounding_box = [object_label, x_cen, y_cen, w, h]
        bounding_box_list.append(bounding_box)

    return bounding_box_list


def read_train_dataset(dir):
    images = []
    annotations = []

    for file in listdir(dir):
        if "jpg" in file.lower() or "png" in file.lower():
            images.append(cv2.imread(dir + file, 1))  # 1 : cv2.IMREAD_COLOR
            annotation_file = file.replace(file.split(".")[-1], "txt")
            bounding_box_list = read_annotation(dir + annotation_file)
            annotations.append((bounding_box_list, annotation_file, file))

    images = np.array(images)

    return images, annotations


def augmentation(images, annotations, augmentation, save_dir, filename):
    # print("\n", augmentation, "\n")
    for idx in range(len(images)):
        image = images[idx]
        boxes = annotations[idx][0]

        ia_bounding_boxes = []
        for box in boxes:
            xyxy = xywh2xyxy(box, Width, Height)
            # print(xyxy)
            ia_bounding_boxes.append(
                ia.BoundingBox(
                    x1=xyxy[0], y1=xyxy[1], x2=xyxy[2], y2=xyxy[3], label=box[0]
                )
            )

        bbs = ia.BoundingBoxesOnImage(ia_bounding_boxes, shape=image.shape)

        seq = iaa.Sequential(augmentation)

        seq_det = seq.to_deterministic()

        image_aug = seq_det.augment_images([image])[0]
        bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

        new_image_file = save_dir + filename + annotations[idx][2]
        cv2.imwrite(new_image_file, image_aug)

        h, w = np.shape(image_aug)[0:2]
        # print("h, w : ", h, w)
        # voc_writer = Writer(new_image_file, w, h)
        with open(save_dir + filename + annotations[idx][1], "w") as f:
            for i in range(len(bbs_aug.bounding_boxes)):
                bb_box = bbs_aug.bounding_boxes[i]
                x_min = bb_box.x1
                y_min = bb_box.y1
                x_max = bb_box.x2
                y_max = bb_box.y2
                cls_id = bb_box.label
                x_cen, y_cen, w, h = xyxy2xywh(x_min, y_min, x_max, y_max)
                f.write("%d %.06f %.06f %.06f %.06f\n" % (cls_id, x_cen, y_cen, w, h))


Width = 640
Height = 640

blur = iaa.AverageBlur(k=(2, 11))  #! 2~11 random
emboss = iaa.Emboss(alpha=(1.0, 1.0), strength=(2.0, 2.0))
gray = iaa.RemoveSaturation(from_colorspace=iaa.CSPACE_BGR)
contrast = iaa.AllChannelsCLAHE(clip_limit=(10, 10), per_channel=True)
bright = iaa.MultiplyAndAddToBrightness(mul=(0.5, 1.5), add=(-30, 30))
color = iaa.pillike.EnhanceColor()
sharpen = iaa.Sharpen(alpha=(0.5, 1.0))  #! 0.5 ~ 1.0 random
edge = iaa.pillike.FilterEdgeEnhance()

augmentations = [[bright], [emboss], [color], [edge]]  #! choice augmentation ##
rotates = [[iaa.Affine(rotate=90)], [iaa.Affine(rotate=180)], [iaa.Affine(rotate=270)]]
flip = iaa.Fliplr(1.0)  #! 100% left & right

dir = "C:\\Users\\jeongseokoon\\AI-hub\\data\\original\\"

save_aug_dir = "C:\\Users\\jeongseokoon\\AI-hub\\data\\images\\"  #! Absolute path

print("        .\n        .\n        .\n")

files = os.listdir(dir)


for file in files:
    sh.copy(dir + file, save_aug_dir)

print("Original data Copied to images directory")

images, annotations = read_train_dataset(save_aug_dir)
augmentation(
    images,
    annotations,
    augmentation=flip,
    save_dir=save_aug_dir,
    filename="fliped_",
)
print("        .\n        .\n        .\n")
print("Flip Finish")
print("        .\n        .\n        .\n")
images, annotations = read_train_dataset(save_aug_dir)
i = 1
for rot in rotates:
    augmentation(
        images,
        annotations,
        augmentation=rot,
        save_dir=save_aug_dir,
        filename="rotated_" + str(i) + "_",
    )
    print("rotates  i : ", i)
    i += 1

print("        .\n        .\n        .\n")
images, annotations = read_train_dataset(save_aug_dir)
i = 1
for aug in augmentations:
    augmentation(
        images,
        annotations,
        augmentation=aug,
        save_dir=save_aug_dir,
        filename="augmented_" + str(i) + "_",
    )
    print("augmentations  i : ", i)
    i += 1