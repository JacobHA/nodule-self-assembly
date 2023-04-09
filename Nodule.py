import numpy as np
X_LENGTH = 500
Y_LENGTH = 500
Z_LENGTH = 200

LATTICE_SCALE = 1
DISTANCE_EPSILON = 0.1


class Nodule:
    def __init__(self, dimensions: int = 2, growth_rate=1):
        self.x = None
        self.y = None
        self.z = None
        self.radius = None
        self.dimensions = dimensions
        self.growth_rate = growth_rate

        # The maximum movement of the nodule in one timestep
        self.max_movement = (2 * self.dimensions)**(1/2)

    def _update_position(self, x, y, z):
        self.x = x
        self.y = y
        if self.dimensions == 2:
            self.z = 0
        else:
            self.z = z

    def _update_radius(self, radius):
        self.radius = radius

    @property
    def position_vector(self):
        return np.array([self.x, self.y, self.z])

    def _timestep(self):
        # for each co-ordinate, generate a random, unbiased
        # value, either -1, 0, or 1.
        # then, update the position by adding the random value
        # to the current position.
        dx = np.random.randint(-1, 2)
        dy = np.random.randint(-1, 2)
        if self.dimensions == 2:
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

        self._grow()
        return

    def _grow(self):
        # more realistic is randomly dividing the cell
        if self.dimensions == 2:
            new_area = self.growth_rate * np.pi * self.radius**2
            new_radius = np.sqrt(new_area / np.pi)
        elif self.dimensions == 3:
            new_volume = self.growth_rate * (4/3) * np.pi * self.radius**3
            new_radius = (new_volume / (4/3) * np.pi)**(1/3)

        self._update_radius(new_radius)
