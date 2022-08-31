# This file handles the neural network of PilotNet
# One key difference from the original paper is that we have 3 output neurons (throttle, brake & steering)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class PilotNet():
    def __init__(self, height, width):
        self.image_height = height
        self.image_width = width
        self.model = self.build_model()
    
    def build_model(self):
        inputs = keras.Input(name='input_shape', shape=(self.image_height, self.image_width, 3))
        
        # convolutional feature maps
        x = layers.Conv2D(filters=24, kernel_size=(5,5), strides=(2,2), activation='relu')(inputs)
        x = layers.Conv2D(filters=36, kernel_size=(5,5), strides=(2,2), activation='relu')(x)
        x = layers.Conv2D(filters=48, kernel_size=(5,5), strides=(2,2), activation='relu')(x)
        x = layers.Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), activation='relu')(x)
        x = layers.Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), activation='relu')(x)

        # flatten layer
        x = layers.Flatten()(x)

        # fully connected layers with dropouts for overfit protection
        x = layers.Dense(units=1152, activation='relu')(x)
        x = layers.Dropout(rate=0.1)(x)
        x = layers.Dense(units=100, activation='relu')(x)
        x = layers.Dropout(rate=0.1)(x)
        x = layers.Dense(units=50, activation='relu')(x)
        x = layers.Dropout(rate=0.1)(x)
        x = layers.Dense(units=10, activation='relu')(x)
        x = layers.Dropout(rate=0.1)(x)

        # derive steering angle value from single output layer by point multiplication
        steering_angle = layers.Dense(units=1, activation='linear')(x)
        steering_angle = layers.Lambda(lambda X: tf.multiply(tf.atan(X), 2), name='steering_angle')(steering_angle)

        # derive throttle pressure value from single output layer by point multiplication
        throttle_press = layers.Dense(units=1, activation='linear')(x)
        throttle_press = layers.Lambda(lambda X: tf.multiply(tf.atan(X), 2), name='throttle_press')(throttle_press)

        # derive brake pressure value from single output by point multiplication
        brake_pressure = layers.Dense(units=1, activation='linear')(x)
        brake_pressure = layers.Lambda(lambda X: tf.multiply(tf.atan(X), 2), name='brake_pressure')(brake_pressure)

        # build and compile model
        model = keras.Model(inputs = [inputs], outputs = [steering_angle, throttle_press, brake_pressure])
        model.compile(
            optimizer = keras.optimizers.Adam(lr = 1e-4),
            loss = {'steering_angle': 'mse', 'throttle_press': 'mse', 'brake_pressure': 'mse'}
        )
        model.summary()
        return model

    def train(self, data):
        pass
    
    def predict(self, data):
        pass