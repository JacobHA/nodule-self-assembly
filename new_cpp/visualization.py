import matplotlib.pyplot as plt
import os
from csv_to_npy import convert_csv_to_nparray


def make_nodule_plot(dataset, timestep, X_LENGTH, Y_LENGTH):
    plt.figure(figsize=(10, 10))
    # Set aspect ratio to be equal so that circles look like circles
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0, X_LENGTH)
    plt.ylim(0, Y_LENGTH)
    for pos_vec_x, pos_vec_y, pos_vec_z, radius in dataset:
        circle = plt.Circle((pos_vec_x, pos_vec_y),
                            radius, color='b', alpha=0.8)
        plt.gca().add_patch(circle)

    # Try using cv2 imwrite
    # or plt.imsave
    plt.savefig(rf'data/timestep_{timestep}.png')
    plt.clf()
    plt.close()


def generate_plots_from_csv(folder: str):
    # Loop through all csv files in the folder
    for file in os.listdir(folder):
        if file.endswith('.csv'):
            # Strip the timestep from the filename
            timestep = file.split('_')[1].split('.')[0]
            # Convert csv file to numpy array
            np_array = convert_csv_to_nparray(os.path.join(folder, file))
            # Plot the numpy array
            make_nodule_plot(np_array, timestep, 500, 500)


if __name__ == '__main__':
    generate_plots_from_csv('data')
