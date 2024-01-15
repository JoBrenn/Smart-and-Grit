import random
from code.modules.house import House
from code.modules.battery import Battery

def get_cable_points(house: tuple[int], battery: tuple[int]) -> tuple[int]:
        """ Generates the points between which a cable must be layed from house
            to battery, following the shortest Manhatten distance
            From house first up or down then left or right"""

        points = [house, (house[0], battery[1]), battery]
        return tuple(points)

def create_cable(house: House, battery: Battery) -> int:
    """ Creates entire cable connection between house and battery
        following shortest manhatten distance.
        Again following from house first up or donw then left or right
        post: returns the cost of the cable"""

    cable_points = get_cable_points((house.row, house.column), (battery.row, battery.column))
    cable_cost = 0

    # House y minus in between y
    y_distance = cable_points[0][1] - cable_points[1][1]
    # In between x minus battery x
    x_distance = cable_points[1][0] - cable_points[2][0]

    # Start at the house
    x_current = house.row
    y_current = house.column

    # Check whether we need to go up or down
    if y_distance > 0:
        # Down
        for step in range(y_distance):
            house.add_cable_segment((x_current, y_current), (x_current, y_current - 1))
            # Add the costs of the cable
            cable_cost += 9
            y_current -= 1
    elif y_distance < 0:
        # Up
        for step in range(abs(y_distance)):
            house.add_cable_segment((x_current, y_current + 1), (x_current, y_current))
            cable_cost += 9
            y_current += 1

   # Check whether we need to go left or right
    if x_distance > 0:
        # Left
        for step in range(x_distance):
            house.add_cable_segment((x_current, y_current), (x_current - 1, y_current))
            cable_cost += 9
            x_current -= 1
    elif x_distance < 0:
        # Right
        for step in range(abs(x_distance)):
            house.add_cable_segment((x_current, y_current), (x_current + 1, y_current))
            cable_cost += 9
            x_current += 1

    return cable_cost

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
