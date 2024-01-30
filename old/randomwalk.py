from code.modules.district import District
from code.modules.house import House
from code.modules.battery import Battery
from code.modules.district import District
from code.algorithms.random_algorithm import random_walk, \
    random_assignment, random_assignment_capacity
from code.algorithms.greedy import greedy_assignment
from code.algorithms.manhattan_distance import create_cable

from typing import Any
from random import choice, shuffle
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


def run_random_assignment_random_walk(district: District) \
                                      -> list[dict[str, Any]]:
    """ Randomly assigns the first house in a district to a battery and
        lays a connection along the Manhattan distance.
        Plots the grid
        Params:
            district    (District): district object
        Returns:
            (list) output list
    """

    connections = random_assignment(district)
    house_1 = list(connections.keys())[0]
    battery = connections[house_1]
    battery.add_house(house_1)
    points_walked = random_walk((int(house_1.row), int(house_1.column)),
                                (int(battery.row), int(battery.column)), 50)

    # Add a cable segment between all the points visited in the random walk
    for i in range(len(points_walked) - 1):
        house_1.add_cable_segment(points_walked[i])

    # Temp fix
    battery.battery_dict["houses"] = [battery.battery_dict["houses"][0]]

    district.output = [district.output[0]]
    district.output.append(battery.battery_dict)

    output = district.return_output()

    return output
