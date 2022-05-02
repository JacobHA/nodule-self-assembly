# Here we will define the "nodule" class 
# which will be used to store the information
# about the nodules in the set of cancer cells.

from gym import make
import numpy as np
import matplotlib.pyplot as plt

X_LENGTH = 200
Y_LENGTH = 200
Z_LENGTH = 200

LATTICE_SCALE = 10
DISTANCE_EPSILON = 0.1

class Nodule:
    def __init__(self, two_dimensional=False):
        self.x = None
        self.y = None
        self.z = None
        self.radius = None
        self.two_dimensional = two_dimensional

        # The maximum movement of the nodule in one timestep
        if self.two_dimensional:
            self.max_movement = (2 + 2)**(1/2)
        self.max_movement = (2 + 2 + 2)**(1/2)
        
    def _update_position(self, x, y, z):
        self.x = x
        self.y = y
        if self.two_dimensional:
            self.z = 0
        else:
            self.z = z

    def _update_radius(self, radius):
        self.radius = radius

    def _timestep(self, nodules, mask):
        # for each co-ordinate, generate a random, unbiased 
        # value, either -1, 0, or 1.
        # then, update the position by adding the random value
        # to the current position.
        dx = np.random.randint(-1, 2)
        dy = np.random.randint(-1, 2)
        if self.two_dimensional:
            dz = 0
        else:
            dz = np.random.randint(-1, 2)

        self.x += dx / LATTICE_SCALE
        self.y += dy / LATTICE_SCALE
        self.z += dz / LATTICE_SCALE

        # Need to impose periodic boundary conditions
        # on the position vector.

        self.x = self.x % X_LENGTH
        self.y = self.y % Y_LENGTH
        self.z = self.z % Z_LENGTH

        # Now we need to check if the new position is
        # within the radius of any of the other nodules.
        # If it is, we need to update the radius
        new_mask = mask.copy()
        for i, nodule in enumerate(nodules):
            if nodule == self:
                continue
            else:
                if mask[i]:
                    distance = np.linalg.norm(self.position_vector() - nodule.position_vector())
                    if distance < nodule.radius + self.radius:
                        if self.two_dimensional:
                            # conserve area
                            total_area = 4 * np.pi * (self.radius**2 + nodule.radius**2)
                            new_radius = np.sqrt(total_area / (4 * np.pi))
                        else:
                            # conserve volume
                            total_volume = (4/3) * np.pi * (nodule.radius**3 + self.radius**3)
                            new_radius = (total_volume / (4/3) * np.pi)**(1/3) 

                        # Update the larger one to "absorb" the smaller one
                        # And delete the smaller one
                        if self.radius >= nodule.radius:
                            self._update_radius(new_radius)
                            nodules.remove(nodule)

                        else: #if nod_i.radius < nod_j.radius:
                            nodule._update_radius(new_radius)
                            nodules.remove(self)

                    # As a (possible) speed-up, we can check whether
                    #  the distance between the two nodules is more than
                    # what is possibly acheivable in the next timestep:
                    # Note: this is still overestimating, because they will
                    # likely not be directly in line.
                    if distance > nodule.radius + self.radius + self.max_movement + nodule.max_movement:
                        # If it is, then we can mask this module to not check on next timestep:
                        new_mask[i] = False

        return nodules, new_mask



    def position_vector(self):
        return np.array([self.x, self.y, self.z])


def make_histogram(nodules,bins=None, save_num=None):
    # make a histogram based on size distribution

    radii = [nodule.radius for nodule in nodules]

    plt.figure()
    plt.hist(radii, bins=bins)
    if save_num is None:
        plt.show()

    else:
        plt.savefig(f'histograms/histogram_{save_num}.png')

def main():
    # This effectively defines a short range attractive force
    # between two nodules.

    # first, we must generate a field of objects,
    # by randomly assigning each object a position and radius
    NUM_NODULES = 100
    nodules = []
    for i in range(NUM_NODULES):
        position = np.random.randint(0, X_LENGTH, 3)
        radius = np.abs(np.random.normal(1, 0.5))
        nodule = Nodule(two_dimensional=True)
        nodule._update_position(*position)
        nodule._update_radius(radius)
        nodules.append(nodule)

    # Now we need to iterate through the nodules,
    # and check for collisions.
    for t in range(50_000):
        mask = np.ones(NUM_NODULES, dtype=bool)
        # update all of the nodules' positions
        for nodule in nodules:
            nodules, mask = nodule._timestep(nodules, mask)

                   
        # plt.figure(figsize=(10,10))
        # plt.xlim(0, X_LENGTH)
        # plt.ylim(0, Y_LENGTH)
        # for nodule in nodules:
        #     circle = plt.Circle((nodule.x, nodule.y), nodule.radius, color='b', alpha=0.8)
        #     plt.gca().add_patch(circle)   
             
        # plt.savefig(r'gif_folder/timestep_%d.png' % t)
        # plt.close()

        if t % 500 == 0:
            print(len(nodules))
            print(mask)
            make_histogram(nodules, save_num = t)


def delete_files(folder, base_dir=r'C:/Users/jacob/OneDrive/Desktop/GitHub/nodule-self-assembly/'):
    folder = base_dir + folder + '/'
    import os

    # Check the directory exists
    if not os.path.exists(folder):
        print('Folder does not exist')
        return

    _, _, files = next(os.walk(folder))
    file_count = len(files)

    # Ask user permission to remove all .png files from the gif saving subfolder:
    if file_count > 0:
        remove_files = input("Remove all .png files from the gif saving subfolder? (y/n) ")
        if remove_files == "y":
            for file in files:
                os.remove(folder + file)
        # otherwise, exit program:
        else:
            print("Exiting program...")
            exit()

if __name__ == "__main__":
    
    delete_files('gif_folder')
    delete_files('histograms')
    
    main()