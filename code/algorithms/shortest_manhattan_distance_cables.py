from code.modules.house import House
from code.modules.battery import Battery

def get_cable_points(house: tuple[int], battery: tuple[int]) -> tuple[int]:
        """ Generates the points between which a cable must be layed from house
            to battery, following the shortest Manhatten distance 
            From house first up or down then left or right"""
           
        points = [house, (house[0], battery[1]), battery]
        return tuple(points)
        
def create_cable(house: House, battery: Battery) -> None:
    """ Creates entire cable connection between house and battery
        following shortest manhatten distance. 
        Again following from house first up or donw then left or right
        post: returns the cost of the cable"""
    
    cable_points = get_cable_points((house.row, house.column), (battery.row, battery.column))
    #cable_cost = 0
    
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
            #cable_cost += 9
            y_current -= 1
    elif y_distance < 0:
        # Up
        for step in range(abs(y_distance)):
            house.add_cable_segment((x_current, y_current + 1), (x_current, y_current))
            #cable_cost += 9
            y_current += 1
   
   # Check whether we need to go left or right
    if x_distance > 0:
        # Left
        for step in range(x_distance):
            house.add_cable_segment((x_current, y_current), (x_current - 1, y_current))
            #cable_cost += 9
            x_current -= 1
    elif x_distance < 0:
        # Right
        for step in range(abs(x_distance)):
            house.add_cable_segment((x_current, y_current), (x_current + 1, y_current))
            #cable_cost += 9
            x_current += 1