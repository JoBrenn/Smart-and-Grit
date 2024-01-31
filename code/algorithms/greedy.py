""" Greedy algorithm

File: greedy.py

Author:    Jesper Vreugde

Date: 17/01/24

Description:
Here a greedy algorithm is implemented. Where greedy
implies choosing battery with most leftover capacity.
Here, a good solution is not guaranteed, since
it is not given a battery still has leftover capacity.

Usage:  from code.algorithms.greedy import ...
"""

from code.modules.house import House
from code.modules.battery import Battery
from code.modules.district import District

from random import shuffle


def greedy_assignment(district: District) -> dict[House, Battery]:
    """ Add each house to the battery with the most capacity left
        Create dictionary indicating these connections
        Params:
            district    (District): District object from which we want to start
        Returns:
            (dict) dictionary where house objects are keys and batteries values
    """

    connection_dict = {}

    max_capacity = 0.0

    houses = district.houses
    shuffle(houses)

    for house in houses:
        # Determines battery with most capacity
        max_battery = None
        max_capacity = 0.0

        for battery in district.batteries:
            if battery.left_over_capacity > max_capacity and \
               battery.left_over_capacity >= house.output:
                max_capacity = battery.left_over_capacity
                max_battery = battery

        # If a compatible battery has been found, the house will be added
        if max_battery is not None:
            max_battery.add_house(house)
            connection_dict[house] = max_battery
        else:
            print("-------------------------------------------------")
            print("WARNING: house has not been assigned to a battery")
            print(f"House {house.house_id}: {house.output}, " +
                  f"x: {house.row}, y: {house.column}")
            print("-------------------------------------------------")

    return connection_dict
