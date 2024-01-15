from code.visualisation.visualize_output import *

def greedy_assignment(district) -> None:
    """ Adds each house to the battery with the most capacity left
        pre: an instance of the District class"""
    max_capacity = 0
    
    for house in district.houses:
        # Determines battery with most capacity
        max_battery = None
        max_capacity = 0

        for battery in district.batteries:
            if battery.left_over_capacity > max_capacity and \
               battery.left_over_capacity >= house.output:
                max_capacity = battery.left_over_capacity
                max_battery = battery
            
        # Quickfix for now
        if max_battery != None:
            max_battery.add_house(house)
            
def run_greedy_assignment_shortest_walk(district) -> None:
    """ Creates cables between houses and batteries that have 
        been assigned using the greedy algorithm and plots this.
        pre: a District object is passed as an argument"""
    # Uses greedy algorithm to assign houses to batteries
    greedy_assignment(district)
    
    # Loops over each house in each battery to create cable paths
    for battery in district.batteries:
        for house in battery.houses: 
            district.create_cable(house, battery)
    print(f"The cost for greedy assignment and shortest Manhattan distance in district {district.district} is {district.return_cost()}.")
    plot_output(district.return_output(), "Greedy + Manhattan")