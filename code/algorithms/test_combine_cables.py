""" Tests for combine cables.

File:           test_combine_cables.py
Tested file:    combine_cables.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 31/01/24 (31/01/24)

Description:
Tests to check the functionality of testable parts of combining
cables in a district configuration.

Usage:  python3 -m pytest code/algorithms/
    NOTE: run from root of depository
"""

from .combine_cables import combine_district

def test_lower_cost():
    """ Here we test that combining the 
        cables does indeed result in 
        lower costs
    """

    # Simple 2 houses 1 battery output
    output = [{"district": 1, "costs-own": 5054}, {"location": "1,1",
               "capacity": 1500, "houses": [{"location": "2,2", "output": 50,
                                             "cables": ["2,2", "2,1", "1,1"]},
                                            {"location": "4,2", "output": 50,
                                             "cables": ["4,2", "4,1", "3,1",
                                                        "2,1", "1,1"]}]}]

    houses = combine_district(output)[1][1]["houses"]
    cost = 5000
    for house in houses:
        cost += (len(house["cables"]) - 1) * 9
    
    assert cost <= 25054
