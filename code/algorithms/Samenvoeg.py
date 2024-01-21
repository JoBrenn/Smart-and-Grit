from code.modules.district import District
from code.modules.battery import Battery
from code.modules.house import House
from code.algorithms.manhattan_distance import return_manhattan_distance, create_cable

import random

def assign_random_house(battery: Battery) -> House
    """ Assign a random house connected to battery to hold it's original path"""
    
    house = random.choice(battery.houses)
        
    return house

def combine_cables_battery(battery: Battery) -> Battery
    """ Combine cable connections associated with a single battery
    Alter battery dictionary to new configuration
    Returns:
        (Battery) Battery object with altered cables in dictionary"""

    battery_coordinate = (battery.row, battery.column)
    
    same_house = assign_random_house(battery)
    all_cable_points = set(same_house.cables)
    
    # Randomly shuffle battery.houses to get random order of combining
    for house in random.shuffle(battery.houses):
        # Do not alter the one house
        if house != same_house:
            manhattan_cable_length = return_manhattan_distance(house, battery_coordinate)
            shortest_length = manhattan_cable_length
            shortest_coordinate = battery_coordinate
            for point in all_cable_points:
                if return_manhattan_distance(house, point) < shortest_length:
                    shortest_length = return_manhattan_distance(house, point)
                    shortest_coordinate = point
                    # Delete old cable, will not need it
                    house.delete_cables()
                    # Delete house from battery, such that old cable is removed in dictionary
                    battery.delete_house(house)
            # After having point shortest from all points create new cable
            create_cable(house, shortest_coordinate)
            # Alter dictionary
            house.house_dict["cables"] = house.str_cables
            # Add house to battery again
            battery.add_house(house)
            # Add new cable points to the set
            for point in house.cables:
                all_cable_points.add(point)
    
    return battery

def combine_district(district: District) -> District
    """ Combine cable connections for entire district
    Alter district dictionary to new configuration
    Params:
            district    (District):        filled district configuration
    Returns:
        (District) District object with altered cables in output"""
    
    # Combine for every battery
    for battery in district.batteries:
        # Remove old dictionary from output
        district.output.remove(battery.battery_dict)
        battery_new = combine_cables_battery(battery)
        # Add new dictionary to output
        district.output.append(battery_new.battery_dict)
    
    # Alter dictionary cost in dictionary
    district.output[0] = {"district": district.district, f"{costs_type}": return_cost(district)}
    
    return district

def run(district: District, n: int) -> District
    """ Combine cable connections for entire district n times
    Gives best solution
    Params:
            district    (District):        filled district configuration
            n           (int):             number of iterations
    Returns:
        (District) District configuration with lowest cost"""
    
    district_original = copy.deepcopy(district)
    lowest_cost = district_original.return_cost()
    district_best = district_original
    
    for iteration in range(n):
        district = combine_district(district_original)
        cost = district.return_cost()
        if cost < lowest_cost:
            district_best = district
    
    return district_best
        
        