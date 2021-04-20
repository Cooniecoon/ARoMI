import numpy as np

from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.layers import Input, Activation, Dense, Dropout, Add, Flatten
from tensorflow.keras import Sequential
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping

from model import import_PoseClassifier

class_id = {"sitting": 0, "standing": 1, "etc": 2}
dataset_path = "C:\\Users\\jeongseokoon\\projects\\ARoMI\\models\\classifier\\pose_data\\train_dataset.npy"
output_shape = len(class_id)

dataset = np.load(dataset_path)

# y_data=np.reshape(dataset[:,-1],(dataset[:,-1].shape[0],1))
cls_vector=dataset[:,-1]
y_data=np.zeros((len(cls_vector),len(class_id)))
x_data=dataset[:,:-1]

for i,class_num in enumerate(cls_vector):
    y_data[i][int(class_num)]=1



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

save_path = "C:\\Users\\jeongseokoon\\projects\\ARoMI\\models\\classifier\\model\\pose_classification.weight"
model.save_weights(save_path)