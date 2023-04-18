#include <iostream>
#include "NoduleField.h"

int main() {

    int num_nodules = 200;
    double x_length = 50;
    double y_length = 50;
    double lattice_scale = 1;
    double distance_epsilon = 0.0001;
    double growth_rate = 0;

    NoduleField nodule_field(num_nodules, x_length, y_length, lattice_scale, distance_epsilon, true, growth_rate);
    std::cout << "Number of nodules: " << nodule_field.get_num_nodules() << std::endl;

    for (int t=0; t<50; t++){

        nodule_field.simulate(1);

        std::cout << "Number of nodules: " << nodule_field.get_num_nodules() << std::endl;

    }

    return 0;
}