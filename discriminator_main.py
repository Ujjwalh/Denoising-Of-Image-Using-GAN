# -*- coding: utf-8 -*-
"""Discriminator main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p3RSIqR9E1eqCMrnfBgQi8cR3unPtlaJ
"""

import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.layers import Input, Conv2D, LeakyReLU, BatchNormalization, Flatten, Dense
from keras.models import Model
from keras.optimizers import Adam

def load_images(directory, label, size=(256, 256)):
    # Load images from the given directory into a list
    images = []
    for filename in os.listdir(directory):
        # Load image
        image = load_img(os.path.join(directory, filename), target_size=size)
        # Convert image to array
        image = img_to_array(image)
        # If image has only one channel, repeat the channel to create a grayscale image with 3 channels
        if image.shape[-1] == 1:
            image = np.repeat(image, 3, axis=-1)
        # Append to list of images
        images.append(image)
    # Convert list of images to a numpy array
    images = np.array(images)
    # Scale pixel values from [0, 255] to [-1, 1]
    images = (images - 127.5) / 127.5
    # Create labels for the images
    labels = np.full((len(images), 1), label)
    return images, labels

def create_discriminator_model(input_shape):
    input_layer = Input(shape=input_shape)

    # Convolutional layers
    conv_layer1 = Conv2D(64, kernel_size=3, strides=2, padding='same')(input_layer)
    conv_layer1 = LeakyReLU(alpha=0.2)(conv_layer1)

    conv_layer2 = Conv2D(128, kernel_size=3, strides=2, padding='same')(conv_layer1)
    conv_layer2 = BatchNormalization()(conv_layer2)
    conv_layer2 = LeakyReLU(alpha=0.2)(conv_layer2)

    conv_layer3 = Conv2D(256, kernel_size=3, strides=2, padding='same')(conv_layer2)
    conv_layer3 = BatchNormalization()(conv_layer3)
    conv_layer3 = LeakyReLU(alpha=0.2)(conv_layer3)

    conv_layer4 = Conv2D(512, kernel_size=3, strides=2, padding='same')(conv_layer3)
    conv_layer4 = BatchNormalization()(conv_layer4)
    conv_layer4 = LeakyReLU(alpha=0.2)(conv_layer4)

    conv_layer5 = Conv2D(512, kernel_size=3, strides=2, padding='same')(conv_layer4)
    conv_layer5 = BatchNormalization()(conv_layer5)
    conv_layer5 = LeakyReLU(alpha=0.2)(conv_layer5)

    conv_layer6 = Conv2D(512, kernel_size=3, strides=2, padding='same')(conv_layer5)
    conv_layer6 = BatchNormalization()(conv_layer6)
    conv_layer6 = LeakyReLU(alpha=0.2)(conv_layer6)

    # Flatten the output from the convolutional layers
    flatten_layer = Flatten()(conv_layer6)

    # Dense layers
    dense_layer1 = Dense(1024)(flatten_layer)
    dense_layer1 = LeakyReLU(alpha=0.2)(dense_layer1)

    dense_layer2 = Dense(512)(dense_layer1)
    dense_layer2 = LeakyReLU(alpha=0.2)(dense_layer2)

    dense_layer3 = Dense(256)(dense_layer2)
    dense_layer3 = LeakyReLU(alpha=0.2)(dense_layer3)

    # Output layer
    output_layer = Dense(1, activation='sigmoid')(dense_layer3)

    model = Model(inputs=[input_layer], outputs=[output_layer], name='discriminator')
    model.compile(loss='binary_crossentropy',
                  optimizer=Adam(lr=0.0002, beta_1=0.5),
                  metrics=['accuracy'])

    return model



# Load denoised images and their labels
denoised_images, denoised_labels = load_images('/content/data/denoised_images3', label=0)

# Load real images and their labels
real_images, real_labels = load_images('/content/data/train gnd', label=1)

# Concatenate the images and labels
images = np.concatenate((denoised_images, real_images))
labels = np.concatenate((denoised_labels, real_labels))

# Shuffle the images and labels
shuffle_indices = np.random.permutation(len(images))
images = images[shuffle_indices]
labels = labels[shuffle_indices]

# Create the discriminator model
discriminator_model = create_discriminator_model(input_shape=(256, 256, 3))

# Print the summary of the discriminator model
discriminator_model.summary()

# Train the discriminator model
discriminator_model.fit(images, labels, epochs=8, batch_size=32)

# Save the trained model to a file
discriminator_model.save('/content/discriminator_model.h5')