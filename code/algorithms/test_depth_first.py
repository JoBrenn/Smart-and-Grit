""" Tests for depth first algorithm.

File:           test_manhattan_distance.py
Tested file:    manhattan_distance.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 31/01/24 (31/01/24)

Description:
Tests to check the functionality of testable parts of the 
depth first algorithm.

Usage:  python3 -m pytest code/algorithms/
    NOTE: run from root of depository
"""

from .depth_first import DepthFirst
from code.modules.district import District

def test_valid_capacity():
    """ Here we test that the valid capacity
        check works as wished
    """

    district = District(2, "costs-own")
    df = DepthFirst(district)

    battery = district.batteries[0]
    battery_cap = battery.capacity

    assert df.valid_capacity(district) is True

    # Assign all houses to same battery
    for house in district.houses:
        battery.add_house(house)

    assert df.valid_capacity(district) is False
