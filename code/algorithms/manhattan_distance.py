from code.modules.house import House
from code.modules.battery import Battery

def get_cable_points(begin: tuple[int], end: tuple[int]) -> tuple[int]:
        """ Generates the points between which a cable must be layed from house
            to battery, following the shortest Manhatten distance
            From house first up or down then left or right"""

        points = [begin, (begin[0], end[1]), end]
        return tuple(points)

def create_cable(house: House, end: tuple[int]) -> None:
    """ Creates entire cable connection between house and battery
        following shortest manhatten distance.
        Again following from house first up or donw then left or right
        post: returns the cost of the cable"""

    cable_points = get_cable_points((house.row, house.column), (end[0], end[1]))

    # begin y minus in between y
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
