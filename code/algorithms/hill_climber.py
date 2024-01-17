import random
import copy
from code.modules.district import District
from code.modules.district import Battery
from code.modules.district import House
from code.algorithms.manhattan_distance import get_cable_points, create_cable

"""Hill Climber with constraint relaxation where penalty is equal to capacity surplus"""

def random_start_state(district: District) -> District:     
    """ Randomly assign houses to batteries, not taking capacity into account
    Creates dictionary, where houses are keys and batteries values
    Creates connections via Manhattan distance
    Params:
        district    (District): district object
    Returns:
        (list) output list
    """

    for house in district.houses: 
        battery = random.choice(district.batteries)
        # Add the house to the battery connection (such that dictionary is added)
        battery.add_house(house)
        create_cable(house, (battery.row, battery.column))
    district.district_dict[f"{district.costs_type}"] = district.return_cost()
    
    output = district.return_output()
    
    return district

def random_change(district: District, costs_type: str) -> list:
    """ Randomly change one house-battery connection
    Alters this change in the connection dictionary
    Params:
        batteries          (list): list of batteries in district
        connection_dict    (dict): dictionary where houses are keys and batteries values
    Returns:
        (District) altered district object
    """
    
    output_1 = copy.deepcopy(district.output)
    
    # Get random house from district
    random_house = random.choice(district.houses)
    dictionary = copy.deepcopy(random_house.house_dict)

    # Find old battery connection
    for battery in district.batteries:
        if random_house in battery.houses:
            old_battery = battery
    
    # Delete it in output dictionary
    index = district.output.index(old_battery.battery_dict)
    district.output[index]["houses"].remove(dictionary)
    
    # Delete house from old battery
    old_battery.delete_house(random_house)
    
    # Delete old cables
    random_house.cables.clear()
    random_house.str_cables.clear()
    
    # Clear house dictionary
    random_house.house_dict["cables"].clear()
    
                  
    # Determine new random battery
    new_battery = random.choice(district.batteries)
    # Add house to new battery
    new_battery.add_house(random_house)
    create_cable(random_house, (new_battery.row, new_battery.column))

    # Add new cables to house dictionary
    random_house.house_dict["cables"] = random_house.str_cables
    
    index_new = district.output.index(new_battery.battery_dict)
    dictionary_new = random_house.house_dict

    district.output[index_new]["houses"].append(dictionary_new)
    
    district.output[0] = {"district": district.district, f"{costs_type}": return_total_cost(district)}

    output = district.return_output()

    return district.output

    
def return_penalty(battery: Battery) -> float:
    """ Return the penalty for a given battery object
    Every capacity surplus is +1
    Params:
        battery     (Battery): Battery object in district
    Returns:
        (float) penalty associated with battery capacity
    """
    
    penalty = 0
    
    capacity = battery.return_capacity()
    # If capacity is negative, then we assign a penalty
    if capacity < 0:
        penalty = abs(capacity)
        
    return penalty
    
def return_total_cost(district: District) -> float:
    """ Return the total cost associated with district
    Adds both the cost and the penalties
    Params:
        district    (District): District object
    Returns:
        (float) cost of district 
    """
    
    penalty_cost = 0
    
    for battery in district.batteries:
        penalty_cost += return_penalty(battery)
        
    total_cost = district.return_cost() + penalty_cost
    
    return total_cost
    
def one_change_iteration(district: District) -> District:
    """ Run one iteration of applying a random change
    Switches change back when cost has worsened.
    Params:
        connection_dict    (dict): dictionary where houses are keys and batteries values
    Returns:
        (District) either altered or original district object
    """
    
    # Initialize a random district configuration
    random_start_state(district)
    output = copy.deepcopy(district.return_output())
    old_cost = return_total_cost(district)
    new_output = random_change(district, "costs-own")
    new_cost = return_total_cost(district)
    
    if new_cost < old_cost:
        output = new_output
        print('true')
    

    return output
    
    
def one_entire_iteration() -> None:
    """ Run one iteration of hill_climber
    Chooses random begin state.
    Params:
        None, calls upon one_change_iteration()
    Returns:
        none
        alters connection_dict only when cost has lowered multiple times
    """
    return