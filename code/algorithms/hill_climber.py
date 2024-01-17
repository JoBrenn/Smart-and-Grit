"""Hill Climber with constraint relaxation where penalty is equal to capacity surplus"""

def random_assignment(batteries: list, houses: list) -> dict:
    """ Randomly assigns houses to batteries, not taking capacity into account
        Adds this to dictionary with house as key and battery as value
        post: returns dictionary"""
        
    """ Randomly assign houses to batteries, not taking capacity into account
    Creates dictionary, where houses are keys and batteries values
    Params:
        batteries    (list): list of batteries in district
    Returns:
        none
        list of battery objects is initialized
    """

    connection_dict = {}
    for house in houses:
        connection_dict[house] = random.choice(batteries)

    return connection_dict