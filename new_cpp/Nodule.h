#ifndef NODULE_H
#define NODULE_H

#include <vector>

class Nodule {
public:
    Nodule(double _growth_rate, double x_length, double y_length, double lattice_scale);

    void _timestep();
    
    // Member variables:
    // Make radius a vector of doubles, there will be multiple circles:
    std::vector <double> radii;
    double* position;
    double lattice_scale;
    double max_movement;

    // Getters:
    double* get_com();
    double get_radius();
    double get_area();
    
    // Setters:
    void set_position(double x, double y);
    void set_radius(double radius);

    double modrem(double a, double N);

    virtual ~Nodule();


private:

    void _grow();

    double _growth_rate;
    double x_length;
    double y_length;
    int dimensions = 2;
};

#endif // NODULE_H
