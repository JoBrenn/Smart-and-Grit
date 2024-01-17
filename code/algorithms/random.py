import random
from code.algorithms.manhattan_distance import get_cable_points, create_cable


def random_assignment(district):#batteries: list, houses: list) -> dict:
    """ Randomly assign houses to batteries, not taking capacity into account
    Creates dictionary, where houses are keys and batteries values
    Params:
        district: District instance containing Battery and House instances
    Returns:
        (dict) houses as keys and batteries as values
    """
    connection_dict = {}
    for house in district.houses:
        connection_dict[house] = random.choice(district.batteries)
        connection_dict[house].add_house(house)

    return connection_dict

def random_assignment_capacity(district) -> dict:
    """ Randomly assigns houses to batteries, taking capacity into account
        Adds this to dictionary with house as key and battery as value
        post: returns dictionary"""

    connection_dict = {}
    for house in district.houses:
        # Randomize the batteries list for every house
        random.shuffle(district.batteries)
        # Walk through elements of list an check capacity
        for battery in district.batteries:
            if battery.left_over_capacity - house.output >= 0:
                battery.add_house(house)
                connection_dict[house] = battery
                # Stop when we have found a battery with enough capacity
                break

    return connection_dict

def get_surrounding_points(coordinates: tuple[int], grid_size: int) -> list:
    """ returns list of the surrounding points given x and y coordinates of a point"""

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


def random_walk(house: tuple[int], battery: tuple[int], grid_size: int) -> list:
    """ Takes a random walk from the house, stops when battery is reached
        adds all visited points to list"""

    # Initialize current location at the house
    current_location = house
    points_visited = [current_location]

    while current_location != battery:
        new_point = random.choice(get_surrounding_points(current_location, grid_size))
        current_location = new_point
        points_visited.append(current_location)

    return points_visited
