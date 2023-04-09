from NoduleField import NoduleField
from utils import make_histogram, make_nodule_plot, delete_files


X_LENGTH = 500
Y_LENGTH = 500
Z_LENGTH = 200

LATTICE_SCALE = 1
DISTANCE_EPSILON = 0.1


def main():

    delete_files('gif_folder')
    delete_files('histograms')
    # This effectively defines a short range attractive force
    # between two nodules.

    # first, we must generate a field of objects,
    # by randomly assigning each object a position and radius
    NUM_NODULES = 300

    nodule_field = NoduleField(num_nodules=NUM_NODULES,
                               x_length=X_LENGTH,
                               y_length=Y_LENGTH,
                               z_length=Z_LENGTH,
                               lattice_scale=LATTICE_SCALE,
                               distance_epsilon=DISTANCE_EPSILON)

    # Now we need to iterate through the nodules,
    # and check for collisions.
    for t in range(50):
        nodule_field.simulate(1)

        print(len(nodule_field.nodules))

        # if t % 10 == 0:
        make_nodule_plot(nodule_field.nodules, t, X_LENGTH, Y_LENGTH)
        make_histogram(nodule_field.nodules, save_num=t, scale=(
            nodule_field.nodules[0].growth_rate)**t)

        if len(nodule_field.nodules) <= 1:
            break


if __name__ == "__main__":

    # import pstats
    # profiler = cProfile.Profile()
    # profiler.enable()
    main()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('tottime')
    # stats.print_stats()

    # profiler.dump_stats('profile.prof')

    # main()
