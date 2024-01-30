""" Random algorithm

File: random..py

Author:    Kathy Molenaar

Date: 19/01/24

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


def get_surrounding_points(coordinates: tuple[int, int],
                           grid_size: int) -> list[tuple[int, int]]:
    """ Get surrounding points of a given coordinate
    Params:
        coordinates (tuple[int]):   tuple of coordinates
        grid_size   (int):          grid size integer
    Returns:
        (list) list of border points of given point
    """

    border_points = []

    x = coordinates[0]
    y = coordinates[1]

    # Check border cases
    if x - 1 >= 0:
        border_points.append((x - 1, y))
    if y - 1 >= 0:
        border_points.append((x, y - 1))
    if x + 1 <= grid_size:
        border_points.append((x + 1, y))
    if y + 1 <= grid_size:
        border_points.append((x, y + 1))

    return border_points


def random_walk(house: tuple[int, int], battery: tuple[int, int],
                grid_size: int) -> list[tuple[int, int]]:
    """ Take a random walk from the house, stops when battery is reached
        adds all visited points to list
    Params:
        house   (tuple[int]):    tuple of house coordinates
        battery (tuple[int]):    tuple of battery coordinates
        grid_size   (int):       grid size integer
    Returns:
        (list) list of points visited in random walk
    """

    # Initialize current location at the house
    current_location = house
    points_visited = [current_location]

    while current_location != battery:
        new_point = choice(get_surrounding_points(current_location,
                                                  grid_size))
        current_location = new_point
        points_visited.append(current_location)

    return points_visited
