import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# plt.plot(10, 10, marker="o", markersize=5, markeredgecolor="green", markerfacecolor="green")

# plt.plot([10, 10], [10, 20], 'k-', lw=2)

# Major ticks every 20, minor ticks every 5
major_ticks = np.arange(0, 51, 10)
minor_ticks = np.arange(0, 51, 1)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

with open("./data/district_1/district-1_batteries.csv", "r") as f:
    next(f)
    for line in f:
        x = int(line.split(",")[0].strip("\""))
        y = int(line.split(",")[1].strip("\""))
        plt.plot(x, y, marker="o", markersize=5, markeredgecolor="green", markerfacecolor="green")

with open("./data/district_1/district-1_houses.csv", "r") as f:
    next(f)
    for line in f:
        x = int(line.split(",")[0])
        y = int(line.split(",")[1])
        plt.plot(x, y, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red")

# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)




plt.show()
