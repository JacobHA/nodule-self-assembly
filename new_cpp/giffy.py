import os
import gif
from random import randint
from matplotlib import pyplot as plt
from matplotlib import collections as mc
from matplotlib.colors import colorConverter
from csv_to_npy import convert_csv_to_nparray

# (Optional) Set the dots per inch resolution to 300
gif.options.matplotlib["dpi"] = 100


t0 = 0
folder = 'data'
# Decorate a plot function with @gif.frame


@gif.frame
def plot(i):
    plt.figure(figsize=(10, 10))
    # Set up ax
    ax = plt.gca()

    file = f'nodules_{t0 + i}.csv'
    np_array = convert_csv_to_nparray(os.path.join(folder, file))

    # Check that all rows have 3 columns
    # assert np_array.shape[1] == 3
    fc = colorConverter.to_rgba('blue', alpha=0.5)

    xs, ys, rs = np_array[:, 0], np_array[:, 1], np_array[:, 2]
    circles = [plt.Circle((xi, yi), radius=ri, fc=fc, ec=None)
               for xi, yi, ri in zip(xs, ys, rs)]

    c = mc.PatchCollection(circles)
    ax.add_collection(c)

    plt.gca().set_aspect('equal', adjustable='box')
    padding = 0.2
    x_min, x_max = 0, 50
    y_min, y_max = 0, 50
    plt.xlim(x_min - padding, x_max + padding)
    plt.ylim(y_min - padding, y_max + padding)
    print(f"frame {i} plotted from file {file}")


# Construct "frames"
NUM_FRAMES = len(os.listdir(folder))
print(f"number of frames: {NUM_FRAMES}")
frames = [plot(i) for i in range(0, NUM_FRAMES)]

# Save "frames" to gif with a specified duration (milliseconds) between each frame
gif.save(frames, 'example.gif', duration=200)
