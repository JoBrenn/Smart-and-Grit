import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib import colors
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import json
import sys


def load_JSON_output(filename: str) -> list:
    """ Returns JSON data as a list
        pre: takes a filename argument as a string
        post: returns a list containing JSON objects as dictionaries"""
    with open(filename, "r") as f:
        return json.load(f)

def load_icon(path: str, zoom: float):
    file = path
    image = mpimg.imread(file)
    return OffsetImage(image, zoom = zoom)

def plot_output(data: list, alg_method: str = "", district_number: int = 0, plot_title: str = "Graph"):
    """ Plots and shows a grid containing the houses, batteries and cables
        pre: takes an output list as an argument that, from the second element onwards,
             contains battery dictinaries containing a list of house dictionaries, which in turn
             have a list of cable coordinates
        post: draws a figure on screen through matplotlib where they markers represent houses
              and batteries while the cables are shown as solid lines"""
    fig, ax = plt.subplots()
    plt.title(plot_title)
    # colors = ["red","green","blue","orange", "aquamarine"]
    # colors = ["salmon","tomato","darksalmon","coral", "orangered"]
    colors = ["dodgerblue","navy","aquamarine","mediumpurple", "violet"]

    # Sources:
    # https://matplotlib.org/3.5.0/tutorials/introductory/images.html
    # https://towardsdatascience.com/how-to-add-an-image-to-a-matplotlib-plot-in-python-76098becaf53
    house_imagebox = load_icon("images/house.png", 0.10)
    battery_imagebox = load_icon("images/battery.png", 0.03)

    cables = []

    # Loops over each battery
    for grid_index, battery in enumerate(data[1:]):
        index = data.index(battery)
        color = colors[grid_index - 1]
        # Gets battery location and displays it as a green mark
        bat_loc = battery['location'].split(",")
        bat_x = int(bat_loc[0])
        bat_y = int(bat_loc[1])
        ab = AnnotationBbox(battery_imagebox, (bat_x, bat_y), frameon = False, zorder=3, label="Battery")
        ax.add_artist(ab)

        # battery_marker, = plt.plot(int(bat_loc[0]), int(bat_loc[1]),\
        #                            marker="o", markersize=8, \
        #                            markeredgecolor="green", \
        #                            markerfacecolor="green", \
        #                            zorder=2)

        # Loops over each house of the battery
        if len(battery['houses']):
            for house in battery['houses']:
                # Gets house location and displays it as a red mark
                house_loc = house['location'].split(",")
                house_x = int(house_loc[0])
                house_y = int(house_loc[1])
                ab = AnnotationBbox(house_imagebox, (house_x, house_y), frameon = False, zorder=2)
                ax.add_artist(ab)


                # house_marker, = plt.plot(int(house_loc[0]), int(house_loc[1]),\
                #                          marker="o", markersize=4, \
                #                          markeredgecolor="red", \
                #                          markerfacecolor="red", \
                #                          zorder=2)

                # Loops over each cable segment of the house
                for cable in range(len(house['cables']) - 1):
                    # Gets location of a cable point and its destination point
                    cable1_loc = house['cables'][cable].split(",")
                    cable2_loc = house['cables'][cable + 1].split(",")

                    x_coords = int(cable1_loc[0]), int(cable2_loc[0])
                    y_coords = int(cable1_loc[1]), int(cable2_loc[1])
                    # cables.extend([x_coords, y_coords, color])

                    plt.plot(x_coords, y_coords,
                             color, lw=2,
                             label=f"Grid {grid_index + 1}",
                             zorder=1
                             )

                    # Plots a line from the first cable point to its destination point
                    # plt.plot([int(cable1_loc[0]),int(cable2_loc[0])], \
                    #          [int(cable1_loc[1]),int(cable2_loc[1])], \
                    #          color, lw=2, label="0",\
                    #          zorder=1)
                # plt.plot(*cables, zorder=1, label=f"Grid {grid_index}")

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

    handles, labels = ax.get_legend_handles_labels()
    newLabels, newHandles = [], []
    for handle, label in zip(handles, labels):
        if label not in newLabels:
            newLabels.append(label)
            newHandles.append(handle)

    leg = plt.legend(newHandles, newLabels, fancybox=True, shadow=True, bbox_to_anchor=(1.05, 1.0), loc='upper left')

    # print(plt.gca())

    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for handle in leg.get_lines():
        handle.set_picker(pickradius)


    # for legend_line, ax_line in zip(leg.get_lines(), handles):
    #     legend_line.set_picker(pickradius)  # Enable picking on the legend line.
    #     if legend_line in map_legend_to_ax:
    #         map_legend_to_ax[legend_line].append(ax_line)
    #     else:
    #         map_legend_to_ax[legend_line] = [ax_line]

    fig.canvas.mpl_connect('pick_event', on_pick)
    fig.canvas.mpl_connect('key_press_event', on_press)

    plt.tight_layout()

    if district_number:
        file_path = f"output/figures/{alg_method[2:]}-district_{district_number}.png"
        plt.savefig(file_path, bbox_inches='tight')

    plt.show()

def plot_output_histogram(outputs: list[int], alg_method: str, runs: int, district_number: int) -> None:
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
    file_path = f"output/histograms/{alg_method[2:]}_{runs}-district_{district_number}-histogram.png"
    plt.savefig(file_path, bbox_inches='tight')

    # Show the plot
    plt.show()

def on_pick(event):
    selected_legend = event.artist
    grid_number = selected_legend.get_label()
    fig, ax = plt.gcf(), plt.gca()

    handles, labels = ax.get_legend_handles_labels()

    map_legend_to_ax = {}

    for legend_line, ax_line in zip(labels, handles):
        if legend_line in map_legend_to_ax:
            map_legend_to_ax[legend_line].append(ax_line)
        else:
            map_legend_to_ax[legend_line] = [ax_line]

    # Do nothing if the source of the event is not a legend line.
    if grid_number not in map_legend_to_ax:
        return

    ax_line_list = map_legend_to_ax[grid_number]
    for ax_line in ax_line_list:
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
    # Change the alpha on the line in the legend, so we can see what lines
    # have been toggled.
    selected_legend.set_alpha(1.0 if visible else 0.2)
    fig.canvas.draw()

def on_press(event):
    print('press', event.key)
    sys.stdout.flush()

    if not 0 <= int(event.key) <= 5:
        return

    selected_grid = "Grid " + event.key
    fig, ax = plt.gcf(), plt.gca()
    legend_lines = ax.get_legend().get_lines()
    selected_legend = legend_lines[int(event.key) - 1]

    handles, labels = ax.get_legend_handles_labels()

    map_legend_to_ax = {}

    for legend_line, ax_line in zip(labels, handles):
        if legend_line in map_legend_to_ax:
            map_legend_to_ax[legend_line].append(ax_line)
        else:
            map_legend_to_ax[legend_line] = [ax_line]


    # Do nothing if the source of the event is not a legend line.
    if selected_grid not in map_legend_to_ax:
        return

    ax_line_list = map_legend_to_ax[selected_grid]
    for ax_line in ax_line_list:
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
    # Change the alpha on the line in the legend, so we can see what lines
    # have been toggled.

    selected_legend.set_alpha(1.0 if visible else 0.2)
    fig.canvas.draw()



if __name__ == "__main__":
    #Loads JSON whose path is specified as the first command line argument
    if len(sys.argv) == 2:
        json_data = load_JSON_output(sys.argv[1])
        plot_output(json_data)
    else:
        print("Usage: python3 visualize_output.py filename.json")
