import json
import os
import copy
import time

from halo import Halo
from code.algorithms.run import *
from code.visualisation.visualize import plot_output
from code.algorithms.hill_climber import HillClimber
from code.algorithms.simulatedannealing import Simulatedannealing
# from code.algorithms.random import *
# from code.algorithms.greedy import *
from code.algorithms.beam_search import BeamSearch



def load_JSON_output(filename: str) -> list:
    """ Returns JSON data as a list
        pre: takes a filename argument as a string
        post: returns a list containing JSON objects as dictionaries"""
    with open(filename, "r") as f:
        return json.load(f)

def write_data_to_JSON(data: list, file_name: str, district_number: int, runs: int) -> None:
    """Write data to output JSON file in output/."""
    # Craft file path
    file_path = f"output/JSON/{file_name}-district_{district_number}-runs_{runs}-output.json"

    # Open file path in WRITE mode and write data
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, indent=4)

def print_helpmsg_methods():
    print("\n\u001b[32mGeneral Methods:\u001b[0m")
    print("  help:\t\t Display help manual")
    print("  load:\t\t Load a JSON file from output/JSON")
    print("  format:\t Display formatted output")
    # print("  histo[gram]:\t Get histogram of N runs of random assignment Manhattan distance algorithm.")
    print("\n\u001b[32mAlgorithms Methods:\u001b[0m")
    print("  randrwalk:\t Randomly assigns houses to batteries. " + \
                        "Creates cable path through randomly taking random steps until destination is reached.")
    print("  randmanh:\t Randomly assigns houses to batteries. \t\t\t\t(Manhattan Distance)")
    print("  greedmanh:\t Uses greedy algorithm to assign houses to batteries. \t\t(Manhattan Distance)")
    print("  greedmanhcap:\t Uses greedy algorithm to assign houses to capped batteries. \t(Manhattan Distance) ")
    print("  exit:\t\t Stop running main.\n")

def print_helpmsg_output():
    print("\n\u001b[32mOptions:\u001b[0m")
    print("  h | histo[gram]:\t Get histogram of N runs of chosen algorithm.")
    print("  f | figure:\t\t Create a figure of the .")
    print("  JSON:\t Get histogram of N runs of chosen algorithm.")

def print_possibilities(possibilities: list[str]) -> None:

    print("\n\u001b[32mPossible Load Files:\u001b[0m")
    for index, file in enumerate(sorted(possibilities)):
        print(f"{index+1}.  {file}")


def get_method_input() -> str:
    method = ""
    while not method:
        method = input("\u001b[33mMethod:\u001b[0m ").lower()
        if method == "exit":
            print("\nExiting main.\n")
            exit()
        elif method in {"help", "--help"}:
            print_helpmsg_methods()
            method = ""
        elif method not in {"format", "load", "randmanh", "randmanhcap",
                            "randrwalk", "greedmanh", "hillclimb", "beamsearch", "simulated"}:
            print("\nInvalid method. Type","\u001b[32mhelp\u001b[0m", "to see possibilities.\n")
            method = ""
    return method

def get_district_input() -> int:
    district = 0
    while not district:
        district = input("\n\u001b[33mDistrict Number:\u001b[0m ")
        if district == "exit":
            print("\nExiting main.\n")
            exit()
        elif not district.isnumeric() or not 1 <= int(district) <= 3:
            print("\nChoose a district between 1 and 3.")
            district = 0
    return int(district)

def get_runs_input(method: str) -> int:
    runs = 0
    if runs == "format":
        runs = 1
        return runs
    while not runs:
        runs = input("\n\u001b[33mRuns:\u001b[0m ")
        if runs == "exit":
            print("\nExiting main.\n")
            exit()
        elif not runs.isnumeric() or int(runs) < 1:
            print("\nPlease choose 1 or more runs.")
            runs = 0
    return int(runs)

def get_beam():
    beam = 0
    while not beam:
        beam = input("\n\u001b[33mBeam:\u001b[0m ")
        if beam == "exit":
            print("\nExiting main.\n")
            exit()
        elif not beam.isnumeric() or int(beam) < 1:
            print("\nPlease choose a beam of 1 or higher.")
            beam = 0
    return int(beam)

def get_load_file(possibilities: list[str]):
    file = ""
    while not file:
        file = input("\n\u001b[33mFile:\u001b[0m ")
        if file == "exit":
            print("\nExiting main.\n")
            exit()
        if not file in possibilities and not file.isnumeric():
            print("\nPlease choose one of the possibilities.")
            file = ""
        elif not file.isnumeric() or not 1 <= int(file) <= len(possibilities):
            print("\nPlease choose one of the possibilities.")
            file = ""
    if file.isnumeric():
        return possibilities[int(file) - 1]
    else:
        return file

def run_general_method(method: str):
    data = []
    if method == "format":
        data.append(load_JSON_output("output/output-format.json"))
    elif method == "load":
        possibilities = os.listdir("output/JSON/")
        if possibilities:
            print_possibilities(possibilities)
            file = get_load_file(possibilities)
            data.append(load_JSON_output(f"output/JSON/{file}"))
            # file_content = load_JSON_output(f"output/JSON/{file}")
            # if isinstance(file_content[0], dict):
            #     data.append(file_content)
            #     print(data)
            # else:
            #     data = file_content
        else:
            print("No load options. Try running an algorithm first.")
    return data


@Halo(text='Running method', spinner='dots')
def run_algo_method(method: str, district_number: int, runs: int) -> list:
    start_time = time.time()
    data = []
    district = District(district_number, "costs-own")

    if method == "randmanh":
        """
        Here we again apply a random assignment of houses to batteries,
        not taking the capacity into account. Instead of a random walk,
        we now implement the shortest Manhattan distance.
        """
        for _ in range(runs):
            district_copy = copy.deepcopy(district)
            data.append(run_random_assignment_shortest_distance(district_copy, method))

    elif method == "randmanhcap":
        """
        Here we again apply a random assignment of houses to batteries,
        not taking the capacity into account. Instead of a random walk,
        we now implement the shortest Manhattan distance.
        """
        for _ in range(runs):
            district_copy = copy.deepcopy(district)
            data.append(run_random_assignment_shortest_distance_with_capacity(district_copy, method))

    elif method == "greedmanh":
        """
        Here we apply a greedy algorithm. A house is assigned to the battery,
        starting at a random house, with the most capacity left.
        The path of the cable is created using the shortest Manhattan distance
        from the house towards the battery.
        """
        for _ in range(runs):
            district_copy = copy.deepcopy(district)
            data.append(run_greedy_assignment_shortest_walk(district_copy, method))

    elif method == "hillclimb":
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
        
    elif method == "simulated":
        simul = Simulatedannealing(district, 10000) #TODO?: 50000 variabel maken
        data.append(simul.run_hill_climber(district, runs, 1000).return_output())

    elif method == "beamsearch":
        beam = get_beam()
        beamsearch = BeamSearch(district, beam)
        data.append(beamsearch.run().return_output())

    # Does not work yet.
    # elif method == "randrwalk":
        # """
        # Here we apply a random assignment of houses to batteries,
        # not taking the capacity into account. Furthermore is a
        # random walk used for the connections between house and
        # batttery.
        # Takes quite some time and is really messy in visualisation,
        # so we only take the first house into account.
        # """
    #     print("Run are not taken into account.")
    #     data.append(run_alg_manh(district, cost_type))
    end_time = time.time()
    print(f"\n\u001b[32mMethod Time\u001b[0m: {round(end_time - start_time, 5)}")

    return data

def plot_data(data, method, runs: int = 1, district_number: str = "Graph"):
    if not data:
        print("Data Error.")
        exit()
    elif len(data) == 1:
        plot_output(data[0])
    else:
        outputs = []
        for district in data:
            outputs.append(district[0]["costs-own"])
        plot_output_histogram(outputs, method, runs, district_number)
