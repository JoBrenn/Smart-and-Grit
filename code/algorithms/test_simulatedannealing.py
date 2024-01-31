""" Tests for Simulatedannealing class.

File:           test_simulatedannealing.py
Tested file:    simulatedannealing.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 31/01/24 (31/01/24)

Description:
Tests to check the functionality of testable parts of the 
Simulatedannealing algorithm class.

Usage:  python3 -m pytest code/algorithms/
    NOTE: run from root of depository
"""

from .simulatedannealing import Simulatedannealing
from code.modules.district import District

def test_temperature_change():
    """ Here we test that the linear temperature change
        works the way we want it to
    """

    district = District(1, "costs-own")
    simul = Simulatedannealing(district, 100, 10)
    
    assert simul.temp == 10

    begin_temp = simul.temp_0
    simul.iterations = 1

    simul.linear_temperature_change()

    assert simul.temp == 9.9
    
    simul.iterations = 2
    simul.linear_temperature_change()

    assert simul.temp == 9.8
