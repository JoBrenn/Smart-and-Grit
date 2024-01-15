from random import randint, shuffle
from code.visualisation.visualize import *
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


def greedy_assignment_2(district) -> None:
    """ Adds each house to the battery with the most capacity left
        pre: an instance of the District class and an optional starting
        house position can be passed as an int"""
    max_capacity = 0
    houses_amount = len(district.houses)   
    
    #house_order = [*range(0, houses_amount, 1)]
    #shuffle(house_order)
    #print(house_order)

    houses = district.houses

    shuffle(houses)
    
    for house in houses:
        # Determines battery with most capacity
        max_battery = None
        max_capacity = 0 
        
        #house_num = (i + starting_house) % houses_amount
        
        for battery in district.batteries:
            if battery.left_over_capacity > max_capacity and \
               battery.left_over_capacity >= house.output:
                max_capacity = battery.left_over_capacity
                max_battery = battery
        
        # If a compatible battery has been found, the house will be added
        if max_battery != None:
            print(f"House {house.house_id} -> Battery {max_battery.battery_id}")
            max_battery.add_house(house)
        else:
            print("-------------------------------------------------")
            print("WARNING: house has not been assigned to a battery")
            print(f"House {house.house_id}: {house.output}, x: {house.row}, y: {house.column}")  
            print("-------------------------------------------------") 

    for battery in district.batteries:
        print(f"Battery {battery.battery_id}: {battery.left_over_capacity}") 

def greedy_assignment(district, starting_house: int = 0) -> None:
    """ Adds each house to the battery with the most capacity left
        pre: an instance of the District class and an optional starting
        house position can be passed as an int"""
    max_capacity = 0
    houses_amount = len(district.houses)
    
    for i in range(houses_amount):
        # Determines battery with most capacity
        max_battery = None
        max_capacity = 0

        house_num = (i + starting_house) % houses_amount

        for battery in district.batteries:
            if battery.left_over_capacity > max_capacity and \
               battery.left_over_capacity >= district.houses[house_num].output:
                max_capacity = battery.left_over_capacity
                max_battery = battery
        
        # If a compatible battery has been found,  will be added
        if max_battery != None:
            max_battery.add_house(district.houses[house_num])
            print(f"House {i} -> Battery {max_battery.battery_id}")
        else:
            print("-------------------------------------------------")
            print("WARNING: house has not been assigned to a battery")
            print(f"House {i}: {district.houses[house_num].output}, "+ \
                f"x: {district.houses[house_num].row}, y: {district.houses[house_num].column}")  
            print("-------------------------------------------------")     

    for battery in district.batteries:
        print(f"Battery {battery.battery_id}: {battery.left_over_capacity}") 
  
        
            
def run_greedy_assignment_shortest_walk(district, costs_type: str) -> list:
    """ Creates cables between houses and batteries that have 
        been assigned using the greedy algorithm and plots this.
        Starts at a random house.
        post: returns output list"""
        
    start = randint(0, len(district.houses) - 1)
    # Uses greedy algorithm to assign houses to batteries
    greedy_assignment_2(district)
    
    # Loops over each house in each battery to create cable paths
    for battery in district.batteries:
        for house in battery.houses: 
            district.district_dict[costs_type] += create_cable(house, battery)

    print(f"The cost for greedy assignment and shortest Manhattan distance in district {district.district} is {district.return_cost()}.")
    
    output = district.return_output()
    
    return output