import imageio
import os


def make_gif(subfolder, base_folder=r'C:/Users/Jacob/OneDrive/Desktop/Github/nodule-self-assembly/new_cpp', fps=60):

    delete_files(subfolder, base_dir=base_folder)
    folder = os.path.join(base_folder, subfolder)
    _, _, files = next(os.walk(folder))
    # Get only those files that are pngs
    files = [file for file in files if file.endswith('.png')]
    file_count = len(files)

    # Check the directory exists
    if not os.path.exists(folder):
        print('Folder does not exist')
        return

    if file_count <= 1:
        print(
            f'Not enough files to make a gif (there are {file_count} files).')
        return

    if file_count > 1:

        indices = [int(file.split('_')[1].split('.')[0]) for file in files]
        start = min(indices)
        end = max(indices)
        spacing = int((end - start) / (file_count - 1))
        name = files[0].split('_')[0]

        def pathname(iternum):
            return name + '_' + str(iternum) + '.png'

        filenames = [
            f'{folder}/{pathname(t)}' for t in range(start, end + 1, spacing)]
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

        imageio.mimsave(
            rf'{base_folder}animation_of_{subfolder}.gif', images, format='GIF', fps=fps)
    return


def delete_files(base_folder, base_dir=r'C:/Users/jacob/OneDrive/Desktop/GitHub/nodule-self-assembly/new_cpp'):
    folder = os.path.join(base_dir, base_folder)

    # Check the directory exists
    if not os.path.exists(folder):
        print('Folder does not exist. (No files to delete.)')
        make_new_folder = input(
            f"Would you like to make a new folder ({base_folder})? (y/n) ").lower()
        if make_new_folder == 'y':
            os.mkdir(folder)
            print(f'Created folder {base_folder}.')

        return

    _, _, files = next(os.walk(folder))
    file_count = len(files)

    # Ask user permission to remove all .png files from the gif saving subfolder:
    if file_count > 0:
        remove_files = input(
            f"Remove all .png files from the {base_folder} subfolder? (y/n): ").lower()
        if remove_files == "y":
            for file in files:
                if file.endswith(".png"):
                    os.remove(os.path.join(folder, file))
        # otherwise, exit program:
        elif remove_files == "n":
            create_new_folder = input(f"Create a new folder? (y/n): ").lower()
            if create_new_folder == "y":
                new_folder = str(time.time())
                new_folder_input = input(
                    "Enter new folder name. (No input will use current datetime as name): ")

                os.mkdir(os.path.join(base_dir, base_folder+new_folder))

        else:
            print("Exiting program...")
            exit()


# make_gif('histograms', fps=10)

make_gif('data', fps=30)
