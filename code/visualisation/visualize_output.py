import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import mplcursors


def load_JSON_output(filename: str) -> list:
    """ Returns JSON data as a list
        pre: takes a filename argument as a string
        post: returns a list containing JSON objects as dictionaries"""
    with open(filename, "r") as f:
        return json.load(f)

def plot_output(data: list, plot_title: str = "Graph"):
    """ Plots and shows a grid containing the houses, batteries and cables
        pre: takes an output list as an argument that, from the second element onwards,
             contains battery dictinaries containing a list of house dictionaries, which in turn
             have a list of cable coordinates
        post: draws a figure on screen through matplotlib where they markers represent houses
              and batteries while the cables are shown as solid lines"""
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.title(plot_title)
    colors = ["b", "k", "c", "m", "g"]

    # Loops over each battery
    for battery in data[1:]:
        index = data.index(battery)
        color = colors[index - 1]
        # Gets battery location and displays it as a green mark
        bat_loc = battery['location'].split(",")
        battery_marker, = plt.plot(int(bat_loc[0]), int(bat_loc[1]),\
                                   marker="o", markersize=8, \
                                   markeredgecolor="green", \
                                   markerfacecolor="green", \
                                   zorder=2)

        # Loops over each house of the battery
        if len(battery['houses']) != 0:
            for house in battery['houses']:
                # Gets house location and displays it as a red mark
                house_loc = house['location'].split(",")
                house_marker, = plt.plot(int(house_loc[0]), int(house_loc[1]),\
                                         marker="o", markersize=4, \
                                         markeredgecolor="red", \
                                         markerfacecolor="red", \
                                         zorder=2)

                # Loops over each cable segment of the house
                for cable in range(len(house['cables']) - 1):
                    # Gets location of a cable point and its destination point
                    cable1_loc = house['cables'][cable].split(",")
                    cable2_loc = house['cables'][cable + 1].split(",")

                    # Plots a line from the first cable point to its destination point
                    plt.plot([int(cable1_loc[0]),int(cable2_loc[0])], \
                             [int(cable1_loc[1]),int(cable2_loc[1])], \
                             color + '-', lw=1, \
                             zorder=1, \
                             highlight=True)

    # Grid code snippet obtained from:
    # https://stackoverflow.com/questions/24943991/change-grid-interval-and-specify-tick-labels

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

    plt.legend([battery_marker, house_marker], ["Battery", "House"], bbox_to_anchor=(1.05, 1.0), \
               loc='upper left')
    #ax.legend([house_marker], ["House"])
    plt.tight_layout()



    plt.show()

if __name__ == "__main__":
    #Loads JSON whose path is specified as the first command line argument
    if len(sys.argv) == 2:
        json_data = load_JSON_output(sys.argv[1])
        plot_output(json_data)
    else:
        print("Usage: python3 visualize_output.py filename.json")
