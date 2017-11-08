import os
import numpy as np
import h5py
from sklearn.externals import joblib
from sklearn.linear_model import ElasticNet, ElasticNetCV
from sklearn.model_selection import train_test_split
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


training_data = training_data[1:, :]
x = training_data[:, :-1]
y = training_data[:, -1]

frame_length = x.shape[1]
x_mean = x.mean()
y_mean = y.mean()

joblib.dump(x_mean, x_mean_dir)
joblib.dump(y_mean, y_mean_dir)

sequential_data = build_sequential_data_from_frames(x - x_mean,
                                                    y - y_mean, 3)

x_sequential = sequential_data[:, :-1]
y_sequential = sequential_data[:, -1]

X_train, X_test, y_train, y_test =\
    train_test_split(x_sequential, y_sequential, test_size=0.1, random_state=1)

del x_sequential, y_sequential, x, y, training_data, current_data

myElastic = ElasticNetCV(cv=2, l1_ratio=0.7, fit_intercept=False)
myElastic.fit(X_train, y_train)
print "Training score: ", myElastic.score(X_train, y_train)
print "Test score: ", myElastic.score(X_test, y_test)

joblib.dump(myElastic, 'ElasticNetSeq.pkl')

