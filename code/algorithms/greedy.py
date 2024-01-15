from random import randint
from code.visualisation.visualize import *


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
        # Quickfix for now
        if max_battery != None:
            max_battery.add_house(district.houses[house_num])          
        
            
def run_greedy_assignment_shortest_walk(district) -> None:
    """ Creates cables between houses and batteries that have 
        been assigned using the greedy algorithm and plots this.
        Starts at a random house.
        pre: a District object is passed as an argument"""

    start = randint(0, len(district.houses) - 1)

    # Uses greedy algorithm to assign houses to batteries
    greedy_assignment(district, start)
    
    # Loops over each house in each battery to create cable paths
    for battery in district.batteries:
        for house in battery.houses: 
            district.create_cable(house, battery)
    print(f"The cost for greedy assignment and shortest Manhattan distance in district {district.district} is {district.return_cost()}.")
    plot_output(district.return_output(), "Greedy + Manhattan")