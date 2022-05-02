import imageio
import numpy as np
import os


def make_gif(subfolder, base_folder=r'C:/Users/Jacob/OneDrive/Desktop/Github/nodule-self-assembly/gif_folder'):
folder = base_folder + '/ ' + subfolder + '/'
_, _, files = next(os.walk(folder))
file_count = len(files)


filenames = [f'gif_folder/timestep_{t}.png' for t in range(0,file_count)]
images = []
for filename in filenames:
    try:
        images.append(imageio.imread(filename))
    except SyntaxError:
        # unpack_from requires a buffer of at least 4 bytes
        # Basically, the last image was not fully saved before user stopped program
        # So just break out and use the images available
        break
imageio.mimsave(r'C:/Users/Jacob/OneDrive/Desktop/Github/nodule-self-assembly/animation.gif', images, format = 'GIF', fps=60)
