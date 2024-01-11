import random

def random_assignment(self, batteries: list, houses: list) -> dict:
    """ Randomly assigns houses to batteries, not taking capacity into account
        Adds this to dictionary with house as key and battery as value
        post: returns dictionary"""
        
    connection_dict = {}
    for house in houses:
        connection_dict[house] = batteries[random.randint(0, len(batteries) - 1)]
    
    return connection_dict

def get_surrounding_points(self, coordinates: tuple[int], grid_size: int) -> list:
    """ returns list of the surrounding points given x and y coordinates of a point"""
    
    border_points = []
    
    x = coordinates[0]
    y = coordinates[1]
    
    # Check border cases
    if x - 1 >= 0:
        border_points.append((x - 1, y))
    elif y - 1 >= 0:
        border_points.append((x, y - 1))
    elif x + 1 <= grid_size:
        border_points.append((x + 1, y))
    elif y + 1 <= grid_size:
        border_points.append((x, y + 1))
    
    return border_points
        
    
def random_walk(self, x_house: int, y_house: int, x_battery: int, y_battery: int, grid_size: int) -> list:
    """ Takes a random walk from the house, stops when battery is reached
        adds all visited points to list
        TO-DO: add cable-segments along the random walk"""
    
    # Initialize current location at the house
    current_location = (x_house, y_house)
    
    points_visited = [current_location]
    
    while current_location != (x_battery, y_battery):
        new_point = random.choice(get_surrounding_points(self, current_location, grid_size))
        current_location = new_point
    
    return points_visited