import os
import h5py
import numpy as np

from keras.models import Model
from keras.layers import Input, Dense, Dropout

from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

from training.utils.sequential_data import build_sequential_data_from_frames

training_sets = os.listdir('pong_data/training_data')


training_data = np.zeros((1, 140801))
for file_number, file_id in enumerate(training_sets[-1:]):
    current_file = h5py.File('pong_data/training_data/'+file_id, 'r')
    current_data = current_file['train_'+file_id][:]
    training_data = np.concatenate([training_data, current_data])

del current_file

training_data = training_data[1:, :]


x_center = training_data[:, :-1] - training_data[:, :-1].mean()
y_center = training_data[:, -1] - training_data[:, -1].mean()

y_mean = training_data[:, -1].mean()
x_mean = training_data[:, :-1].mean()

del training_data


joblib.dump(x_mean, 'x_mean.pkl')
joblib.dump(y_mean, 'ymean.pkl')


sequential_data = build_sequential_data_from_frames(x_center, y_center, 2)

del x_center, y_center

x_sequential = sequential_data[:, :-1]
y_sequential = sequential_data[:, -1]

del sequential_data

X_train, X_test, y_train, y_test = train_test_split(x_sequential, y_sequential)

del x_sequential, y_sequential


batch_size = 32
num_epochs = 2
drop_prob_1 = 0.5
drop_prob_2 = 0.5 
hidden_size_1 = X_train.shape[1] / 2
hidden_size_2 = hidden_size_1 / 2


input_placeholder = Input(shape=(X_train.shape[1],))
hidden1 = Dense(hidden_size_1, activation='relu')(input_placeholder)
drop_out1 = Dropout(drop_prob_1)(hidden1)
hidden2 = Dense(hidden_size_2, activation='relu')(drop_out1)
drop_out2 = Dropout(drop_prob_2)(hidden2)
output = Dense(1)(drop_out2)

model = Model(inputs=input_placeholder, outputs=output)

model.compile(loss='mean_squared_error', 
              optimizer='adam', 
              metrics=['mae'])


model.fit(X_train, y_train,             
          batch_size=batch_size, epochs=num_epochs,
          verbose=1, validation_split=0.1)


model.evaluate(X_test, y_test, verbose=1)

model.save('pong_2_layers_mlp.h5')

