import tensorflow as tf
#import tensorflowjs as tfjs
import os, sys
import cv2
from matplotlib import pyplot as plt
import torch
import importlib.util
#from tensorflow.python.client import device_lib

# try this at home
#gpus = tf.config.experimental.list_physical_devices('GPU')
#print(gpus)

#print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

data_dir='data'
print(os.listdir(data_dir))

print(os.listdir(os.path.join(data_dir,'Ads')))

imgTest= cv2.imread(os.path.join('data','Ads','iframe_3_AD.jpg'))

print(type(imgTest))
print(imgTest.shape)

plt.imshow(imgTest)

plt.imshow(cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB))
#plt.show()

# loading the data

data=tf.keras.utils.image_dataset_from_directory('data', batch_size=32)