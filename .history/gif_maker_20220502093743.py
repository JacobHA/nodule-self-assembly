import imageio
import numpy as np
import os


def make_gif(subfolder, base_folder=r'C:/Users/Jacob/OneDrive/Desktop/Github/nodule-self-assembly/', fps = 60):
    folder = os.path.join(base_folder, subfolder)
    _, _, files = next(os.walk(folder))
    file_count = len(files)

    # Check the directory exists
    if not os.path.exists(folder):
        print('Folder does not exist')
        return

    if file_count <= 1:
        print(f'Not enough files to make a gif (there are {file_count} files).')
        return

    if file_count > 1:

        indices = [int(file.split('_')[1].split('.')[0]) for file in files]
        start = min(indices)
        end = max(indices)
        spacing = int((end - start) / (file_count - 1))
        print(spacing)
        name = files[0].split('_')[0]
        # spacing = int(files[1].split('_')[1].split('.')[0]) - start
        # end = int(files[-1].split('_')[1].split('.')[0])
        # print(start, spacing, end)

        def pathname(file, iternum):
            return file + '_' + str(iternum) + '.png'

        filenames = [f'{folder}/{pathname('filename',t)}' for t in range(start, end + 1, spacing) ]
        print(f'Using {len(filenames)} files to make the gif.')
        images = []
        for filename in filenames:
            try:
                images.append(imageio.imread(filename))
            except SyntaxError:
                # unpack_from requires a buffer of at least 4 bytes
                # Basically, the last image was not fully saved before user stopped program
                # So just break out and use the images available
                break

        imageio.mimsave(rf'{base_folder}animation_of_{subfolder}.gif', images, format = 'GIF', fps=fps)
    return 


make_gif('histograms', fps=10)
make_gif('gif_folder', fps=60)
