""" Manhattan distance functions

File: manhattan_distance.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 12/01/24

Description:
Determines Manhattan distance and lays cables along this distance

Usage:  from code.algorithms.manhattan_distance import ...
"""

from code.modules.house import House

# Create a coordinate typehint structure
CoStructure = tuple[int, int]


def get_cable_points(begin: CoStructure, end: CoStructure) \
                    -> tuple[CoStructure, CoStructure, CoStructure]:
    """ Generate 3 points between which cable must be layed
        along Manhattan distance
        From begin point first up or down then left or right
    Params:
        begin    (tuple[int]): tuple of begin coordinates
        end      (tuple[int]): tuple of end coordinates
    Returns:
        (tuple[int]) tuple of begin, in between, end coordinates
    """

    points = [begin, (begin[0], end[1]), end]

    return tuple(points)


def return_manhattan_distance(house: House, end: CoStructure) -> int:
    """ Return manhattan distance from a house to a given end point
        Params:
            house         (House): House object from which we want to start
            end    (tuple[int]): given end coordinate
        Returns:
            (int) Manhattan distance between house and end point
    """

    house_coordinate = (house.row, house.column)

    x_distance = abs(house_coordinate[0] - end[0])
    y_distance = abs(house_coordinate[1] - end[1])
    distance = x_distance + y_distance

    return distance


def create_cable(house: House, end: CoStructure) -> None:
    """ Creates entire cable connection between house and end point
        following shortest manhatten distance.
        Params:
            house         (House): House object from which we want to start
            end    (tuple[int]): given end coordinate
        Returns:
            none
            add cable to house object
    """

    cable_points = get_cable_points((house.row, house.column),
                                    (end[0], end[1]))

    # Begin y minus in between y
    y_distance = cable_points[0][1] - cable_points[1][1]

    # In between x minus end x
    x_distance = cable_points[1][0] - cable_points[2][0]

    # Start at the begin
    x_current = house.row
    y_current = house.column

    # Add house coordinate
    house.add_cable_segment((x_current, y_current))

    # Check whether we need to go up or down
    if y_distance > 0:
        # Down
        for step in range(y_distance):
            y_current -= 1
            house.add_cable_segment((x_current, y_current))

    elif y_distance < 0:
        # Up
        for step in range(abs(y_distance)):
            y_current += 1
            house.add_cable_segment((x_current, y_current))

    # Check whether we need to go left or right
    if x_distance > 0:
        # Left
        for step in range(x_distance):
            x_current -= 1
            house.add_cable_segment((x_current, y_current))

    elif x_distance < 0:
        # Right
        for step in range(abs(x_distance)):
            x_current += 1
            house.add_cable_segment((x_current, y_current))
