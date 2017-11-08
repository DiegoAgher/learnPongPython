import os
import numpy as np
import h5py
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import Input, Convolution2D, MaxPooling2D, Dense, Dropout,\
    Flatten
from training.utils.sequential_data import build_sequential_data_from_frames

MODELS_PARAMETERS_DIR = 'pong_data/models_parameters/'
x_mean_dir = MODELS_PARAMETERS_DIR + 'x_mean.pkl'
y_mean_dir = MODELS_PARAMETERS_DIR + 'y_mean.pkl'

TRAINING_DATA_DIR = 'pong_data/training_data'
training_sets = os.listdir(TRAINING_DATA_DIR)

for i, file_id in enumerate(training_sets[-3:]):
    current_file = h5py.File(TRAINING_DATA_DIR + '/{}'.format(file_id), 'r')
    dataset_id = 'train_' + file_id.replace('.h5', '')
    if i == 0:
        current_data = current_file[dataset_id][:]
    else:
        training_data = current_data
        current_data = current_file[dataset_id][:]
        training_data = np.concatenate([training_data, current_data])

x = training_data[:, :-1]
y = training_data[:, -1]

frame_length = x.shape[1]

x_mean = x.mean()
y_mean = y.mean()
joblib.dump(x_mean, x_mean_dir)
joblib.dump(y_mean, y_mean_dir)


sequential_data = build_sequential_data_from_frames(x - x_mean, y - y_mean, 3)
x_sequential = sequential_data[:, :-1]
y_sequential = sequential_data[:, -1]
del x, y, training_data, current_data, sequential_data

x_sequential = np.reshape(x_sequential, (x_sequential.shape[0],
                                         frame_length/400, 400, 3))


num_train, height, width, channels = x.shape

X_train, X_test, y_train, y_test = train_test_split(x_sequential, y_sequential)
del x_sequential, y_sequential

batch_size = 32
num_epochs = 2
kernel_size = 3
pool_size = 2
conv_depth_1 = 32
conv_depth_2 = 64
drop_prob_1 = 0.25
drop_prob_2 = 0.5
hidden_size = 512
output_size = 1

input_placeholder = Input(shape=(height, width, channels))
conv_1 = Convolution2D(conv_depth_1, (kernel_size, kernel_size),
                       padding='same', activation='relu')(input_placeholder)

conv_2 = Convolution2D(conv_depth_1, (kernel_size, kernel_size),
                       padding='same', activation='relu')(conv_1)

pool_1 = MaxPooling2D(pool_size=(pool_size, pool_size))(conv_2)
drop_1 = Dropout(drop_prob_1)(pool_1)

conv_3 = Convolution2D(conv_depth_2, (kernel_size, kernel_size),
                       padding='same', activation='relu')(drop_1)
conv_4 = Convolution2D(conv_depth_2, (kernel_size, kernel_size),
                       padding='same', activation='relu')(conv_3)
pool_2 = MaxPooling2D(pool_size=(pool_size, pool_size))(conv_4)
drop_2 = Dropout(drop_prob_1)(pool_2)

flat = Flatten()(drop_2)
hidden = Dense(hidden_size, activation='relu')(flat)

output = Dense(output_size)(hidden)

model = Model(inputs=input_placeholder, outputs=output)

model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['mae'])

model.fit(X_train, y_train,
          batch_size=batch_size, epochs=num_epochs,
          verbose=1, validation_split=0.1)

model.evaluate(X_test, y_test, verbose=1)

model.save('pong_conv2d.h5')
