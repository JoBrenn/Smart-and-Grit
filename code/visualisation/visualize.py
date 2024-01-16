import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import json
import sys


def load_JSON_output(filename: str) -> list:
    """ Returns JSON data as a list
        pre: takes a filename argument as a string
        post: returns a list containing JSON objects as dictionaries"""
    with open(filename, "r") as f:
        return json.load(f)

def plot_output(data: list, alg_method: str, district_number: int, plot_title: str = "Graph"):
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
                             zorder=1)

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

    file_path = f"output/figures/{alg_method[2:]}-district{district_number}.png"

    plt.savefig(file_path, bbox_inches='tight')

    plt.show()

def plot_output_histogram(outputs: list[int], alg_method: str, runs: int) -> None:
    """Plot histogram.
    Given the list of outputs, function creates histogram plot and shows it.
    Additionally, a .png file is of the plot is created in output/histogram.
    Params:
        outputs     (list[int]): List with costs of algorithm runs.
        alg_method  (str): Used algorithm for outputs.
        runs        (int): Amount of runs done.
    Returns:
        None
        .png in output/histogram
        plot shown
    """
    #
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Title includes the method and the number of runs.
    plt.title(f"Histogram: {alg_method[2:]} (n={runs})")
    binwidth = 500
    # The numbers of bins is a range from the mininum value to the maximum value
    # and the step is the binwidth
    n_bins = range(min(outputs), max(outputs) + binwidth, binwidth)

    # Source (l. 95-107): https://matplotlib.org/stable/gallery/statistics/hist.html
    # Empty histogram plot is created
    N, bins, patches = plt.hist(outputs, bins=n_bins)

    # We'll color code by height, but you could use any scalar
    fracs = N / N.max()

    # We need to normalize the data to 0..1 for the full range of the colormap
    norm = colors.Normalize(fracs.min(), fracs.max())

    # Now, we'll loop through our objects and set the color of each accordingly
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    # Mean is calculated and plotted. Label is put in legend.
    mean = round(np.average(outputs))
    plt.axvline(mean, color='k', linestyle='dashed', linewidth=1, label=f'mean: {mean}')

    # Labels and legend are plotted.
    plt.xlabel("Costs")
    plt.ylabel("Count")
    plt.legend()

    # Tight layout for nicer look.
    plt.tight_layout()

    # File path is used to save the plot to output/histogram
    file_path = f"output/histograms/{alg_method[2:]}_{runs}-histogram.png"
    plt.savefig(file_path, bbox_inches='tight')

    # Show the plot
    plt.show()


if __name__ == "__main__":
    #Loads JSON whose path is specified as the first command line argument
    if len(sys.argv) == 2:
        json_data = load_JSON_output(sys.argv[1])
        plot_output(json_data)
    else:
        print("Usage: python3 visualize_output.py filename.json")
