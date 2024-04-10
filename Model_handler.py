import keras
import tensorflow as tf
#import tensorflowjs as tfjs
import os, sys
import cv2
from matplotlib import pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
import torch
import importlib.util
from tensorflow.python.client import device_lib

activate_GPU = True
if activate_GPU:
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    # try this at home
    gpus = tf.config.experimental.list_physical_devices('GPU')
    print(gpus)

    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

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

data = tf.keras.utils.image_dataset_from_directory('data', batch_size=32)
print("data", data)

data_iterator = data.as_numpy_iterator()
batch = data_iterator.next()

#print(len(batch))  # batch contain 2 items, the image batch[0] and the label batch[1]
print("batch shape:", batch[0].shape) # images are numpy arrays
print("Batch[1]", batch[1]) #labels

fig, ax = plt.subplots(ncols=10, figsize=(20,20)) # class 0= futurama, class 1 = simpsons
for idx, img in enumerate(batch[0][:4]):
    ax[idx].imshow(img.astype(int))
    ax[idx].title.set_text(batch[1][idx])


# scale data
scaled = data.map(lambda x,y: (x/255, y))
print("scaled data", scaled)

scaled.as_numpy_iterator().next()

# split data

train_size = int(len(scaled)*.7) #batch = 32
val_size = int(len(scaled)*.2)
test_size = int(len(scaled)*.1)

print(f'Train Size: {train_size}, Val Size:{val_size}, Test Size: {test_size}')

train = scaled.take(train_size)
val = scaled.skip(train_size).take(val_size)
test = scaled.skip(train_size+val_size).take(test_size)

print(train.as_numpy_iterator().next()[0])

#### Model
model = Sequential()

model.add(Conv2D(16, (3,3), 1, activation='relu', input_shape=(256,256,3)))
model.add(MaxPooling2D())
model.add(Conv2D(32, (3,3), 1, activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(16, (3,3), 1, activation='relu'))
model.add(MaxPooling2D())
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile('adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])

print("Summary: ",model.summary())



### Training
hist = model.fit(train, epochs=8, validation_data=val)

fig = plt.figure()
plt.plot(hist.history['loss'][1:], color='teal', label='loss')
plt.plot(hist.history['val_loss'][1:], color='orange', label='val_loss')
fig.suptitle('Loss', fontsize=20)
plt.legend(loc="upper left")
plt.show()

fig = plt.figure()
plt.plot(hist.history['accuracy'], color='teal', label='accuracy')
plt.plot(hist.history['val_accuracy'], color='orange', label='val_accuracy')
fig.suptitle('Accuracy', fontsize=20)
plt.legend(loc="upper left")
plt.show()