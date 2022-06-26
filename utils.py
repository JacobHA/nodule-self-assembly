import os
import matplotlib.pyplot as plt
import time
import math 

# ?
# min(vectorlist, key = lambda  compare: sum([(a - b)**2 for a, b in zip(vector1, compare)]) 
def squared_distance(v1, v2):
    # square root calculation is expensive, so we keep in "square-space" for comparisons
    dist = [(a - b)**2 for a, b in zip(v1, v2)]
    dist = sum(dist)
    return dist

def make_histogram(nodules,bins=None, save_num=None, scale=1):
    # make a histogram based on size distribution

    radii = [nodule.radius for nodule in nodules]
    if save_num == 0:
        plt.figure()
        
    plt.title(f'Radius size distribution, timestep {save_num}')
    plt.ylim(0, len(nodules))
    plt.xlim(0,20*scale) # TODO: need to change this to be the max radius possible
    plt.hist(radii, bins=bins)
    if save_num is None:
        plt.show()
    else:
        plt.savefig(f'histograms/histogram_{save_num}.png')
    plt.cla()
    plt.close()

def make_nodule_plot(nodules, t, X_LENGTH, Y_LENGTH):
    if t == 0:
        plt.figure(figsize=(10,10))
    plt.xlim(0, X_LENGTH)
    plt.ylim(0, Y_LENGTH)
    for nodule in nodules:
        circle = plt.Circle((nodule.x, nodule.y), nodule.radius, color='b', alpha=0.8)
        plt.gca().add_patch(circle)   
            
    # Try using cv2 imwrite
    # or plt.imsave
    plt.savefig(r'gif_folder/timestep_%d.png' % t)
    plt.clf()

def delete_files(base_folder, base_dir=r'C:/Users/jacob/OneDrive/Desktop/GitHub/nodule-self-assembly/'):
    folder = os.path.join(base_dir, base_folder)

    # Check the directory exists
    if not os.path.exists(folder):
        print('Folder does not exist. (No files to delete.)')
        make_new_folder = input(f"Would you like to make a new folder ({base_folder})? (y/n) ").lower()
        if make_new_folder == 'y':
            os.mkdir(folder)
            print(f'Created folder {base_folder}.')

        return

    _, _, files = next(os.walk(folder))
    file_count = len(files)

    # Ask user permission to remove all .png files from the gif saving subfolder:
    if file_count > 0:
        remove_files = input(f"Remove all .png files from the {base_folder} subfolder? (y/n): ").lower()
        if remove_files == "y":
            for file in files:
                os.remove(os.path.join(folder, file))
        # otherwise, exit program:
        elif remove_files == "n":
            create_new_folder = input(f"Create a new folder? (y/n): ").lower()
            if create_new_folder == "y":
                new_folder = str(time.time())
                new_folder_input = input("Enter new folder name. (No input will use current datetime as name): ")

                os.mkdir(os.path.join(base_dir, base_folder+new_folder))

        else:
            print("Exiting program...")
            exit()
