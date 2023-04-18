"""
Convert the data/ folder to a time series of the mean radius over time.
Also use the standard deviation of the radius for error bars.

Output:
    - mean_radius_over_time.png
"""
import matplotlib.pyplot as plt
from csv_to_npy import convert_csv_to_nparray
import os

# Get the data
folder = 'data'
files = os.listdir(folder)
# Sort the files by time (the number in the file name)
files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

# Get the mean radius over time
mean_radius_over_time = []
std_radius_over_time = []
for file in files:
    np_array = convert_csv_to_nparray(os.path.join(folder, file))
    mean_radius_over_time.append(np_array[:, 2].mean())
    std_radius_over_time.append(np_array[:, 2].std())

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlabel("Time")
ax.set_ylabel("Mean radius")
ax.set_title("Mean radius over time")

# Plot the mean radius over time
plt.errorbar(range(len(mean_radius_over_time)),
             mean_radius_over_time, yerr=std_radius_over_time, fmt='o')
plt.savefig("mean_radius_over_time.png")
