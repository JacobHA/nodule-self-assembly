#include <cmath>
#include <cstdlib>
#include <vector>
#include <random>
#include <cmath>
#include <array>

#include "Nodule.h"
#include <cmath>

Nodule::Nodule(int dimensions, double _growth_rate, int x_length, int y_length, int z_length, int lattice_scale) {
    this->x_length = x_length;
    this->y_length = y_length;
    this->z_length = z_length;
    this->lattice_scale = lattice_scale;
    this->dimensions = dimensions;
    this->_growth_rate = _growth_rate;

    this->position = new double[dimensions];
    this->radius = 0;
}

void Nodule::_update_position(double x, double y, double z) {
    this->position[0] = x;
    this->position[1] = y;
    if (this->dimensions == 3) {
        this->position[2] = z;
    }
}

void Nodule::_update_radius(double radius) {
    this->radius = radius;
}

void Nodule::_grow() {
    double new_radius;
    if (this->dimensions == 2) {
        double new_area = this->_growth_rate * M_PI * pow(this->radius, 2);
        new_radius = sqrt(new_area / M_PI);
    } else {
        double new_volume = this->_growth_rate * (4.0/3.0) * M_PI * pow(this->radius, 3);
        new_radius = pow(new_volume / ((4.0/3.0) * M_PI), 1.0/3.0);
    }
    this->_update_radius(new_radius);
}

void Nodule::_timestep() {
    // for each co-ordinate, generate a random, unbiased
    // value, either -1, 0, or 1.
    // then, update the position by adding the random value
    // to the current position.
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(-1, 1);

    int dx = distrib(gen);
    int dy = distrib(gen);
    int dz;
    if (dimensions == 3) {
        dz = distrib(gen);
    }

    this->position[0] += dx / lattice_scale;
    this->position[1] += dy / lattice_scale;
    if (this->dimensions == 3){
        this->position[2] += dz / lattice_scale;
    }
    // Need to impose periodic boundary conditions
    // on the position vector.
    static_cast<double>(rand() % x_length);
    static_cast<double>(rand() % y_length);
    static_cast<double>(rand() % z_length);

    this->position[0] = fmod(this->position[0], this->x_length);
    this->position[1] = fmod(this->position[1], this->y_length);
    if (this->dimensions == 3){
        this->position[2] = fmod(this->position[2], this->z_length);
    }

    // _grow();
}

Nodule::~Nodule() {
    // delete[] position;
}