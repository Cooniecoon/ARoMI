import numpy as np

from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.layers import Input, Activation, Dense, Dropout, Add, Flatten
from tensorflow.keras import Sequential
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping

from model import import_PoseClassifier

class_id = {"sitting": 0, "standing": 1, "etc": 2}
dataset_path = "C:\\Users\\jeongseokoon\\projects\\ARoMI\\models\\classifier\\pose_data\\"
output_shape = len(class_id)

x_data_list = []
y_data = []
for cls_, id_ in class_id.items():
    x_train = np.load(dataset_path + cls_ + f"\\x_train_{cls_}.npy")
    # print(x_train.shape)
    x_data_list.append(x_train)
    one_hot_yvec = np.zeros((len(class_id),))
    one_hot_yvec[id_] = id_

    for i in range(x_train.shape[0]):
        y_data.append(one_hot_yvec)

x_data = x_data_list[0]
# print(x_data.shape)

for i in x_data_list[1:]:
    # print("__", i.shape)
    x_data = np.concatenate((x_data, i), axis=0)


print("Y_SHAPE: ", np.array(y_data, dtype=int).shape)
print("X_SHAPE: ", x_data.shape)

x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2)
x_train, x_val, y_train, y_val = (
    np.array(x_train),
    np.array(x_val),
    np.array(y_train),
    np.array(y_val),
)
print(y_val)
print("Y_train: ", y_train.shape)
print("X_train: ", x_train.shape)
print("Y_tset: ", y_val.shape)
print("X_test: ", x_val.shape)

model = import_PoseClassifier(output_shape=3)

print(model.summary())

early_stop = EarlyStopping(monitor="val_loss", patience=5)
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["acc", "mse"])


history = model.fit(
    x_train,
    y_train,
    validation_data=(x_val, y_val),
    epochs=100,
    batch_size=16,
    callbacks=[
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=10,
            verbose=1,
            mode="auto",
            min_lr=1e-05,
        ),
        # early_stop,
    ],
)

save_path = f"C:\\Users\\jeongseokoon\\projects\\ARoMI\\models\\classifier\\model\\pose_classification_{len(class_id)}_cls.weight"
model.save_weights(save_path)
