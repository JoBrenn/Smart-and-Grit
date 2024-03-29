""" Functions able to combine cables in district

File: combine_cables.py

Author:    Kathy Molenaar

Date: 19/01/24

Description:
Here from a district configuration where each house has
its own cable a new configuration with combined cables
can be made

Usage:  from code.algorithms.combine_cables import ...
"""

from random import shuffle, choice
from copy import deepcopy
from json import dump
from code.modules.battery import Battery
from code.modules.house import House
from code.algorithms.manhattan_distance import return_manhattan_distance, \
                                               create_cable


def assign_random_house(houses: list) -> dict:
    """ Assign one random house from a list
        Params:
            houses    (list): list with house objects to choose from
        Returns:
            (dict) dictionary of said house object
    """

    house_dict = choice(houses)

    return house_dict


def combine_cables_battery(battery_dict: dict) -> Battery:
    """ Combine cable connections associated with a single battery
        Alter battery dictionary to new configuration
        Params:
            battery_dict  (dict):   battery dictionary
        Returns:
           (Battery)   Battery object with altered cables in dictionary
    """

    battery_x = int(battery_dict["location"].split(",")[0])
    battery_y = int(battery_dict["location"].split(",")[1])
    battery_coordinate = (battery_x, battery_y)

    houses_dicts = []

    for house_dict in battery_dict["houses"]:
        houses_dicts.append(house_dict)

    same_house_dict = assign_random_house(houses_dicts)
    all_cable_points = set()
    for point in same_house_dict["cables"]:
        point = (int(point.split(",")[0]), int(point.split(",")[1]))
        all_cable_points.add(point)

    # Randomly shuffle houses to get random order of combining
    shuffle(houses_dicts)

    for house_dict in houses_dicts:
        house_x = int(house_dict["location"].split(",")[0])
        house_y = int(house_dict["location"].split(",")[1])
        house_coordinate = (house_x, house_y)
        house = House(1, house_coordinate, float(house_dict["output"]))

        # Do not alter the one house
        if house_dict != same_house_dict:
            manhattan_cable_length\
                = return_manhattan_distance(house, battery_coordinate)
            shortest_length = manhattan_cable_length
            shortest_coordinate = battery_coordinate
            for point in all_cable_points:
                # Keep track of shortest length
                if return_manhattan_distance(house, point) < shortest_length:
                    shortest_length = return_manhattan_distance(house, point)
                    shortest_coordinate = point

                    # Delete old cable
                    house_dict["cables"].clear()

            # After having point shortest from all points create new cable
            create_cable(house, shortest_coordinate)

            # Alter house dictionary
            house_dict["cables"] = house.str_cables

            # Add new cable points to the set
            for point in house.cables:
                all_cable_points.add(point)

    return battery_dict


def combine_district(output: list) -> list:
    """ Combine cable connections for entire district
        Alter district dictionary to new configuration
    Params:
            output    (list):  filled output of district configuration
    Returns:
        (list) altered cables in output
    """

    output_original = deepcopy(output)

    cost = 0

    # Combine for every battery
    for battery_dict in output[1:]:
        cost += 5000

        # Remove old dictionary from output
        output.remove(battery_dict)
        battery_dict_new = combine_cables_battery(battery_dict)

        # Add new dictionary to output
        output.append(battery_dict_new)
        for house_dict in battery_dict_new["houses"]:
            cable_length = len(house_dict["cables"]) - 1
            if cable_length != -1:
                cost += cable_length * 9

    # Delete old costs from output
    del output[0]["costs-own"]

    # Add new cost value and change it to costs-shared
    output[0]["costs-shared"] = cost

    return output, output_original


def run(output: list, n: int, filename: str) -> list:
    """ Combine cable connections for entire district n times
        Gives best solution
    Params:
            output    (list):   filled output of district configuration
            n         (int):    number of iterations
            filename  (str):     filename of json output we want to combine
    Returns:
        ((list) altered cables in output with lowest cost
    """

    output_original = deepcopy(output)
    lowest_cost = output_original[0]["costs-own"]
    output_best = output_original

    # Combine cables n different times
    for iteration in range(n):
        output, output_original = combine_district(output_original)
        cost = output[0]["costs-shared"]
        if cost < lowest_cost:
            output_best = deepcopy(output)

    filepath = f"output/JSON/{filename}-combined.json"
    with open(filepath, "w") as f:
        dump(output_best, f, indent=4)

    return output_best
