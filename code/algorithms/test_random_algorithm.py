""" Tests for random_algorithm file.

File:           test_random_algorithm.py
Tested file:    random_algorithm.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 31/01/24 (31/01/24)

Description:
Tests to check the functionality of testable parts of the 
random algorithm.

Usage:  python3 -m pytest code/algorithms/
    NOTE: run from root of depository
"""

from .random_algorithm import random_assignment_capacity
from code.modules.battery import Battery
from code.modules.district import District

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
