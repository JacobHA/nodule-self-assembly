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

NUM_SAMPLES = 4


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
    epsilons = np.logspace(-3, 0, 10, base=10)
    growth_rates = []
    for epsilon in epsilons:
        slopes = []
        for sample in range(NUM_SAMPLES):
            growth_data = epsilon_run(epsilon)
            # Calculate the average slope, knowing y-intercept is 0.1:
            slope = np.polyfit(np.arange(100), growth_data, 1)
            slopes.append(slope)
        growth_rates.append(np.mean(slopes))

    plt.plot(epsilons, growth_rates)
    plt.xlabel(r"$\epsilon$")
    plt.ylabel("Mean Growth Rate (Radius/Time)")
    plt.title("Growth Rate for Different Epsilon Values")
    plt.legend()
    plt.savefig("eps_expt_rate.png")
    # Save data to file with np.save
    np.save("eps_expt_rate.npy", np.array(growth_rates))

    return


if __name__ == "__main__":
    main()
