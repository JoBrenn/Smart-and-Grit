from .random_algorithm import random_assignment_capacity, Battery, District

def test_capacity():
    """ Here we test that for random assignment 
        where we take capacity into account, the
        capacity is indeed not exceeded
    """

    district = District(3, "costs-own")

    dictionary = random_assignment_capacity(district)

    batteries = list(dictionary.values())

    for battery in batteries:
        assert battery.left_over_capacity >= 0
