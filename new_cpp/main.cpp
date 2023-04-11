#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <random>
#include <cmath>
#include <array>

#include "Nodule.h"
#include "NoduleField.h"
#include <cmath>

int main() {

    int dim = 2;
    int num_nodules = 800;
    int x_length = 500;
    int y_length = 500;
    int z_length = 2;
    int lattice_scale = 1;
    double distance_epsilon = 0.000;

    NoduleField nodule_field(dim, num_nodules, x_length, y_length, z_length, lattice_scale, distance_epsilon, true);
    std::cout << "Number of nodules: " << nodule_field.get_num_nodules() << std::endl;

    for (int t=0; t<100; t++){

        nodule_field.simulate(2);

        std::cout << "Number of nodules: " << nodule_field.get_num_nodules() << std::endl;

    }

    return 0;
}