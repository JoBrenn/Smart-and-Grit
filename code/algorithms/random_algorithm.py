""" Random algorithm

File: random.py

Author:    Kathy Molenaar

Date: 19/01/24 (31/01/24)

Description:
Here a random configuration is created for a given district

Usage:  from code.algorithms.random import ...
"""

from code.modules.district import District
from code.modules.house import House
from code.modules.battery import Battery

from random import choice, shuffle


def random_assignment(district: District) -> dict[House, Battery]:
    """ Randomly assign houses to batteries, not taking capacity into account
    Creates dictionary, where houses are keys and batteries values
    Params:
        district    (District): district object
    Returns:
        (dict) houses as keys and batteries as values
    """

    connection_dict = {}
    for house in district.houses:
        connection_dict[house] = choice(district.batteries)
        connection_dict[house].add_house(house)

    return connection_dict


def random_assignment_capacity(district: District) -> dict[House, Battery]:
    """ Randomly assigns houses to batteries, taking capacity into account
        Adds this to dictionary with house as key and battery as value
    Params:
        district    (District): district object
    Returns:
        (dict) houses as keys and batteries as values
    """

    connection_dict = {}
    for house in district.houses:
        # Randomize the batteries list for every house
        shuffle(district.batteries)

        # Walk through elements of list an check capacity
        for battery in district.batteries:
            if battery.left_over_capacity - house.output >= 0:
                battery.add_house(house)
                connection_dict[house] = battery

                # Stop when we have found a battery with enough capacity
                break

    return connection_dict
