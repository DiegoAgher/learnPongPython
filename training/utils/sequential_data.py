import numpy as np


def build_sequential_data_from_frames(x_data, y_data, window_size):
    num_rows = x_data.shape[0]
    frame_length = x_data.shape[1]

    sequential_data = np.zeros((num_rows, (frame_length * window_size) + 1))

    for i, vector in enumerate(x_data):
        sequential_data[i, -1] = y_data[i]
        sequential_data[i, :-1] = (x_data[i: i + window_size].
                                   reshape((1, frame_length * window_size)))

        if i == num_rows - window_size:
            break

    return sequential_data


