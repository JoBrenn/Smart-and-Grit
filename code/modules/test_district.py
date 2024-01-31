""" Tests for District class.

File:           test_district.py
Tested file:    district.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 31/01/24 (31/01/24)

Description:
Tests to check the functionality of different parts of the District class.

Usage:  python3 -m pytest code/modules
    NOTE: run from root of depository
"""
from code.modules.district import District

def test_load_houses_batteries():
    """ Here we test that all houses and batteries
        in the district are loaded
    """

    district = District(1, "costs-own")
    assert len(district.houses) == 150
    assert len(district.batteries) == 5

def test_return_cost():
    """ Here we test the return_cost function
        from the District class
    """

    district = District(2, "costs-own")
    assert district.return_cost() == 25000

    # Add a cable segment to one house
    house_0 = district.houses[0]
    house_0.cables = [(1,1), (1,2)]
    battery_0 = district.batteries[0]
    battery_0.add_house(house_0)
    assert district.return_cost() == 25009
