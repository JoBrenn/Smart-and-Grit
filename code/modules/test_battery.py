""" Tests for Battery class.

File:           test_battery.py
Tested file:    battery.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 31/01/24 (31/01/24)

Description:
Tests to check the functionality of different parts of the Battery class.

Usage:  python3 -m pytest code/modules
    NOTE: run from root of depository
"""
from code.modules.battery import Battery
from code.modules.house import House

def test_sequence_of_methods():
    """ Here we test that a house
        is added and deleted correctly
        and the capacity responds correctly.
    """

    battery = Battery(1, (2,2), 3, 1000)
    house = House(1, (1,1), 1)
    battery.add_house(house)
    assert house in battery.houses
    assert battery.left_over_capacity == 2

    battery.delete_house(house)
    assert house not in battery.houses
    assert battery.left_over_capacity == 3
    assert battery.return_capacity() == 3


def test_convert_coordinate_correct():
    """ Test if coordinates are converted correctly. """
    battery = Battery(1, (2,2), 3, 1000)
    assert battery.convert_coordinate_to_str((2,2)) == "2,2"

def test_return_capacity():
    """ Test if capacity is returned correctly. """
    battery = Battery(1, (2,2), 2500, 1000)
    assert battery.return_capacity() == 2500

def test_house_correct_capacity():
    """ Test if correct left over capacity is returned. """
    battery = Battery(1, (2,2), 2500, 1000)
    house = House(1, (1,1), 500)
    battery.add_house(house)
    assert battery.return_capacity() == 2000
