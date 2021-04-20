import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

import tensorflow as tf
from model import import_PoseClassifier

class_id = {"sitting": 0, "standing": 1, "etc": 2}
save_path = f"C:\\Users\\jeongseokoon\\projects\\ARoMI\\models\\classifier\\model\\pose_classification_{len(class_id)}_cls.weight"
dataset_path = "C:\\Users\\jeongseokoon\\projects\\ARoMI\\models\\classifier\\pose_data\\"
output_shape = len(class_id)


x_data = np.load(dataset_path + "testdata\\test_data.npy")


model = import_PoseClassifier(output_shape=output_shape)
model.load_weights(save_path)

for idx in range(x_data.shape[0]):
    preds = model.predict(np.reshape(x_data[idx],(1,36))) #! pose classification
    score = tf.nn.softmax(preds[0])
    print(list(class_id.keys())[np.argmax(score)])