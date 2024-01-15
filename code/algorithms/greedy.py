from random import randint, shuffle
from code.visualisation.visualize import *

"""
def greedy_assignment(district, starting_house: int = 0) -> None:
    """""" Adds each house to the battery with the most capacity left
        pre: an instance of the District class and an optional starting
        house position can be passed as an int""""""
    max_capacity = 0
    houses_amount = len(district.houses)
    
    
    house_order = [*range(0, houses_amount, 1)]
    shuffle(house_order)
    print(house_order)
    
    for i in house_order:
        # Determines battery with most capacity
        max_battery = None
        max_capacity = 0 
        
        house_num = (i + starting_house) % houses_amount
        
        for battery in district.batteries:
            if battery.left_over_capacity > max_capacity and \
               battery.left_over_capacity >= district.houses[i].output:
                max_capacity = battery.left_over_capacity
                max_battery = battery
        
        # If a compatible battery has been found, the house will be added
        if max_battery != None:
            max_battery.add_house(district.houses[i])
        else:
            print("WARNING: one or more houses have not been assigned to a battery")   """

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

        bat_num = 0

        for n, battery in enumerate(district.batteries):
            if battery.left_over_capacity > max_capacity and \
               battery.left_over_capacity >= district.houses[house_num].output:
                max_capacity = battery.left_over_capacity
                max_battery = battery
                bat_num = n + 1
        
        # If a compatible battery has been found,  will be added
        if max_battery != None:
            max_battery.add_house(district.houses[house_num])
            print(f"House {i} -> Battery {bat_num}")
        else:
            print("WARNING: one or more houses have not been assigned to a battery")
            print(f"House {i}: {district.houses[house_num].output}")       

    for n, battery in enumerate(district.batteries):
        print(f"Battery {n + 1}: {battery.left_over_capacity}")    
        
            
def run_greedy_assignment_shortest_walk(district) -> list:
    """ Creates cables between houses and batteries that have 
        been assigned using the greedy algorithm and plots this.
        Starts at a random house.
        post: returns output list"""
        
    start = randint(0, len(district.houses) - 1)
    # Uses greedy algorithm to assign houses to batteries
    greedy_assignment(district, start)
    
    # Loops over each house in each battery to create cable paths
    for battery in district.batteries:
        for house in battery.houses: 
            district.create_cable(house, battery)
    print(f"The cost for greedy assignment and shortest Manhattan distance in district {district.district} is {district.return_cost()}.")
    
    output = district.return_output()
    
    return output