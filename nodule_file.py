# Here we will define the "nodule" class 
# which will be used to store the information
# about the nodules in the set of cancer cells.

import cProfile
import numpy as np
# from numba import jit
from utils import make_histogram, make_nodule_plot, delete_files, squared_distance
from math import sqrt, pow


X_LENGTH = 500
Y_LENGTH = 500
Z_LENGTH = 200

LATTICE_SCALE = 1
DISTANCE_EPSILON = 0.1

class Nodule:
    def __init__(self, two_dimensional=False, growth_rate=1):
        self.x = None
        self.y = None
        self.z = None
        self.radius = None
        self.two_dimensional = two_dimensional
        self.growth_rate = growth_rate

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

    def _is_isolated(self, nodules):
        raise NotImplementedError
        isolated_from_nodule = np.ones(len(nodules), dtype=bool)
        for i, nodule in enumerate(nodules):
            if nodule == self:
                continue
                # As a (possible) speed-up, we can check whether
                # the distance between the two nodules is more than
                # what is possibly acheivable in the next timestep:
                # Note: this is still overestimating, because they will
                # likely not be directly in line.
            else:
                distance = np.linalg.norm(self.position_vector - nodule.position_vector)
                if distance > nodule.radius + self.radius + self.max_movement + nodule.max_movement:
                    # If it is, then we can mask this module to not check on next timestep:
                    isolated_from_nodule[i] = True
        return isolated_from_nodule.all()

    def _timestep(self, nodules):
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
        
        for i, nodule in enumerate(nodules):
            if nodule == self:
                continue
            else:
                if True: #not self._is_isolated(nodules): #mask[i]:
                    # distance = np.linalg.norm(self.position_vector - nodule.position_vector)
                    distance2 = squared_distance(nodule.position_vector, self.position_vector)
                  
                    if distance2 < (nodule.radius + self.radius)**2:
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
        self._grow()
        return nodules

    def _grow(self):
        # more realistic is randomly dividing the cell
        if self.two_dimensional:
            new_area = self.growth_rate * np.pi * self.radius**2 
            new_radius = np.sqrt(new_area / np.pi)
        else:
            new_volume = self.growth_rate * (4/3) * np.pi * self.radius**3
            new_radius = (new_volume / (4/3) * np.pi)**(1/3)

        self._update_radius(new_radius)

    @property
    def position_vector(self):
        return [self.x, self.y, self.z]




def main():
    
    delete_files('gif_folder')
    delete_files('histograms')
    # This effectively defines a short range attractive force
    # between two nodules.

    # first, we must generate a field of objects,
    # by randomly assigning each object a position and radius
    NUM_NODULES = 150
    nodules = []
    for i in range(NUM_NODULES):
        position = np.random.randint(0, X_LENGTH, 3)
        radius = np.abs(np.random.normal(1, 0.5))
        nodule = Nodule(two_dimensional=True, growth_rate=1.00001)
        nodule._update_position(*position)
        nodule._update_radius(radius)
        nodules.append(nodule)

    # Now we need to iterate through the nodules,
    # and check for collisions.
    for t in range(50):
        # mask = np.ones((NUM_NODULES, NUM_NODULES), dtype=bool)
        # update all of the nodules' positions
        for nodule in nodules:

            nodules = nodule._timestep(nodules)

        print(len(nodules), flush=True, end='\r')
  
        if t % 50 == 0:
            make_nodule_plot(nodules, t, X_LENGTH, Y_LENGTH)
            make_histogram(nodules, save_num = t, scale=(nodules[0].growth_rate)**t)

        if len(nodules) <= 1:
            break


if __name__ == "__main__":
    
    import pstats
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()   

    profiler.dump_stats('profile.prof')

    # main()