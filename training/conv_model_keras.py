import numpy as np
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import Input, Convolution2D, MaxPooling2D, Dense, Dropout,\
    Flatten


y_mean = joblib.load('ymean.pkl')
x_mean = joblib.load('x_mean.pkl')
centered_data = joblib.load('centered_data.pkl')

x = centered_data[:, :-1]
y = centered_data[:,-1]


x = np.reshape(x, (x.shape[0], 400, 400, 1))
num_train, height, width, channels = x.shape

X_train, X_test, y_train, y_test = train_test_split(x, y)

batch_size = 32
num_epochs = 3
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
