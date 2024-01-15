import random
from code.algorithms.shortest_manhattan_distance_cables import get_cable_points, create_cable

def random_assignment(batteries: list, houses: list) -> dict:
    """ Randomly assigns houses to batteries, not taking capacity into account
        Adds this to dictionary with house as key and battery as value
        post: returns dictionary"""

    connection_dict = {}
    for house in houses:
        connection_dict[house] = random.choice(batteries)

    return connection_dict

def random_assignment_capacity(batteries: list, houses: list) -> dict:
    """ Randomly assigns houses to batteries, taking capacity into account
        Adds this to dictionary with house as key and battery as value
        post: returns dictionary"""

    connection_dict = {}
    for house in houses:
        # Randomize the batteries list for every house
        random.shuffle(batteries)
        # Walk through elements of list an check capacity
        for battery in batteries:
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

def run_random_assignment_random_walk(district) -> list:
    """ Randomly assigns the first house in a district to a battery and
        lays a connection along the shortest Manhattan distance.
        Plots the grid
        post: returns output list"""

    connections = random_assignment(district.batteries, district.houses)
    house_1 = list(connections.keys())[0]
    battery = connections[house_1]
    battery.add_house(house_1)
    points_walked = random_walk((int(house_1.row), int(house_1.column)), (int(battery.row), int(battery.column)), 50)
    # Add a cable segment between all the points visited in the random walk
    for i in range(len(points_walked) - 1):
        house_1.add_cable_segment((points_walked[i][0], points_walked[i][1]),\
                        (points_walked[i + 1][0], points_walked[i + 1][1]))

    output = district.return_output()
    return output

def run_random_assignment_shortest_distance(district, costs_type) -> list:
    """ Randomly assigns the houses in a district to batteries and
        lays connections along the shortest Manhattan distance.
        Plots the grid
        post: returns output list"""

    connections = random_assignment(district.batteries, district.houses)
    for house in connections:
        battery = connections[house]
        # Add the house to the battery connection (such that dictionary is added)
        battery.add_house(house)
        district.district_dict[costs_type] += create_cable(house, battery)

    print(f"The cost for random assignment and shortest Manhattan distance in district {district.district}\
 is {district.return_cost()}.")

    # district.create_cable(house, battery)

    output = district.return_output()

    return output


def run_random_assignment_shortest_distance_with_capacity(district, costs_type) -> list:
    """ Randomly assigns the houses in a district to batteries with enough
        capacity and lays connections along the shortest Manhattan distance.
        Plots the grid
        post: returns output list"""

    connections = random_assignment_capacity(district.batteries, district.houses)
    for house in connections:
        battery = connections[house]
        district.district_dict[costs_type] += create_cable(house, battery)

    print(f"The cost for random assignment with enough capacity\
 and shortest Manhattan distance in district {district.district}\
 is {district.return_cost()}.")

    output = district.return_output()

    return output
