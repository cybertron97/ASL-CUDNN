# -*- coding: utf-8 -*-
"""FinalProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hj4yy_M43OaFvgQVLw7W9Bh2tDBq2x5v

Code for cuda CNN


Mounts the Google Drive
"""

from google.colab import drive
drive.mount('/content/drive')

"""Import statements"""

# Commented out IPython magic to ensure Python compatibility.

import numpy as np 
# %tensorflow_version 1.x
import tensorflow as tf
import matplotlib.pyplot as plt
# %matplotlib inline
import os
import cv2
import keras
import torch as th
import torchvision
import torchvision.transforms as transforms
th.manual_seed(42)
import time 
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Conv2D, Dense, Dropout, Flatten
from keras.layers import Flatten, Dense
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from keras import regularizers
tf.set_random_seed(2)
print(tf.__version__)
np.random.seed(5)
tf.set_random_seed(2)
start_time = time.time()

"""Turning on Cuda and making CudNN as our backend library"""

if th.cuda.is_available():
  # Make CuDNN Determinist
  th.backends.cudnn.deterministic = True
  th.cuda.manual_seed(42)
  print("GPU is available and turned on")
device = th.device("cuda" if th.cuda.is_available() else "cpu")

"""Setting the Two Directories"""

train_set = "/content/drive/MyDrive/asl_alphabet_train"
eval_set = "/content/drive/MyDrive/asl-alphabet-test"

"""Loading the data """

def load_data():
  images= []
  labels = []
  size = 64,64
  print ("Loading ", end = "")
  for folder_index, folder in enumerate(os.listdir(train_set)):
    print(folder,end='|')
    for image in os.listdir(train_set + "/"+folder):
      temp_img = cv2.imread(train_set + '/' + folder + '/' + image)
      temp_img = cv2.resize(temp_img, size)
      images.append(temp_img)
      labels.append(folder_index)
  images= np.array(images)
  images = images.astype('float32')/255.0  #normalize the RGB values
  labels = keras.utils.to_categorical(labels) # one hot encoding
  X_train, X_test, Y_train, Y_test = train_test_split(images, labels, test_size = 0.1)
  # print()
  # print(len(labels))
  # print(len(images))
  # print(len(X_train))
  # print(len(X_test))
  # print(len(Y_train))
  # print(len(Y_test))
  return X_train, X_test, Y_train, Y_test, labels

"""Setting our data for training and testing"""

x_train, x_test, y_train, y_test, Labels = load_data()



"""Print function for our images

"""

def print_images(image_list):
    n = len(image_list)
    cols = 8
    rows = 4
    fig = plt.figure(figsize = (24, 12))
    
    for i in range(29):
      ax = plt.subplot(rows,cols, i+1)
      plt.imshow(image_list[i])
      # plt.title(Labels[i])
      ax.title.set_fontsize(20)
      ax.axis('off')
    plt.show()

"""Training model"""

model = Sequential()
model.add(Conv2D(filters=5, kernel_size=5, padding='same', activation='relu', input_shape=(64, 64, 3)))
model.add(MaxPooling2D((4,4)))
model.add(Conv2D(filters=15, kernel_size=(5,5), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(4,4)))
model.add(Flatten())
model.add(Dense(29, activation='softmax'))
model.summary()

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

hist = model.fit(x_train, y_train, validation_split=0.2, epochs=10, batch_size=32)

hist = model.history
epochs = range(1, len(hist.history['loss']) + 1)
plt.plot(epochs, hist.history['loss'], 'bo-')
plt.plot(epochs, hist.history['val_loss'], 'ro--')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show()

score = model.evaluate(x=x_test, y=y_test,verbose=0)
print('Test accuracy:', score[1])

Total_time = time.time()-start_time
print("Total _runtime", Total_time)

print_images(x_train)

"""If you want to test the code with you image and see the result you have to pick the address and put it instead if the address we have in eval_set.
But please put it in a folder which is showing its right class.This will not effect the predicting but after predicting you can see whether it is working right or not. 
"""

def load_testdata():
  images= []
  labels = []
  size = 64,64
  print ("Loading ", end = "")
  for folder_index, folder in enumerate(os.listdir(eval_set)):
    print(folder,end='|')
    for image in os.listdir(eval_set + "/"+folder):
      temp_img = cv2.imread(eval_set + '/' + folder + '/' + image)
      temp_img = cv2.resize(temp_img, size)
      images.append(temp_img)
      labels.append(folder_index)
  images= np.array(images)
  images = images.astype('float32')/255.0  #normalize the RGB values
  labels = keras.utils.to_categorical(labels) # one hot encoding
  return images,labels

"""Here we load the pictures for your test."""

images,labels=load_testdata()

predicted_classes = model.predict_classes(images)
print("The number of the class in which the pictuter belong is")
print(predicted_classes)