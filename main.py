# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RIzkAgiarwio6s1a0weAFskHfKbDyNd7
"""

import os
from tensorflow.keras.preprocessing.image import load_img
import numpy as np

# Define the image folder path
image_folder = '/content/data/train data'

# Define the desired image size
image_size = (256, 256)

# Define an empty list to store the images
images = []

# Loop through the image folder and load the images
for filename in os.listdir(image_folder):
    # Check if the file is a valid image file
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        try:
            # Load the image using Keras' load_img function
            img = load_img(os.path.join(image_folder, filename), color_mode='rgb', target_size=image_size)

            # Convert the image to a numpy array and normalize pixel values
            img_array = np.array(img) / 255.0

            # Add the image to the list
            images.append(img_array)
        except:
            # Handle the error if the file is not a valid image file
            print(f"Skipping file {filename} as it is not a valid image file.")

# Convert the list of images to a numpy array
images = np.array(images)

# Print the shape of the image array
print(images.shape)

import os
from PIL import Image
from tensorflow.keras import optimizers

import numpy as np

# Define the image folder path
image_folder = '/content/data/train gnd'

# Define the desired image size
image_size = (256, 256)

# Define an empty list to store the images
images = []

# Loop through the image folder and load the images
for filename in os.listdir(image_folder):
    # Load the image using Pillow
    img = Image.open(os.path.join(image_folder, filename))

    # Resize the image to the desired size
    img = img.resize(image_size)

    # Convert the image to a numpy array and normalize pixel values
    img_array = np.array(img) / 256.0

    # Add the image to the list
    images.append(img_array)

# Convert the list of images to a numpy array
images = np.array(images)

# Print the shape of the image array
print(images.shape)

import tensorflow as tf


# Load the saved denoiser model
denoiser_model = tf.keras.models.load_model('denoiser_model2.h5')

# Define the output folder path
output_folder = '/content/data/denoised_images3'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through the images and save the denoised output
for i in range(len(images)):
    # Get the original image from the list
    original_image = images[i]

    # Reshape the image to match the model input shape
    image = np.reshape(original_image, (1, original_image.shape[0], original_image.shape[1], original_image.shape[2]))

    # Generate the denoised image using the denoiser model
    denoised_image = denoiser_model.predict(image)

    # Rescale the pixel values from [0, 1] to [0, 255]
    denoised_image = denoised_image * 255.0

    # Convert the pixel values to integers
    denoised_image = denoised_image.astype(np.uint8)

    # Convert the denoised image from (1, height, width, channels) to (height, width, channels)
    denoised_image = np.squeeze(denoised_image, axis=0)

    # Create the output file path
    output_filename = os.path.join(output_folder, f'denoised_{i}.png')

    # Save the denoised image
    Image.fromarray(denoised_image).save(output_filename)

    # Print the output file path
    print(f"Denoised image saved to: {output_filename}")