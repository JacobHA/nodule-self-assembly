import os
import gif
from random import randint
from matplotlib import pyplot as plt

from csv_to_npy import convert_csv_to_nparray

x = [randint(0, 100) for _ in range(100)]
y = [randint(0, 100) for _ in range(100)]

# (Optional) Set the dots per inch resolution to 300
gif.options.matplotlib["dpi"] = 300


t0 = 716965745
folder = 'data'
# Decorate a plot function with @gif.frame


@gif.frame
def plot(i):
    plt.figure(figsize=(10, 10))

    file = f'nodules_{t0 + i}.csv'
    np_array = convert_csv_to_nparray(os.path.join(folder, file))
    # Plot the numpy array
    # for pos_vec_x, pos_vec_y, pos_vec_z, radius in np_array:
    #     circle = plt.Circle((pos_vec_x, pos_vec_y),
    #                         radius, color='b', alpha=0.8)
    #     plt.gca().add_patch(circle)

    # Do plt.scatter of the same thing above, should be much faster:
    plt.scatter(np_array[:, 0], np_array[:, 1],
                s=np_array[:, 3], c='b', alpha=0.8)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0, 500)
    plt.ylim(0, 500)
    print(i)


# Construct "frames"
frames = [plot(i) for i in range(200)]

# Save "frames" to gif with a specified duration (milliseconds) between each frame
gif.save(frames, 'example.gif', duration=50)
