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

from random import shuffle


def greedy_assignment(district) -> None:
    """ Adds each house to the battery with the most capacity left
        pre: an instance of the District class and an optional starting
        house position can be passed as an int"""

    connection_dict = {}

    max_capacity = 0

    houses = district.houses
    shuffle(houses)

    for house in houses:
        # Determines battery with most capacity
        max_battery = None
        max_capacity = 0

        for battery in district.batteries:
            if battery.left_over_capacity > max_capacity and \
               battery.left_over_capacity >= house.output:
                max_capacity = battery.left_over_capacity
                max_battery = battery

        # If a compatible battery has been found, the house will be added
        if max_battery is not None:
            print(f"House {house.house_id} ->\
            Battery {max_battery.battery_id}")
            max_battery.add_house(house)
            connection_dict[house] = max_battery
        else:
            print("-------------------------------------------------")
            print("WARNING: house has not been assigned to a battery")
            print(f"House {house.house_id}: {house.output}, " +
                  f"x: {house.row}, y: {house.column}")
            print("-------------------------------------------------")

    return connection_dict
