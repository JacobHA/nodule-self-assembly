#include <iostream>
#include "NoduleField.h"

int main(int argc, char* argv[]) {

    // use the input arg as distance epsilon
    // Check that at least one argument was passed
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <double_arg>\n";
    return 1;
    }

    // Convert the first argument to a std::double
    std::cout << "Distance epsilon: " << argv[1] << std::endl;


    int num_nodules = 300;
    double x_length = 50;
    double y_length = 50;
    double lattice_scale = 1;
    double distance_epsilon = std::stod(argv[1]); 
    double growth_rate = 0;
    bool verbose = false;

    NoduleField nodule_field(num_nodules, x_length, y_length, lattice_scale, distance_epsilon, true, growth_rate, verbose);
    
    if (verbose){
        std::cout << "Number of nodules: " << nodule_field.get_num_nodules() << std::endl;
    }

    for (int t=0; t<100; t++){

        nodule_field.simulate(1);
        if (verbose){
            std::cout << "Number of nodules: " << nodule_field.get_num_nodules() << std::endl;
        }
    }
    return 0;
}