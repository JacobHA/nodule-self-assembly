#include <cmath>
#include <cstdlib>
#include <vector>
#include <random>
#include <cmath>
#include <array>
#include <stdexcept>

#include "Nodule.h"

Nodule::Nodule(double _growth_rate, double x_length, double y_length, double lattice_scale, bool verbose) {
    this->x_length = x_length;
    this->y_length = y_length;
    this->lattice_scale = lattice_scale;
    this->_growth_rate = _growth_rate;
    this->position = new double[dimensions];
    this->radius = 0;
    this->verbose = verbose;
}

void Nodule::set_position(double x, double y) {
    // Assert the new position is within the bounds of the field.
    if (x < 0 || x > this->x_length) {
        throw std::invalid_argument("x must be within the bounds of the field.");
    }
    if (y < 0 || y > this->y_length) {
        throw std::invalid_argument("y must be within the bounds of the field.");
    }
    this->position[0] = x;
    this->position[1] = y;
}

double Nodule::get_area() {
    return M_PI * pow(radius, 2);
}

void Nodule::set_radius(double radius) {
    if (radius <= 0) {
        throw std::invalid_argument("Radius must be positive.");
    }
    this->radius = radius;
}

void Nodule::_grow() {
    double new_radius;
    double new_area = this->_growth_rate * M_PI * pow(this->radius, 2);
    new_radius = sqrt(new_area / M_PI);
    set_radius(new_radius);
}

void Nodule::_timestep() {
    // for each co-ordinate, generate a random, unbiased value
    std::random_device rd;
    std::mt19937 gen(rd());

    // Draw a random angle from a uniform distribution between 0 and 2pi
    std::uniform_real_distribution<> distrib(0, 2*M_PI);
    double theta = distrib(gen);
    // Use this to determine the change in x and y
    // First get the current position:
    double* position = get_position();
    double x_pos = position[0];
    double y_pos = position[1];
    double new_x_pos = x_pos + lattice_scale * cos(theta) / radius;
    double new_y_pos = y_pos + lattice_scale * sin(theta) / radius;

    // Need to impose periodic boundary conditions
    // on the position vector.

    double shift_x_pos = modrem(new_x_pos, x_length);
    double shift_y_pos = modrem(new_y_pos, y_length);

    // Now update the position vector with set_position:
    set_position(shift_x_pos, shift_y_pos);

    // _grow();
}

Nodule::~Nodule() {
    // delete[] position;
}

double Nodule::modrem(double a, double N){
    return a - N * floor(a / N);
}