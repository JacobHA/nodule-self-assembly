#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <algorithm>
#include <random>
#include <cmath>
#include <array>
#include <fstream>


#include "Nodule.h"
#include "NoduleField.h"

NoduleField::NoduleField(int num_nodules, double x_length, double y_length, double lattice_scale, double distance_epsilon, bool write_to_file, double growth_rate) {
    this->num_nodules = num_nodules;
    this->x_length = x_length;
    this->y_length = y_length;
    this->lattice_scale = lattice_scale;
    this->distance_epsilon = distance_epsilon;
    this->growth_rate = growth_rate;
    this->write_to_file = write_to_file;

    double mu = 1.0;
    std::exponential_distribution<double> dist(1.0 / mu);
    std::uniform_real_distribution<double> dist2(0.0, 1.0);
    std::mt19937_64 rng; // Use the 64-bit Mersenne Twister as the random number generator

    for (int i = 0; i < this->num_nodules; i++) {

        double radius_epsilon = 0.00;
        double radius = 0.1; //* dist(rng) + radius_epsilon;

        Nodule nodule(this->growth_rate,
                      this->x_length, 
                      this->y_length, 
                      this->lattice_scale);

        // Generate random values for the x,y,z coordinates of the nodule.
        std::vector<double> position(this->dimensions);

        double x_0 = dist2(rng) * x_length;
        double y_0 = dist2(rng) * y_length;
        std::cout << "x_0: " << x_0 << std::endl;
        std::cout << "y_0: " << y_0 << std::endl;
        nodule.set_position(x_0, y_0);
        nodule.set_radius(radius);

        nodules_.push_back(nodule);
    }
    std::cout << "Finished initializing " << get_num_nodules() << "/" << this->num_nodules << " nodules." << std::endl;

    if (write_to_file){
        // Delete all files in the data directory.
        std::cout << "Deleting all files in the data directory." << std::endl;
        std::string win_command = "del data\\*";
        std::string lin_command = "rm data/*";
        system(win_command.c_str());
    }
}

bool NoduleField::_check_collision(Nodule nodule1, Nodule nodule2) {
    // First, need to modulo by the length of the field to account for periodic boundary conditions.
    double x1 = nodule1.get_position()[0];
    double y1 = nodule1.get_position()[1];
    double x2 = nodule2.get_position()[0];
    double y2 = nodule2.get_position()[1];

    // Use the Nodule modrem method
    double x1_mod = nodule1.modrem(x1, x_length);
    double y1_mod = nodule1.modrem(y1, y_length);
    double x2_mod = nodule2.modrem(x2, x_length);
    double y2_mod = nodule2.modrem(y2, y_length);

    double distance = std::sqrt(
        std::pow(x1_mod - x2_mod, 2) + std::pow(y1_mod - y2_mod, 2));
    return distance <= (nodule1.get_radius() + nodule2.get_radius() + distance_epsilon);
}

void NoduleField::_resolve_collision(Nodule& nodule1, Nodule& nodule2, int idx2) {
    // combine nodules into one by updating its position and radius
    double combined_radius;
    double weight = nodule1.get_area() / (nodule1.get_area() + nodule2.get_area());

    double combined_position[2] = {weight * nodule1.get_position()[0] + (1 - weight) * nodule2.get_position()[0],
                                   weight * nodule1.get_position()[1] + (1 - weight) * nodule2.get_position()[1]};

    // Weight the combined_position to the COM
    nodule1.set_position(combined_position[0], combined_position[1]);
    combined_radius = std::sqrt(
        (std::pow(nodule1.get_radius(), 2) +
        std::pow(nodule2.get_radius(), 2))
                              );
    std::cout << "Combined radius: " << combined_radius << std::endl;
    nodule1.set_radius(combined_radius);

    // remove the absorbed nodule from the list of nodules
    _garbage_collect_nodule(idx2);
}

void NoduleField::_garbage_collect_nodule(int idx) {
    removable_nodule_indices_.push_back(idx);
}

void NoduleField::_destroy_nodules(std::vector<int>& indx_list) {
    // Sort indices in descending order and remove duplicates
    std::sort(indx_list.begin(), indx_list.end(), std::greater<int>());
    indx_list.erase(std::unique(indx_list.begin(), indx_list.end()), indx_list.end());

    // Remove nodules corresponding to indices
    int num_removed = 0;
    for (auto it = indx_list.begin(); it != indx_list.end(); ++it) {
        int index = *it;
        if (index < nodules_.size()) {
            nodules_.erase(nodules_.begin() + index);
            ++num_removed;
            // Subtract 1 from all indices greater than the removed index
            // to account for the shift in the vector size
            for (auto it2 = it + 1; it2 != indx_list.end(); ++it2) {
                if (*it2 > index) {
                    *it2 -= 1;
                }
            }
        }
    }
    // Clear removable_nodule_indices_
    indx_list.clear();

    // Print how many nodules were removed and how many are left
    std::cout << "Removed " << num_removed << " nodules." << std::endl;
    std::cout << "There are " << get_num_nodules() << " nodules left." << std::endl;
}

void NoduleField::_absorb_collisions() {
    for (int i = 0; i < nodules_.size(); i++) {
        Nodule& nodule1 = nodules_[i];
        for (int j = i + 1; j < nodules_.size(); j++) {
            Nodule& nodule2 = nodules_[j];
            if (_check_collision(nodule1, nodule2)) {
                _resolve_collision(nodule1, nodule2, j);
                // collect the indices of the nodules to be removed
                _garbage_collect_nodule(j);
            }
            _destroy_nodules(removable_nodule_indices_);

        }
    }
}

void NoduleField::_timestep() {
    for (auto& nodule : nodules_) {
        nodule._timestep();
    }
    _absorb_collisions();

    // Find the total area present in the field
    // double total_area_ = 0;
    // for (auto& nodule : nodules_) {
    //     total_area_ += nodule.get_area();
    // }
    // print the total area
    // std::cout << "Total area: " << total_area_ << std::endl;
}

void NoduleField::simulate(int num_timesteps) {
    for (int i = 0; i < num_timesteps; i++) {
        if (write_to_file) {
            std::string filename = std::string("data/nodules_") + std::to_string(timestep_) + ".csv";
            _write_nodules_to_file(filename);
        }
        _timestep();
        // Increment the internal timestep counter
        timestep_++;

    }
}

void NoduleField::_write_nodules_to_file(const std::string& filename) const {
    // Check if file exists
    std::ifstream infile(filename);
    if (infile.good()) {
        std::cerr << "File " << filename << " already exists." << std::endl;
        infile.close();
    }
 
    // Open file for writing
    std::ofstream outfile(filename);

    if (!outfile.is_open()) {
        std::cerr << "Unable to open file " << filename << " for writing." << std::endl;
        return;
    }

    // Write nodules' positions and radii to file
    for (const auto& nodule : nodules_) {
        const auto& pos = nodule.get_position();
        double radius = nodule.get_radius();
        outfile << pos[0] << "," << pos[1] << "," << radius << std::endl;
    }

    // Close file
    outfile.close();
}