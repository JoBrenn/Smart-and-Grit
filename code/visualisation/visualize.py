""" Code to vizualize the output of algorithms.

File: vizualize.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 10/01/24 (19/01/24)

Description:   Depending on input gives a vizualization of data.

Usage:  python3 main.py --load [file]
    Note: file should be in output/JSON
"""
import json
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def load_JSON_output(filename: str) -> list:
    """ Returns JSON data as a list
        pre: takes a filename argument as a string
        post: returns a list containing JSON objects as dictionaries"""
    with open(filename, "r") as f:
        return json.load(f)

def load_icon(path: str, zoom: float):
    """ Load an icon for batteries or houses."""
    file = path
    image = mpimg.imread(file)
    return OffsetImage(image, zoom = zoom)

def location_to_artist(location: str, imagebox, order: int = 1) -> AnnotationBbox:
    """ Create a figure box for either batteries or houses.
    This box is placed on x and y coordinates and thus can be plotted."""
    loc_coords = location.split(",")
    x = int(loc_coords[0])
    y = int(loc_coords[1])
    return AnnotationBbox(imagebox, (x, y), frameon = False, zorder=order, label="Battery")

def plot_cables(plt, cables: list[str], grid_index: int, color: str) -> None:
    """ Plot cables corresponding to house.
    Two point coordinates are defined and a line is drawn between them.
    """
    for cable in range(len(cables) - 1):
        # Gets location of a cable point and its destination point
        cable1_loc = cables[cable].split(",")
        cable2_loc = cables[cable + 1].split(",")

        x_coords = int(cable1_loc[0]), int(cable2_loc[0])
        y_coords = int(cable1_loc[1]), int(cable2_loc[1])

        plt.plot(x_coords, y_coords, color, lw=2,
                 label=f"Grid {grid_index + 1}", zorder=1
                 )

def deduplicate_legend_items(handles, labels):
    """Find one unique handle for duplicate labels.
    Labels (['Grid 1', 'Grid 2', ...]) correspond to one battery.
    """
    newLabels, newHandles = [], []
    for handle, label in zip(handles, labels):
        if label not in newLabels:
            newLabels.append(label)
            newHandles.append(handle)
    return newLabels, newHandles

def plot_output(data: list, alg_method: str = "", district_number: int = 0, plot_title: str = "Graph"):
    """ Plots and shows a grid containing the houses, batteries and cables
        pre: takes an output list as an argument that, from the second element onwards,
             contains battery dictinaries containing a list of house dictionaries, which in turn
             have a list of cable coordinates
        post: draws a figure on screen through matplotlib where they markers represent houses
              and batteries while the cables are shown as solid lines"""
    # Create figure and give title
    fig, ax = plt.subplots()
    plt.title(plot_title)

    # Define colors used in figure
    colors = ["dodgerblue","navy","aquamarine","mediumpurple", "violet"]

    # Sources:
    # https://matplotlib.org/3.5.0/tutorials/introductory/images.html
    # https://towardsdatascience.com/how-to-add-an-image-to-a-matplotlib-plot-in-python-76098becaf53
    house_imagebox = load_icon("images/house.png", 0.10)
    battery_imagebox = load_icon("images/battery.png", 0.03)

    # Loops over each battery
    for grid_index, battery in enumerate(data[1:]):
        # Select color for cables of current battery
        color = colors[grid_index]

        # Add battery icons
        ax.add_artist(location_to_artist(battery['location'], battery_imagebox, order=3))

        # Loops over each house of the battery
        if battery['houses']:
            for house in battery['houses']:
                # Add house icons
                ax.add_artist(location_to_artist(house['location'], house_imagebox, order=2))

                # Plot cables connect to current house
                plot_cables(plt, house['cables'], grid_index, color)

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

    # Extract all elements with labels (cables) and select one per battery
    handles, labels = ax.get_legend_handles_labels()
    unqLabels, unqHandles = deduplicate_legend_items(handles, labels)

    # Plot legend, located outside graph
    leg = plt.legend(unqHandles, unqLabels, fancybox=True, shadow=True,
                     bbox_to_anchor=(1.05, 1.0), loc='upper left', title='District Legend')

    # Points (Pt). How close the click needs to be to trigger an event.
    pickradius = 5

    # Make legend lines clickable
    for handle in leg.get_lines():
        handle.set_picker(pickradius)

    # Define interaction events
    fig.canvas.mpl_connect('pick_event', on_pick)
    fig.canvas.mpl_connect('key_press_event', on_press)

    # Tight plot for better look
    plt.tight_layout()

    # Save figure if district number is defined
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
    """Reverse visibility of cables from grid.
    Grid number corresponds to legend line clicked.
    Usage: Click legend line to toggle visibility
    """
    # Get selected line in legend
    selected_legend = event.artist
    grid_number = selected_legend.get_label()

    # Get current figure and axes
    fig, ax = plt.gcf(), plt.gca()

    # Get all elements with labels
    handles, labels = ax.get_legend_handles_labels()

    map_legend_to_ax = {}

    # Create dict with grid-cables pairs
    for legend_line, ax_line in zip(labels, handles):
        if legend_line in map_legend_to_ax:
            map_legend_to_ax[legend_line].append(ax_line)
        else:
            map_legend_to_ax[legend_line] = [ax_line]

    # Do nothing if the source of the event is not a legend line.
    if grid_number not in map_legend_to_ax:
        return

    # Reverse visibility of selected grid cables
    ax_line_list = map_legend_to_ax[selected_grid]
    for ax_line in ax_line_list:
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)

    # Change the alpha on the line in the legend, so we can see what lines
    # have been toggled.
    selected_legend.set_alpha(1.0 if visible else 0.2)

    # Draw updated figure
    fig.canvas.draw()

def on_press(event):
    """Reverse visibility of cables from grid.
    Grid number corresponds to key pressed.
    Usage: Press 1 to 5 to toggle visibility
    """
    if not 0 <= int(event.key) <= 5:
        return

    # Select the key Grid
    selected_grid = "Grid " + event.key

    # Get current figure and axes
    fig, ax = plt.gcf(), plt.gca()

    # Get lines in legend and select the one corresponding with key pressed
    legend_lines = ax.get_legend().get_lines()
    selected_legend = legend_lines[int(event.key) - 1]

    # Get all elements with labels
    handles, labels = ax.get_legend_handles_labels()

    map_legend_to_ax = {}

    # Create dict with grid-cables pairs
    for legend_line, ax_line in zip(labels, handles):
        if legend_line in map_legend_to_ax:
            map_legend_to_ax[legend_line].append(ax_line)
        else:
            map_legend_to_ax[legend_line] = [ax_line]


    # Do nothing if the source of the event is not a legend line.
    if selected_grid not in map_legend_to_ax:
        return

    # Reverse visibility of selected grid cables
    ax_line_list = map_legend_to_ax[selected_grid]
    for ax_line in ax_line_list:
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)

    # Change the alpha on the line in the legend, so we can see what lines
    # have been toggled.
    selected_legend.set_alpha(1.0 if visible else 0.2)

    # Draw updated figure
    fig.canvas.draw()



if __name__ == "__main__":
    #Loads JSON whose path is specified as the first command line argument
    if len(sys.argv) == 2:
        json_data = load_JSON_output(sys.argv[1])
        plot_output(json_data)
    else:
        print("Usage: python3 visualize_output.py filename.json")
