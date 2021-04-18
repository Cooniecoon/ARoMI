import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.layers import Input, Activation, Dense, Dropout, Add, Flatten
from tensorflow.keras import Sequential
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import ReduceLROnPlateau

class_id = {"sitting": 0, "standing": 1}

x_train_standing = np.load(
    "C:\\Users\\jeongseokoon\\capstone\\tf-pose-estimation\\pose_data\\standing\\x_train_standing.npy"
)
x_train_sitting = np.load(
    "C:\\Users\\jeongseokoon\\capstone\\tf-pose-estimation\\pose_data\\sitting\\x_train_sitting.npy"
)


y_train_standing = np.array(
    [class_id["standing"] for i in range(x_train_standing.shape[0])]
)
y_train_sitting = np.array(
    [class_id["sitting"] for i in range(x_train_sitting.shape[0])]
)

print(x_train_standing.shape, y_train_standing.shape)
print(x_train_sitting.shape, y_train_sitting.shape)

x_data = np.concatenate((x_train_standing, x_train_sitting), axis=0)
# x_data = np.reshape(x_data, (x_data.shape[0], x_data.shape[1], x_data.shape[2]))
y_data = np.concatenate((y_train_standing, y_train_sitting), axis=0)
y_data = np.reshape(y_data, (y_data.shape[0], 1))
print(x_data.shape, y_data.shape)

x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2)


with tf.device("gpu:0"):
    model = Sequential(
        [
            Input(
                shape=(
                    18,
                    2,
                )
            ),
            Flatten(),
            Dense(36, activation="relu"),
            Dense(64, activation="relu"),
            Dense(32, activation="relu"),
            Dense(1, activation="sigmoid"),
        ]
    )


print(model.summary())

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
        )
    ],
)

save_path = "C:\\Users\\jeongseokoon\\capstone\\tf-pose-estimation\\classifier\\pose_classification.weight"
model.save_weights(save_path)

for idx in range(x_val.shape[0]):
    preds = model.predict(
        x_val[idx].reshape(1, x_val[idx].shape[0], x_val[idx].shape[1])
    )
    if preds > 0.7:
        result = 1
    else:
        result = 0
    print(preds, result, y_val[idx])
