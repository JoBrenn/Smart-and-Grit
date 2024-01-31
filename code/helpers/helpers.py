""" File with helper functions.

File: helpers.py

Authors:    Jonas Brenninkmeijer
            Kathy Molenaar

Date: 16/01/24 (31/01/24)

Description:
Different helper functions, mainly used in main.py

Functions:
    load_JSON_output        (-> list): Load JSON data from .json file in output/JSON/
    write_data_to_JSON:     (-> None): Write data to .json file in output/JSON/
    print_dictkeys:         (-> None): Print keys in dictionary
    print_possibilities:    (-> None): Print filenames in output/JSON/
    print_helpmsg_methods:  (-> None): Print possible methods
    get_beam_input:         (-> int): Get user input for beam
    get_max_runs_input:     (-> int): Get user input for maximum runs
    get_max_depth_input:    (-> int): Get user input for maximum depth
    get_method_input:       (-> str): Get user input for method
    get_file_input:         (-> str): Get user input for file
    get_runs_input:         (-> int): Get user input for runs
    get_dictkey_input:      (-> str): Get user input for dictionary key
    get_district_input:     (-> int): Get user input for district
    load_method:            (-> list): Load data from output/JSON/ correctly
    combine_method:         (-> list): Combine cables from valid output more efficiently
    run_general_method:     (-> list): Run general method (load, format, combine)
    run_algo_method:        (-> list): Run algorithm (randrwalk, randmanh, randmanhcap, greedmanh,
                                                    greedmanhcap, closest, depthfirst, breadthfirst,
                                                    hillclimber, simulatedannealing, beamsearch.)
    plot_data:              (-> None): Plot generated data to grid or histogram

Usage:  import code.helpers.helpers as hlp
"""
# General packages imported
from os import listdir, walk
from os.path import isdir
from json import load, dump
from time import time
from copy import deepcopy
from halo import Halo

# Visualisation imported
from code.visualisation.visualize import plot_output, plot_output_histogram

# Run methods imported
from code.algorithms.run import run_greedy_assignment_shortest_walk, \
    run_random_assignment_with_capacity, \
    run_random_assignment

# Algorithms inmported
from code.algorithms.hill_climber import HillClimber
from code.algorithms.beam_search import BeamSearch
from code.algorithms.simulatedannealing import Simulatedannealing
from code.algorithms.closest import Closest
from code.algorithms.depth_first import DepthFirst
from code.algorithms.breadth_first import BreadthFirst
from code.algorithms.combine_cables import run as combine

# District module imported
from code.modules.district import District

from experiments.beamsearch.beamsearch_script import BeamSearchTuning
from experiments.hillclimber.hill_climb_experiment import run_hillclimber_experiments
from experiments.simulatedannealing.simulatedannealing_experiment import run_simulatedannealing_experiments
from experiments.timed.time_scripts import run_time_script


def load_JSON_output(filename: str) -> list:
    """ Return JSON data as a list
        Params:
            filename    (str): filename
        Returns:
            (list) list of json file data
    """

    with open(filename, "r") as f:
        return load(f)


def write_data_to_JSON(data: list, file_name: str,
                       district_number: int, runs: int) -> None:
    """ Write data list to output JSON file in output/
        Params:
            data            (list):data list
            file_name       (str): filename to which data is written
            district_number (int): district number
            runs            (int): number of runs of data
        Returns:
            (list) list of json file data
    """

    # Craft file path
    file_path = f"output/JSON/{file_name}\
-district_{district_number}-runs_{runs}-output.json"

    # Open file path in WRITE mode and write data
    with open(file_path, "w") as outfile:
        dump(data, outfile, indent=4)


def print_helpmsg_methods():
    """ Print help messages methods
        Returns:
            none
            prints help messages
    """
    # General methods: help, load, format and exit
    # \u001b[32m gives color GREEN in terminal
    print("\n\u001b[32mGeneral Methods:\u001b[0m")
    print("  help:\t\t Display help manual")
    print("  load:\t\t Load a JSON file from output/JSON")
    print("  format:\t Display formatted output")
    print("  exit:\t\t Stop running main.(Useable at every input.)\n")

    # Algorithm methods: randrwalk, randmanh, randmanhcap, greedmanh,
    # greedmanhcap, closest, depthfirst, breadthfirst, hillclimber,
    # simulatedannealing, beamsearch.
    print("\n\u001b[32mAlgorithms Methods:\u001b[0m")
    print("  randrwalk:\t Randomly assigns houses to batteries. " + \
                        "Creates cable path through randomly taking random steps until destination is reached.")
    print("  randmanh:\t Randomly assigns houses to batteries. \t\t\t\t\t\t\t\t\t(Manhattan Distance)")
    print("  greedmanh:\t Uses greedy algorithm to assign houses to batteries. \t\t\t\t\t\t\t(Manhattan Distance)")
    print("  greedmanhcap:\t Uses greedy algorithm to assign houses to capped batteries. \t\t\t\t\t\t(Manhattan Distance) ")
    print("  closest:\t Assigns a house to its closest battery that has capacity left \t\t\t\t\t\t(Manhattan Distance) ")
    print("  depthfirst:\t Assigns houses using a depth first algorithm until the set depth is reached \t\t\t\t(Manhattan Distance)")
    print("  breadthfirst:\t Assigns houses using a breadth first algorithm until the set depth is reached \t\t\t\t(Manhattan Distance)")
    print("  hillclimber:\t Uses hillclimber algorithm to assign houses to capped\
batteries. \t\t\t\t\t(Manhattan Distance) ")
    print("  simulatedannealing:\t Uses simulated annealing algorithm to assign\
houses to capped batteries. \t\t\t(Manhattan Distance) ")
    print("  beamsearch:\t Searches state space breadth first with a width (beam).\
N (beam) states are kept at every iteration.\t(Manhattan Distance) ")

def print_possibilities(possibilities: list[str]) -> None:
    """ Print possible files from output/JSON/"""
    print("\n\u001b[32mPossible Load Files:\u001b[0m")
    for index, file in enumerate(possibilities):
        print(f"{index+1}.  {file}")

def print_dictkeys(min_dictkey: int, max_dictkey) -> None:
    """ Print dictionary keys from Beam Search .json output """
    print(f"\n\u001b[32mPossible DictKeys: \u001b[0m {min_dictkey} - {max_dictkey}")


def get_method_input() -> str:
    """ Get input for method.
    Asks the user to input one of the methods.
    General Methods:
        format:                 A format of the district.
        load:                   Load a figure of a JSON file.
        combine:                Combine the cables from a JSON file.
    Algorithm Methods:
        randmanh:               Randomly chooses a house and connects it to battery with Manhattan Distance (NO CAPACITY constraint)
        randmanhcap:            Randomly chooses a house and connects it to battery with free capacity with Manhattan Distance
        greedmanh:              Random house is assigned to battery with most capacity.
        hillclimber:            Iteration algorithm where 'steps' are taken and positive steps are accepted.
        beamsearch:             Creates states from randomly starting houses at prunes according to defined beam
        simulatedannealing:     Similar to hillclimber, but with a chance that a negative step is accepted according to temperature.
        closest:                Random house is connected to closest battery with capacity
        depthfirst:             State space is searched, going into a state full depth first.
        breadthfirst:           State space is searched, going over states full breadth first.
    """
    method = ""
    # Keep asking user for valid input
    while not method:
        # Get method in lowercase
        method = input("\u001b[33mMethod:\u001b[0m ").lower()
        if method == "exit":
            print("\nExiting main.\n")
            exit()
        # User asked for help
        elif method in {"help", "--help"}:
            print_helpmsg_methods()
            method = ""
        # Check if user selected valid method
        elif method not in {"format", "load", "combine", "randmanh", "randmanhcap",
                            "greedmanh", "hillclimber", "beamsearch", "simulatedannealing",
                            "closest", "depthfirst", "breadthfirst", "experiment"}:
            print("\nInvalid method. Type","\u001b[32mhelp\u001b[0m", "to see possibilities.\n")
            method = ""

    return method

def get_district_input() -> int:
    """ Get input for district.
    A district between 1 and 3 can be chosen.
    Data can be found in data/"""
    district = 0
    # Keep asking user for valid input
    while not district:
        district = input("\n\u001b[33mDistrict Number:\u001b[0m ")
        if district == "exit":
            print("\nExiting main.\n")
            exit()
        # Check if district is numeric and between 1 and 3
        elif not district.isnumeric() or not 1 <= int(district) <= 3:
            print("\nChoose a district between 1 and 3.")
            district = 0
    return int(district)

def get_runs_input() -> int:
    """ Get input for amount of runs."""
    runs = 0
    # Keep asking user for valid input
    while not runs:
        runs = input("\n\u001b[33mRuns:\u001b[0m ")
        if runs == "exit":
            print("\nExiting main.\n")
            exit()
        # Check if runs numeric and >0
        elif not runs.isnumeric() or int(runs) < 1:
            print("\nPlease choose 1 or more runs.")
            runs = 0

    return int(runs)

def get_beam_input():
    """ Get input for beam for Beam Search.
    Beam defines how many states are saved after every iteration.
    Code for Beam Search can be found in code/algorithms/beam_search.py"""
    beam = 0
    # Keep asking user for valid input
    while not beam:
        beam = input("\n\u001b[33mBeam:\u001b[0m ")
        if beam == "exit":
            print("\nExiting main.\n")
            exit()
        # Check if beam is numeric and >0
        elif not beam.isnumeric() or int(beam) < 1:
            print("\nPlease choose a beam of 1 or higher.")
            beam = 0
    return int(beam)

def get_max_runs_input():
    """ Get input for maximum runs."""
    runs = 0
    while not runs and runs != "":
        runs = input("\n\u001b[33mMax runs:\u001b[0m ")
        if runs == "exit":
            print("\nExiting main.\n")
            exit()
        elif runs == "":
            runs = 10
            print("\nMax runs are set at a default of 10")
        elif not runs.isnumeric() or int(runs) < 1:
            print("\nPlease choose a max amount of runs")
            runs = 0
    return int(runs)

def get_max_depth_input(house_count: int) -> int:
    """ Get input for maximum depth for Depth First Search."""
    depth = 0
    while not depth:
        depth = input("\n\u001b[33mMax depth:\u001b[0m ")
        if depth == "exit":
            print("\nExiting main.\n")
            exit()
        elif not depth:
            depth = 4
            print("\nMax depth are set at a default of 4")
        elif int(depth) > house_count:
            print(f"\nDepth exceeds the amount of houses in district ({house_count})")
        elif not depth.isnumeric() or int(depth) < 1:
            print("\nPlease choose which layer to end at")
            depth = 0
    return int(depth)

def get_dictkey_input(dictkeys: list[int]) -> str:
    """ Get input from user for dictkey.
    Params:
        dictkeys    (list): List of dictkeys, gotten from an output dictionary of BeamSearch
    Returns:
        selected dictkey string
    """
    if dictkeys:
        # Define dictkey and max and min values in dictkeys
        dictkey = 0
        max_dictkey = int(max(dictkeys))
        min_dictkey = int(min(dictkeys))
    else:
        return 0

    # If max and min are
    if max_dictkey == min_dictkey:
        dictkey = str(min_dictkey)

    while not dictkey:
        print_dictkeys(min_dictkey, max_dictkey)
        dictkey = input("\n\u001b[33mSelect dictionary key:\u001b[0m ")
        if not dictkey.isnumeric() or not min_dictkey <= int(dictkey) <= max_dictkey:
            print(f"\nPlease choose a key between {min_dictkey} and {max_dictkey}.")
            dictkey = 0

    return dictkey

def get_file_input(possibilities: list[str]) -> str:
    """ Get input for the desired file to be loaded.
    Files need to be in output/JSON/
    Params:
        possibilities   (list[str]): List with filename in output/JSON/
    Returns:
        filename string
    """
    file = ""

    # Keep asking user
    while not file:
        file = input("\n\u001b[33mFile:\u001b[0m ")

        # Exit
        if file == "exit":
            print("\nExiting main.\n")
            exit()

        # If input is not filenae or index
        if not file in possibilities and not file.isnumeric():
            print("\nPlease choose one of the possibilities.")
            file = ""
        # If input is not index or within range of file indexing
        elif not file.isnumeric() or not 1 <= int(file) <= len(possibilities):
            print("\nPlease choose one of the possibilities.")
            file = ""
    # If index of file was given
    if file.isnumeric():
        return possibilities[int(file) - 1]
    # If filename was given
    else:
        return file

def load_method(json_data: list) -> list:
    """ Select correct way of loading data from .json file
    from output/JSON/ for plotting.
    Params:
        json_data   (list): List with JSON data, loaded from output/JSON/
    Returns:
        list with data from .json
    """
    data = []
    # If JSON data is directly avaliable
    if len(json_data) == 6 and isinstance(json_data, list):
        data.append(json_data)

    # If JSON data is in nested list
    else:
        # Fill data with outcomes
        for outcome in json_data:
            data.append(outcome)

    return data

def combine_method(json_data: list, file: str) -> list:
    """ Combine cables in output/JSON/ .json.
    combine() is tried N (runs) times. combine() comes
    code/algorithms/combine_cables.py.
    Params:
        json_data   (list): List with JSON data, loaded from output/JSON/
        file        (str): File where the JSON came from
    Returns:
        list with data where cables are combined more efficiently.
        prints the amount of dictkeys if dictionary is found.
    """
    # Get input for runs and prepare filename for .json output
    data = []
    runs = get_runs_input()
    filename = file.split(".")[0]

    # Single output is found
    if len(json_data) == 6 and isinstance(json_data, list):
        # Combine cables from output
        data.append(combine(json_data, runs, filename))

    # Dictionary is found
    elif isinstance(json_data, dict):
        # Get dictionary keys and let user choose one
        dictkeys = list(json_data.keys())
        dictkey = get_dictkey_input(dictkeys)

        # Check if any dictkeys were found
        if dictkey:
            # Combine cables from data in chosen key output
            data.append(combine(json_data[dictkey], runs, filename))

    # Nested list is found
    elif len(json_data) == 1 and len(json_data[0]) == 6:
        # Combine cable from output in list
        data.append(combine(json_data[0], runs, filename))

    return data

def get_experiment_input():
    experiment_input = ""
    while not experiment_input:
        experiment_input = input("\n\u001b[33mExperiment Method:\u001b[0m ")
        if experiment_input not in {"beamsearch", "simulatedannealing", "hillclimber", "timed"}:
            print("Please chooses between:")
            print(" beamsearch\n", "simulatedannealing\n", "hillclimber\n", "timed")
            experiment_input = ""

    return experiment_input


def get_algorithm_input():
    algorithm_input = ""
    while not algorithm_input:
        algorithm_input = input("\n\u001b[33mAlgorithm Method:\u001b[0m ")
        if algorithm_input not in {"closest", "beamsearch",\
                                    "hillclimber", "simulated", "depthfirst"}:
            print("Please chooses between:")
            print("closest\n", "beamsearch\n" "hillclimber\n", "simulated\n", "depthfirst\n")
            algorithm_input = ""

    return algorithm_input


def run_experiment(district_number: int):
    selected_experiment = get_experiment_input()
    district = District(district_number, "costs-own")

    if selected_experiment == "beamsearch":
        max_beam = get_beam_input()
        runs = get_runs_input()
        beam = BeamSearchTuning(district_number, runs, max_beam)
        beam.run_tuning()
    elif selected_experiment == "hillclimber":
        run_hillclimber_experiments(district)
    elif selected_experiment == "simulatedannealing":
        run_simulatedannealing_experiments(district)
    elif selected_experiment == "timed":
        selected_algorithm = get_algorithm_input()
        run_time_script(selected_algorithm)


def run_general_method(method: str) -> list:
    """ Run a general method.
    Params:
        method      (str): Algorithm method chosen.
    Returns:
        data, a list of data to be used for plotting and saving.
        prints possibilities for files in output/JSON/
    """
    data = []
    # If format is chosen, load data from format
    if method == "format":
        data.append(load_JSON_output("output/output-format.json"))

    # With load or combine, possibilities are listed
    elif method in {"load", "combine"}:
        # Extract possibilities
        possibilities = sorted(listdir("output/JSON/"))

        # If any files are found
        if possibilities:
            # Print the possibilities
            print_possibilities(possibilities)

            # Ask user to choose one of possibilities
            file = get_file_input(possibilities)

            # Extract JSON data from chosen file
            json_data = load_JSON_output(f"output/JSON/{file}")

            # Run load_method
            if method == "load":
                data = load_method(json_data)

            # Run combine_method
            else:
                data = combine_method(json_data, file)
        else:
            # No files in output/JSON/
            print("No options in output/JSON/. Try running an algorithm first.")

    return data

def run_algo_method(method: str, district_number: int, runs: int) -> list:
    """ Run the specified algorithm method.
    Methods (get_method_input for further reference):
        randmanh:               Random Manhattan Distance
        randmanhcap:            Random Manhattan Distance with capacity
        greedmanh:              Connect to battery with most capacity
        hillclimber:            Take step and accept if improvement
        beamsearch:             Search states, breadth first with beam
        simulatedannealing:     Take step and accept if improvement or deteration within temperature
        closest:                Assign house to closest battery
        depthfirst:             Search states, depth first
        breadthfirst:           Search states, breadth first
    Params:
        method          (str): Algorithm method
        district_number (int): Number of district
        runs            (int): Amount of runs to be done
    Returns:
        data            (list): List with one or more district output (through .return_output())
    """
    # Start time for measuring run time
    start_time = time()

    # Start Halo spinner to give visual indication of running
    spinner = Halo(text='Running method', spinner='dots')
    spinner.start()

    # Initialize data and district
    data = []
    district = District(district_number, "costs-own")

    if method == "randmanh":
        """
        Here we again apply a random assignment of houses to batteries,
        not taking the capacity into account. Instead of a random walk,
        we now implement the shortest Manhattan distance.
        """
        for _ in range(runs):
            district_copy = deepcopy(district)
            data.append(run_random_assignment(district_copy, method))

    elif method == "randmanhcap":
        """
        Here we again apply a random assignment of houses to batteries,
        not taking the capacity into account. Instead of a random walk,
        we now implement the shortest Manhattan distance.
        """
        for _ in range(runs):
            district_copy = deepcopy(district)
            data.append(run_random_assignment_with_capacity(district_copy, method))

    elif method == "greedmanh":
        """
        Here we apply a greedy algorithm. A house is assigned to the battery,
        starting at a random house, with the most capacity left.
        The path of the cable is created using the shortest Manhattan distance
        from the house towards the battery.
        """
        for _ in range(runs):
            district_copy = deepcopy(district)
            data.append(run_greedy_assignment_shortest_walk(district_copy))

    elif method == "hillclimber":
        """
        Here we apply a Hillclimber algorithm. We start with a random configuration
        of house-battery connections by Manhattan distance. We change one house-battery
        connection and check whether this lowers the costs
        until we come across a valid solution to our problem. From there
        we randomly swap two house-battery connections and check whether the solution
        is still valid and the cost is lowered.
        Give integer of number of iterations in command line before indicating district number.
        """
        hillclimb = HillClimber(district)
        data.append(hillclimb.run_hill_climber(district, runs, 1000).return_output())

    elif method == "simulatedannealing":
        simul = Simulatedannealing(district)
        data.append(simul.run_hill_climber(district, runs, 1000).return_output())

    elif method == "beamsearch":
        """
        Beamsearch algorithm. The beam specified is the amount of states saved between
        every iteration. An iteration is where the previous states are replaced by
        new states that have one more connected house. In every state the same randomly
        chosen house is connected to all batteries with enough capacity. A number
        of best states are then kept according to the beam
        """
        # Stop spinner, because interference with input()
        spinner.stop()

        # Get beam input
        beam = get_beam_input()

        # Start spinner again
        spinner.start()

        # Initialize BeamSearch
        beamsearch = BeamSearch(district, beam)
        best_state = beamsearch.run()
        data.append(best_state.return_output())

    elif method == "closest":
        """
        Runs a greedy type algorithm where each house is assigned to the
        battery that closest to the battery, the distance between which
        is calculated through the Manhattan distance. Each run can result in
        an invalid solution, and will be run again until it either finds a
        valid solution or the max_runs has been reached.
        """
        # Stop spinner, because interference with input()
        spinner.stop()

        # Get max runs input
        max_runs = get_max_runs_input()

        # Start spinner again
        spinner.start()

        # Initialize closest
        closest = Closest(district, max_runs)
        best_state = closest.run()
        data.append(best_state.return_output())

    elif method == "depthfirst":
        """
        A depth first algorithm that goes through each state. The max
        depth, or assigned houses, can be given so the amount of states
        can be reduced. The state trees where a battery has its capacity
        exceeded will be pruned as well. A standard district of 150 houses
        and 5 batteries would too long to reasonably complete, so specifying a
        max depth or running a smaller district is advised
        """
        # Stop spinner, because interference with input()
        spinner.stop()

        # Get max runs input
        max_depth = get_max_depth_input(len(district.houses))

        # Start spinner again
        spinner.start()

        # Initialize depth first
        depthfirst = DepthFirst(district, max_depth)
        best_state = depthfirst.run()
        data.append(best_state.return_output())


    elif method == "breadthfirst":
        """
        Works similarly to depth first, but goes through each state, layer by
        layer instead. The runtime of the algorithm with a standard district is
        as long as depthfirst at minimum, so the districts and depth should be
        chosen with similar consideration.
        """
        # Stop spinner, because interference with input()
        spinner.stop()

        # Get max runs input
        max_depth = get_max_depth_input(len(district.houses))

        # Start spinner again
        spinner.start()

        # Initialize breadth first
        breadthfirst = BreadthFirst(district, max_depth)
        best_state = breadthfirst.run()
        data.append(best_state.return_output())

    # Stop spinner
    spinner.stop()

    # End timer and print to terminal
    end_time = time()
    print(f"\n\u001b[32mMethod Time\u001b[0m: {round(end_time - start_time, 5)}")

    return data

def plot_data(data, method: str, runs: int = 1, district_number: str = "Graph") -> None:
    """ Determine how data should be plotted and plot."""
    # Data error, when no data.
    if not data:
        print("Data Error.")
        exit()

    # If data list contains 1 item, plot figure
    elif len(data) == 1:
        plot_output(data[0])

    # If data list contains multiple items, plot histogram
    else:
        # Extract all outcome costs from data
        outcomes = []
        for district in data:
            outcomes.append(district[0]["costs-own"])

        # Plot histogram from outcomes
        plot_output_histogram(outcomes, method, runs, district_number)
