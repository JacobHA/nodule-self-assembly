#ifndef NODULE_H
#define NODULE_H

class Nodule {
public:
    Nodule(int dimensions, double _growth_rate, int x_length, int y_length, int z_length, int lattice_scale);

    void _timestep();
    
    int dimensions;
    double radius;
    double* position;
    double lattice_scale;
    double max_movement;

    // Getters:
    double* get_position() const { return position; }
    double get_radius() const { return radius; }

    // Setters:
    void _update_position(double x, double y, double z);
    void _update_radius(double radius_);

    // Equality comparison operator:
    bool operator==(const Nodule& other) const {
        // Get the position vectors
        double* this_pos = get_position();
        double* other_pos = other.get_position();

        double other_radius = other.radius;
        bool equal_pos;

        // Compare the position vectors and radius for equality
        if (dimensions == 3){
            equal_pos = (this_pos[0] == other_pos[0] &&
                            this_pos[1] == other_pos[1] &&
                            this_pos[2] == other_pos[2]);
        }
        else {
            equal_pos = (this_pos[0] == other_pos[0] &&
                        this_pos[1] == other_pos[1]);
        }
        bool equal_radius = (radius == other_radius);

        // Clean up memory
        delete[] this_pos;
        delete[] other_pos;

        return (equal_pos && equal_radius);
    }
    virtual ~Nodule();


private:

    void _grow();

    double _growth_rate;
    int x_length;
    int y_length;
    int z_length;
};

#endif // NODULE_H
