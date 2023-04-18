#ifndef NODULE_H
#define NODULE_H

class Nodule {
public:
    Nodule(double _growth_rate, double x_length, double y_length, double lattice_scale);

    void _timestep();
    
    double radius = 1.0;
    double* position;
    double lattice_scale;
    double max_movement;

    // Getters:
    double* get_position() const { return position; }
    double get_radius() const { return radius; }
    double get_area();
    double get_volume();

    // Setters:
    void set_position(double x, double y);
    void set_radius(double radius);

    // Equality comparison operator:
    bool operator==(const Nodule& other) const {
        // Get the position vectors
        double* this_pos = get_position();
        double* other_pos = other.get_position();

        double this_radius = get_radius();
        double other_radius = other.get_radius();

        // Compare the position vectors and radius for equality
        bool equal_pos = (this_pos[0] == other_pos[0] &&
                        this_pos[1] == other_pos[1]);
        
        bool equal_radius = (radius == other_radius);

        // Clean up memory
        delete[] this_pos;
        delete[] other_pos;

        return (equal_pos && equal_radius);
    }
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
