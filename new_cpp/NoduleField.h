#ifndef NODULEFIELD_H
#define NODULEFIELD_H

#include <vector>
#include <cmath>
#include <cstdlib>
#include "Nodule.h"

class NoduleField {
public:
    NoduleField(int num_nodules, 
                double x_length, 
                double y_length, 
                double lattice_scale, 
                double distance_epsilon, 
                bool write_to_file=false, 
                double growth_rate=0.000,
                bool verbose=false);

    std::vector<Nodule> nodules_;
    void simulate(int num_timesteps);

    // Getters
    int get_num_nodules() const { return nodules_.size(); }

private:
    int dimensions = 2;
    int num_nodules;
    double x_length;
    double y_length;
    double lattice_scale;
    int timestep_ = 0;
    double distance_epsilon;
    bool write_to_file;
    double growth_rate;
    bool verbose;

    std::vector<int> removable_nodule_indices_;
    
    bool _check_collision(Nodule nodule1, Nodule nodule2);
    void _resolve_collision(Nodule& nodule1, Nodule& nodule2, int idx2);
    void _destroy_nodules(std::vector<int>& indx_list);
    void _garbage_collect_nodule(int idx);
    void _absorb_collisions();
    void _timestep();
    void _write_nodules_to_file(const std::string& filename) const;
};

#endif //NODULEFIELD_H
