""" Depth first algorithm

File: depth_first.py

Author:    Jesper Vreugde

Date: 26/01/24

Description:    A depth first algorithm that goes through each possible
                configuration of houses being assigned to batteries.
                Runs until a specified depth(assigned houses) which is set at
                5 as the default. Prunes the branches where the sum of the output
                of each house assigned to a battery exceeds the capacity of that 
                battery.

Usage:  from code.algorithms.depth_first import DepthFirst
"""

import copy

from code.modules.district import District
from code.modules.district import Battery
from code.modules.district import House
from code.algorithms.manhattan_distance import *
from code.visualisation.visualize import plot_output
from random import shuffle

class DepthFirst:
    """ DepthFirst algorithm classes

    Methods:
        run():                      runs the depth first algorithm                   
        return_next_state()         returns the next item in the stack
        valid_capacity(district)    determines whether each battery has exceeded their capacity
    """
    def __init__(self, district: District, depth: int = 5)-> None:
        """ Initialize Depth First class
        Params:
            district    (District): Distrisct object
            depth       (int): Tha maximum depth that the Depth search tree
                               will be. Set at the max as default
        Returns
            None"""

        self.depth = depth
        self.states = [district]
        self.house_num = len(district.houses)
        # Randomize
        shuffle(self.states[0].houses)

    def run(self) -> District:
        """ Runs the depth first algorithm

            Returns
                A district object that has the lowest found cost state"""
        # Set the initial costs to be the 
        lowest_costs = float("inf")
        lowest_state = None

        # Loop over stack until it is empty
        while len(self.states) > 0:
            state = self.return_next_state()

            # Prunes branches where a battery's capacity has been exceeded 
            if self.valid_capacity(state) == True:

                # Will run if the 
                if self.house_num - len(state.houses) < self.depth:
                    print(self.house_num - len(state.houses))
                    house = state.houses.pop()
                    
                    for n, battery in enumerate(state.batteries):
                        child = copy.deepcopy(state)
                        house_add = copy.deepcopy(house)
                        create_cable(house_add, (battery.row, battery.column))
                        child.batteries[n].add_house(house_add)
                        self.states.append(child)
                        

                # If not, a state at the desired depth has been found and can be compared
                else:
                    state.district_dict[f"{state.costs_type}"] = state.return_cost()

                    if state.district_dict[state.costs_type] < lowest_costs:
                        lowest_costs = state.district_dict[state.costs_type]
                        lowest_costs_state = copy.deepcopy(state)

        return lowest_costs_state


    def return_next_state(self) -> District:
        """ Returns next state in the stack
            Returns:
                a District object at the end of the states list
        """
        return self.states.pop()

    def valid_capacity(self, district) -> bool: 
        """ Determines whether the district is a valid solution for
            the depth that was given
            Returns: 
                a bool that that determines whether or not a battery
                has exceeded its maximum capacity

        """
        for battery in district.batteries:
            if battery.left_over_capacity < 0:
                return False
        return True
