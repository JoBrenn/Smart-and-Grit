from random import randint, shuffle
from code.visualisation.visualize import *
from code.algorithms.manhattan_distance import get_cable_points, create_cable

def greedy_assignment(district) -> None:
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
            print(f"House {house.house_id}: {house.output}, "+ \
                f"x: {house.row}, y: {house.column}")
            print("-------------------------------------------------")

"""
def greedy_assignment(district, starting_house: int = 0) -> None:
    """""" Adds each house to the battery with the most capacity left
        pre: an instance of the District class and an optional starting
        house position can be passed as an int
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

    return True """
