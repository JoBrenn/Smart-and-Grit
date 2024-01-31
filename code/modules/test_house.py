""" Tests for House class.

File:           test_house.py
Tested file:    house.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 31/01/24 (31/01/24)

Description:
Tests to check the functionality of different parts of the House class.

Usage:  python3 -m pytest code/modules/
    NOTE: run from root of depository
"""

from code.modules.house import House

def test_add_and_delete():
    """ Here we test that a cable coordinate
        is added and deleted correctly and the
        right length is returned
    """
    house = House(1, (1,1), 1)
    house.add_cable_segment((1,2))
    assert house.str_cables == ["1,2"]
    assert house.cables == [(1,2)]
    house.add_cable_segment((1,3))
    assert house.return_cable_length() == 1
    house.delete_cables()
    assert len(house.str_cables) == 0
    assert len(house.cables) == 0
    assert house.return_cable_length() == -1

def test_house_id():
    house = House(1, (1,1), 1)
    assert house.house_id == 1

def test_convert_coordinate_correct():
    """ Test if coordinates are converted correctly. """
    house = House(1, (1,1), 1)
    assert house.convert_coordinate_to_str((1,1)) == "1,1"

def test_return_cable_length():
    """ Test if cable length is returned correctly.
    Cables are connected between points. 3 points is 2 cables
    """
    house_coords = 1,1
    house = House(1, house_coords, 1)
    # Add house
    house.add_cable_segment(house_coords)

    # Add two cables coords
    house.add_cable_segment((1,2))
    house.add_cable_segment((2,2))

    assert house.return_cable_length() == 2

def test_delete_cables():
    house = House(1, (1,1), 1)
    house.add_cable_segment((1,2))
    house.add_cable_segment((2,2))
    house.delete_cables()
    assert house.return_cable_length() == -1
