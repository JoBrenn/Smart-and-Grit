""" Code to run random and greedy algorithms

File: run.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 10/01/24 (31/01/24)

Description:
All random and greedy algorithms can be run by the functions
in this file.

Usage:  from code.algorithms.run import ...
"""

from code.modules.district import District
from code.algorithms.random_algorithm import random_assignment, \
    random_assignment_capacity
from code.algorithms.greedy import greedy_assignment
from code.algorithms.manhattan_distance import create_cable

from typing import Any


def runs_algorithms_to_costs(district_number: int, runs: int,
                             alg_method: str) -> list[int] | int:
    """ Create list of outputs, used for mpl histogram
        Creates connections via Manhattan distance
        Params:
            district_number    (int): district number
            runs               (int): number of runs wanted
            alg_method         (str): name of algorithm method
        Returns:
            (list[int] or int) list of all costs or zero 
                               when method not random
    """

    outputs = []

    for run in range(runs):
        district = District(district_number, "costs-own")

        # Check for different methods
        if alg_method == "randmanh":
            output = run_random_assignment(district, "costs-own")
        elif alg_method == "randmanhcap":
            output = \
                run_random_assignment_with_capacity(district, "costs-own")
        else:
            return 0
        outputs.append(output[0]["costs-own"])

    return outputs


def run_random_assignment(district: District,
                          costs_type: str) -> list[dict[str, Any]]:
    """ Randomly assigns the houses in a district to batteries and
        lays connections along the Manhattan distance.
        Plots the grid
        Params:
            district    (District): district object
            costs_type  (str):      either costs-own or costs-shared
        Returns:
            (list) output list
    """

    connections = random_assignment(district)

    for house in connections:
        battery = connections[house]

        # Create cables
        create_cable(house, (battery.row, battery.column))

    # Place cost in district dictionary
    district.district_dict[f"{district.costs_type}"] = district.return_cost()

    output = district.return_output()

    return output


def run_random_assignment_with_capacity(district: District, costs_type: str) \
                                        -> list[dict[str, Any]]:
    """ Randomly assigns the houses in a district to batteries with enough
        capacity and lays connections along the shortest Manhattan distance.
        Plots the grid
        Params:
            district    (District): district object
            costs_type  (str):      either costs-own or costs-shared
        Returns:
            (list[dict) output list
    """

    connections = random_assignment_capacity(district)

    for house in connections:
        battery = connections[house]
        create_cable(house, (battery.row, battery.column))

    district.district_dict[f"{district.costs_type}"] = district.return_cost()
    output = district

    return output


def run_greedy_assignment_shortest_walk(district: District) \
                                        -> list[dict[str, Any]]:
    """ Creates cables between houses and batteries that have
        been assigned using the greedy algorithm and plots this.
        Starts at a random house.
        Params:
            district    (District): district object
            costs_type  (str):      either costs-own or costs-shared
        Returns:
            (list[dict]) output list
    """
    # Create connection dictionary that assigns batteries to houses
    connections = greedy_assignment(district)

    # Loops over each house in the district that has a battery assigned
    # for n, house in enumerate(connections):
    for house in connections:
        battery = connections[house]
        battery.add_house(house)
        create_cable(house, (battery.row, battery.column))

    district.district_dict[f"{district.costs_type}"] = district.return_cost()
    output = district.return_output()

    return output
