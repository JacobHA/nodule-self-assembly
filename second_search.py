from numpy import random as rnd
import numpy as np
import numba as nb
# from sklearn.neighbors import BallTree
# from joblib import Parallel, delayed
from scipy.spatial import cKDTree


# @nb.jit('(float64[:, ::1], int64[::1], int64[::1], float64)')
def compute(poss, all_neighbours, all_neighbours_sizes, dia_max):
    particle_corsp_overlaps = []
    ends_ind_lst = [np.empty((1, 2), dtype=np.int64)]
    an_offset = 0

    for particle_idx in range(len(poss)):
        cur_point = poss[particle_idx]
        cur_len = all_neighbours_sizes[particle_idx]
        nears_i_ind = all_neighbours[an_offset:an_offset+cur_len]
        an_offset += cur_len
        assert len(nears_i_ind) > 0

        if len(nears_i_ind) <= 1:
            continue

        nears_i_ind = nears_i_ind[nears_i_ind != particle_idx]
        dist_i = np.empty(len(nears_i_ind), dtype=np.float64)

        # Compute the distances
        x1, y1, z1 = poss[particle_idx]
        for i in range(len(nears_i_ind)):
            x2, y2, z2 = poss[nears_i_ind[i]]
            dist_i[i] = np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

        contact_check = dist_i - (radii[nears_i_ind] + radii[particle_idx])
        connected = contact_check[contact_check <= 0]

        particle_corsp_overlaps.append(connected)

        contacts_ind = np.where(contact_check <= 0)
        contacts_sec_ind = nears_i_ind[contacts_ind]
        sphere_olps_ind = np.sort(contacts_sec_ind)

        ends_ind_mod_temp = np.empty((len(sphere_olps_ind), 2), dtype=np.int64)
        for i in range(len(sphere_olps_ind)):
            ends_ind_mod_temp[i, 0] = particle_idx
            ends_ind_mod_temp[i, 1] = sphere_olps_ind[i]

        if particle_idx > 0:
            ends_ind_lst.append(ends_ind_mod_temp)
        else:
            tmp = ends_ind_lst[0]
            tmp[:] = ends_ind_mod_temp[0, :]

    return particle_corsp_overlaps, ends_ind_lst


def ends_gap(poss, dia_max):
    kdtree = cKDTree(poss)
    tmp = kdtree.query_ball_point(poss, r=dia_max, workers=-1)
    all_neighbours = np.concatenate(tmp, dtype=np.int64)
    all_neighbours_sizes = np.array([len(e) for e in tmp], dtype=np.int64)
    particle_corsp_overlaps, ends_ind_lst = compute(
        poss, all_neighbours, all_neighbours_sizes, dia_max)
    ends_ind_org = np.concatenate(ends_ind_lst)
    ends_ind, ends_ind_idx = np.unique(
        np.sort(ends_ind_org), axis=0, return_index=True)
    try:
        gap = np.concatenate(particle_corsp_overlaps)[ends_ind_idx]
    except ValueError or IndexError:
        gap = np.empty(0, dtype=np.float64)
    return gap  # , ends_ind, ends_ind_idx, ends_ind_org


data_volume = 300

radii = rnd.uniform(0.15, 3.42, data_volume)
dia_max = 2 * np.max(radii)

x = rnd.uniform(-1.02, 1.02, (data_volume, 1))
y = rnd.uniform(-3.52, 3.52, (data_volume, 1))
z = rnd.uniform(-1.02, -0.575, (data_volume, 1))
poss = np.hstack((x, y, z))
print(ends_gap(poss, dia_max))
