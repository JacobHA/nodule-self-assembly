import imageio
import numpy as np
import os


def make_gif(subfolder, base_folder=r'C:/Users/Jacob/OneDrive/Desktop/Github/nodule-self-assembly/'):
    folder = base_folder + subfolder 
    _, _, files = next(os.walk(folder))
    file_count = len(files)

    # Check the directory exists
    if not os.path.exists(folder):
        print('Folder does not exist')
        return

    if file_count <= 1:
        print('Not enough files to make a gif (there are {file_count} files)')
        return

    if file_count > 1:

        filename, start = files[0].split('_')[0], int(files[0].split('_')[1].split('.'[0]))
        spacing = int(files[1].split('_')[1].split('.'[0])) - start
        end = int(files[-1].split('_')[1].split('.'[0]))


        filenames = [f'{subfolder}/{filename}_{t}.png' for t in range(start, end, spacing) ]
        images = []
        for filename in filenames:
            try:
                images.append(imageio.imread(filename))
            except SyntaxError:
                # unpack_from requires a buffer of at least 4 bytes
                # Basically, the last image was not fully saved before user stopped program
                # So just break out and use the images available
                break

        imageio.mimsave(r'{base_folder}animation_of_{subfolder}.gif', images, format = 'GIF', fps=60)
    return 


make_gif('histograms')
