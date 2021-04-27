import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Input
from tensorflow.keras import Sequential

from tensorflow.keras.optimizers import Adam

def import_PoseClassifier(output_shape):
    with tf.device("gpu:0"):
        model = Sequential(
            [
                # Flatten(input_shape=(18, 2, 1)),
                Dense(36, activation="relu",input_shape=(36,)),
                Dropout(0.2),
                Dense(64, activation="relu"),
                Dropout(0.2),
                Dense(32, activation="relu"),
                Dense(output_shape, activation="softmax"),
            ]
        )
    return model

def import_FacER():
    with tf.device("gpu:0"):
        base_model = tf.keras.applications.MobileNetV2(input_shape=(96,96,3),include_top=False)

        global_average_layer = tf.keras.layers.GlobalAveragePooling2D()

        prediction_layer = tf.keras.layers.Dense(3, activation='softmax')

        model = tf.keras.Sequential([
        base_model,
        global_average_layer,
        prediction_layer
        ])
        

    return model


# def import_FacER():
#     with tf.device("gpu:0"):
#         model = Sequential([
#         Input((48,48,1)),
#         Conv2D(32, kernel_size=(3, 3), padding='same', activation='relu'), #, input_shape=(300,300,3)
#         MaxPooling2D(pool_size=(2, 2)),
#         Conv2D(48, kernel_size=(3, 3), padding='same', activation='relu'),
#         MaxPooling2D(pool_size=(2, 2)),
#         Dropout(0.25),

#         Conv2D(64, kernel_size=(3, 3), padding='same', activation='relu'),
#         MaxPooling2D(pool_size=(2, 2)),

#         Conv2D(128, kernel_size=(3, 3), padding='same', activation='relu'),
#         MaxPooling2D(pool_size=(2, 2)),
#         Dropout(0.25),

#         Flatten(),
#         Dense(128, activation='relu'),
#         Dropout(0.5),
#         Dense(3, activation='softmax')
#         ])
        

#     return model
