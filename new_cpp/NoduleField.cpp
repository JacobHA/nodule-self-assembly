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


#include "nodule.h"
#include "NoduleField.h"

NoduleField::NoduleField(int dimensions, int num_nodules, int x_length, int y_length, int z_length, int lattice_scale, double distance_epsilon, bool write_to_file, double growth_rate) {
    this->dimensions = dimensions;
    this->num_nodules = num_nodules;
    this->x_length = x_length;
    this->y_length = y_length;
    this->z_length = z_length;
    this->lattice_scale = lattice_scale;
    this->distance_epsilon = distance_epsilon;
    this->growth_rate = growth_rate;
    this->write_to_file = write_to_file;

    double mu = 1.0;
    std::exponential_distribution<double> dist(1.0 / mu);
    std::mt19937_64 rng; // Use the 64-bit Mersenne Twister as the random number generator

    for (int i = 0; i < this->num_nodules; i++) {
        double position[3] = {static_cast<double>(rand() % this->x_length), static_cast<double>(rand() % this->y_length), static_cast<double>(rand() % this->z_length)};

        double radius_epsilon = 0.001;
        double radius = dist(rng) + radius_epsilon;

        Nodule nodule(this->dimensions, 
                    this->growth_rate,
                    this->x_length, 
                    this->y_length, 
                    this->z_length, 
                    this->lattice_scale);

        nodule._update_position(position[0], position[1], position[2]);
        nodule._update_radius(radius);

        nodules_.push_back(nodule);
    }
    std::cout << "Finished initializing " << get_num_nodules() << "/" << this->num_nodules << " nodules." << std::endl;
}

int NoduleField::get_num_nodules() const {
    // Get the length of the nodules vector
    return nodules_.size();
}

bool NoduleField::_check_collision(Nodule nodule1, Nodule nodule2) {
    double distance;
    if (dimensions == 3){
        distance = std::sqrt(std::pow(nodule1.get_position()[0] - nodule2.get_position()[0], 2) +
                                std::pow(nodule1.get_position()[1] - nodule2.get_position()[1], 2) +
                                std::pow(nodule1.get_position()[2] - nodule2.get_position()[2], 2));
    }
    if (dimensions == 2){
        distance = std::sqrt(std::pow(nodule1.get_position()[0] - nodule2.get_position()[0], 2) +
                                std::pow(nodule1.get_position()[1] - nodule2.get_position()[1], 2));
    }        
    return distance <= (nodule1.radius + nodule2.radius + this->distance_epsilon);
    }

void NoduleField::_resolve_collision(Nodule& nodule1, Nodule& nodule2, int idx2) {
    // combine nodules into one by updating its position and radius
    double combined_radius = std::pow((std::pow(nodule1.radius, 3) +
                        std::pow(nodule2.radius, 3)), (1.0 / 3));
    double combined_position[3] = {(nodule1.get_position()[0] + nodule2.get_position()[0]) / 2,
                                    (nodule1.get_position()[1] + nodule2.get_position()[1]) / 2,
                                    (nodule1.get_position()[2] + nodule2.get_position()[2]) / 2};
    nodule1._update_position(combined_position[0], combined_position[1], combined_position[2]);
    nodule1._update_radius(combined_radius);

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
        }
    }

    // Clear removable_nodule_indices_
    indx_list.clear();

    // Print how many nodules were removed and how many are left
    std::cout << "Removed " << num_removed << " nodules." << std::endl;
    std::cout << "There are " << get_num_nodules() << " nodules left." << std::endl;
}
void NoduleField::absorb_collisions() {
    for (int i = 0; i < nodules_.size(); i++) {
        Nodule& nodule1 = nodules_[i];
        for (int j = i + 1; j < nodules_.size(); j++) {
            Nodule& nodule2 = nodules_[j];
            if (_check_collision(nodule1, nodule2)) {
                _resolve_collision(nodule1, nodule2, j);
            }
        }
    }
    _destroy_nodules(removable_nodule_indices_);
}

void NoduleField::_timestep() {
    for (auto& nodule : nodules_) {
        nodule._timestep();
    }
    absorb_collisions();
}

void NoduleField::simulate(int num_timesteps) {
    for (int i = 0; i < num_timesteps; i++) {
        _timestep();
        // Increment the internal timestep counter
        timestep_++;
        if (write_to_file) {
            std::string filename = std::string("data/nodules_") + std::to_string(timestep_) + ".csv";

            _write_nodules_to_file(filename);
        }
    }
}

void NoduleField::_write_nodules_to_file(const std::string& filename) const {

    // Check if file exists
    std::ifstream infile(filename);
    if (infile.good()) {
        std::cerr << "File " << filename << " already exists." << std::endl;
        infile.close();
        return;
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
        if (dimensions == 2) {
            outfile << pos[0] << "," << pos[1] << "," << radius << std::endl;
        }
        if (dimensions == 3) {
            outfile << pos[0] << "," << pos[1] << "," << pos[2] << "," << radius << std::endl;
        }
    }

    // Close file
    outfile.close();
}