#ifndef NODULEFIELD_H
#define NODULEFIELD_H

#include <vector>
#include <cmath>
#include <cstdlib>
#include "nodule.h"

class NoduleField {
public:
    NoduleField(int dimensions, int num_nodules, int x_length, int y_length, int z_length, int lattice_scale, double distance_epsilon, bool write_to_file=false, double growth_rate=0.0001);
    std::vector<Nodule> nodules_;
    void simulate(int num_timesteps);
    int get_num_nodules() const;
private:
    int dimensions;
    int num_nodules;
    int x_length;
    int y_length;
    int z_length;
    int lattice_scale;
    int timestep_;
    double distance_epsilon;
    bool write_to_file;
    double growth_rate;

    std::vector<int> removable_nodule_indices_;
    
    bool _check_collision(Nodule nodule1, Nodule nodule2);
    void _resolve_collision(Nodule& nodule1, Nodule& nodule2, int idx2);
    void _destroy_nodules(std::vector<int>& indx_list);
    void _garbage_collect_nodule(int idx);
    void absorb_collisions();
    void _timestep();
    void _write_nodules_to_file(const std::string& filename) const;
};

#endif //NODULEFIELD_H
