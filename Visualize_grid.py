import numpy as np
import matplotlib.pyplot as plt
import json


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

with open('./data/output-format.json') as f:
    data = json.load(f)

for battery in data[1:]:
    bat_loc = battery['location'].split(",")
    plt.plot(int(bat_loc[0]), int(bat_loc[1]), marker="o", markersize=3, markeredgecolor="green", markerfacecolor="green")

    for house in battery['houses']:
        house_loc = house['location'].split(",")
        plt.plot(int(house_loc[0]), int(house_loc[1]), marker="o", markersize=3, markeredgecolor="red", markerfacecolor="red")
        for cable in range(len(house['cables'])):
            if cable == len(house['cables']) - 1:
                break
            print(cable)    
            cable1_loc = house['cables'][cable].split(",")
            print(cable1_loc)
            cable2_loc = house['cables'][cable + 1].split(",")
            plt.plot(cable1_loc, cable2_loc, 'k-', lw=1)
        


"""
for x in range(5, 10, 1):
    plt.plot(x, 15, marker="o", markersize=3, markeredgecolor="red", markerfacecolor="red")
    
for x in range(0, 5, 1):
    plt.plot(x, 10, marker="o", markersize=3, markeredgecolor="green", markerfacecolor="green")
"""



# Major ticks every 20, minor ticks every 5
major_ticks = np.arange(0, 51, 10)
minor_ticks = np.arange(0, 51, 1)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)


# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)

plt.show()