import numpy as np
import matplotlib.pyplot as plt
import json
import sys


def load_JSON_output(filename: str) -> dict:
    """ Returns JSON data as a dictionary"""
    with open(filename, "r") as f:
        return json.load(f)

def plot_output(data: list):
    """ Plots and shows a grid containing the houses, batteries and cables"""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Loops over each battery
    for battery in data[1:]:
        # Gets battery location and displays it as a green mark
        bat_loc = battery['location'].split(",")
        plt.plot(int(bat_loc[0]), int(bat_loc[1]), marker="o", markersize=3, markeredgecolor="green", markerfacecolor="green")

        # Loops over each house of the battery
        for house in battery['houses']:
            # Gets house location and displays it as a red mark
            house_loc = house['location'].split(",")
            plt.plot(int(house_loc[0]), int(house_loc[1]), marker="o", markersize=3, markeredgecolor="red", markerfacecolor="red")

            # Loops over each cable segment of the house
            for cable in range(len(house['cables']) - 1):
                # Gets location of a cable point and its destination point
                cable1_loc = house['cables'][cable].split(",")
                cable2_loc = house['cables'][cable + 1].split(",")

                # Plots a line from the first cable point to its destination point
                plt.plot([int(cable1_loc[0]),int(cable2_loc[0])], [int(cable1_loc[1]),int(cable2_loc[1])], 'k-', lw=1)

    # Grid code snippet obtained from https://stackoverflow.com/questions/24943991/change-grid-interval-and-specify-tick-labels
    # Major ticks every 20, minor ticks every 5
    major_ticks = np.arange(0, 51, 10)
    minor_ticks = np.arange(0, 51, 1)

    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)

    # Different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    plt.show()

if __name__ == "__main__":
    #Loads JSON whose path is specified as the first command line argument
    json_data = load_JSON_output(sys.argv[1])
    plot_output(json_data)
