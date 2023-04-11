import os
import gif
from random import randint
from matplotlib import pyplot as plt
from csv_to_npy import convert_csv_to_nparray

# (Optional) Set the dots per inch resolution to 300
gif.options.matplotlib["dpi"] = 100


t0 = 1
folder = 'data'
# Decorate a plot function with @gif.frame


@gif.frame
def plot(i):
    plt.figure(figsize=(10, 10))

    file = f'nodules_{t0 + i}.csv'
    np_array = convert_csv_to_nparray(os.path.join(folder, file))

    plt.scatter(np_array[:, 0], np_array[:, 1],
                s=np_array[:, 2], c='b', alpha=0.8)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0, 200)
    plt.ylim(0, 200)
    print(i)


# Construct "frames"
frames = [plot(i) for i in range(20)]

# Save "frames" to gif with a specified duration (milliseconds) between each frame
gif.save(frames, 'example.gif', duration=500)
