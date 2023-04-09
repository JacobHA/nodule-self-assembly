import numpy as np

from Nodule import *


class NoduleField:
    def __init__(self, num_nodules=10, x_length=500, y_length=500, z_length=200, lattice_scale=1, distance_epsilon=0.1):
        self.x_length = x_length
        self.y_length = y_length
        self.z_length = z_length
        self.lattice_scale = lattice_scale
        self.distance_epsilon = distance_epsilon
        self.num_nodes = num_nodules
        self.nodules = []
        self.removable_nodules = []

        for _ in range(num_nodules):
            position = np.random.randint(0, (x_length, y_length, z_length))
            np.random.randint
            radius = np.abs(np.random.exponential(1))
            nodule = Nodule(dimensions=2, growth_rate=1.00001)
            nodule._update_position(*position)
            nodule._update_radius(radius)
            self.nodules.append(nodule)

    def _check_collision(self, nodule1, nodule2):
        distance = np.linalg.norm(
            nodule1.position_vector - nodule2.position_vector)
        return distance <= (nodule1.radius + nodule2.radius + self.distance_epsilon)

    def _resolve_collision(self, nodule1, nodule2):
        # combine nodules into one by updating its position and radius
        combined_radius = (nodule1.radius ** 3 +
                           nodule2.radius ** 3) ** (1 / 3)
        combined_position = (nodule1.position_vector +
                             nodule2.position_vector) / 2
        nodule1._update_position(
            combined_position[0], combined_position[1], combined_position[2])
        nodule1._update_radius(combined_radius)

        # remove the absorbed nodule from the list of nodules
        self._remove_nodules(nodule2, flush=False)

    def _remove_nodules(self, nodule, flush=False):
        if not flush:
            self.removable_nodules.append(nodule)
        if flush:
            print(f"Removing {len(self.removable_nodules)} nodules")
            for n in self.removable_nodules:
                self.nodules.remove(n)
            self.removable_nodules = []

    def absorb_collisions(self):
        for i in range(len(self.nodules)):
            nodule1 = self.nodules[i]
            for j in range(i + 1, len(self.nodules)):
                nodule2 = self.nodules[j]
                if self._check_collision(nodule1, nodule2):
                    self._resolve_collision(nodule1, nodule2)

        self._remove_nodules(self.removable_nodules, flush=True)

    def _timestep(self):
        for nodule in self.nodules:
            nodule._timestep()

        # Now, perform the collision detection and resolution
        self.absorb_collisions()

    def simulate(self, num_timesteps):
        for _ in range(num_timesteps):
            self._timestep()
