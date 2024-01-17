import random
from code.modules.battery import Battery
from code.modules.district import District

"""Hill Climber with constraint relaxation where penalty is equal to capacity surplus"""

def random_assignment(batteries: list, houses: list) -> dict:     
    """ Randomly assign houses to batteries, not taking capacity into account
    Creates dictionary, where houses are keys and batteries values
    Params:
        batteries    (list): list of batteries in district
        houses       (list): list of houses in district
    Returns:
        (dict) houses as keys and batteries as values
    """

    connection_dict = {}
    for house in houses:
        connection_dict[house] = random.choice(batteries)

    return connection_dict
    
def random_change(batteries: list, connection_dict: dict) -> dict:
    """ Randomly change one house-battery connection
    Alters this change in the connection dictionary
    Params:
        batteries          (list): list of batteries in district
        connection_dict    (dict): dictionary where houses are keys and batteries values
    Returns:
        (dict) dictionary where houses are keys and batteries values, with small change
    """
    
    # Get random house from the keys of dictionary
    random_house = random.choice(list(connection_dict.keys()))
    # Change dictionary value for a new random choice in batteries
    connection_dict[random_house] = random.choice(batteries)
    
    return connection_dict
    
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