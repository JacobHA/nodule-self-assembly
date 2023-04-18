"""
For epsilon in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
Input epsilon value into ./program and run it.
Gather mean radius over time and store it.
Plot mean radius over time for each epsilon value.
"""

import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt

from csv_to_npy import convert_csv_to_nparray

NUM_SAMPLES = 10


def run_program(epsilon):
    # Run program
    subprocess.call(["./program", str(epsilon)])
    return


def epsilon_run(epsilon):
    run_program(epsilon)
    # Gather data from data/ folder
    files = os.listdir("data/")
    # Sort files by time
    files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))
    # Get mean radius over time
    mean_radius = []
    for file in files:
        data = convert_csv_to_nparray("data/" + file)
        mean_radius.append(np.mean(data[:, 2]))
    return mean_radius


def main():
    epsilons = np.logspace(-3, 1, 30, base=10)
    for epsilon in epsilons:
        avg_radius = np.empty((NUM_SAMPLES, 100), dtype=float)
        for sample in range(NUM_SAMPLES):
            avg_radius[sample] = epsilon_run(epsilon)

        # Plot mean radius over time
        mean_over_samples = np.mean(avg_radius, axis=0)
        plt.plot(mean_over_samples, label=fr"$\epsilon = {epsilon}$")
        # Add a shaded region for standard deviation
        std_over_samples = np.std(avg_radius, axis=0)
        plt.fill_between(
            np.arange(100),
            mean_over_samples - std_over_samples,
            mean_over_samples + std_over_samples,
            alpha=0.3,
        )

    # plt.plot(avg_radius, label=r"$\epsilon = {epsilon}$")
    plt.xlabel("Time")
    plt.ylabel("Mean Radius")
    plt.title("Growth Rate for Different Epsilon Values")
    plt.legend()
    plt.savefig("eps_expt.png")

    return


if __name__ == "__main__":
    main()
