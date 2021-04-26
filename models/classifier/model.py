import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
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
        model.load_weights('.\model\MobileNetV2_1.pb')
    return model