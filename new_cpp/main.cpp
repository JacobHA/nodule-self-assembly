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
    int num_nodules = 600;
    int x_length = 200;
    int y_length = 200;
    int z_length = 1;
    int lattice_scale = 1;
    double distance_epsilon = 0.0005;

    NoduleField nodule_field(dim, num_nodules, x_length, y_length, z_length, lattice_scale, distance_epsilon, true);
    std::cout << "Number of nodules: " << nodule_field.get_num_nodules() << std::endl;

    for (int t=0; t<20; t++){

        nodule_field.simulate(1);

        std::cout << "Number of nodules: " << nodule_field.get_num_nodules() << std::endl;

    }

    return 0;
}