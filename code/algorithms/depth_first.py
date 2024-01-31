""" Depth first algorithm

File: depth_first.py

Author:    Jesper Vreugde

Date: 26/01/24

Description:
A depth first algorithm that goes through each possible
configuration of houses being assigned to batteries.
Runs until a specified depth(assigned houses) which is set at
5 as the default. Prunes the branches where the sum of the output
of each house assigned to a battery exceeds the capacity of that
battery.

Usage:  from code.algorithms.depth_first import DepthFirst
"""

from copy import deepcopy
from random import shuffle
from csv import writer

from code.modules.district import District
from code.algorithms.manhattan_distance import create_cable


class DepthFirst:
    """ DepthFirst algorithm classes

    Methods:
        run():                      run the depth first algorithm
        return_next_state()         return the next item in the stack
        valid_capacity(district)    determine whether each
                                    battery has exceeded their capacity
        state_to_csv(district)      saves costs of state to csv file
    """

    def __init__(self, district: District, depth: int = 5) -> None:
        """ Initialize Depth First class
        Params:
            district    (District): Distrisct object
            depth       (int): Tha maximum depth that the Depth search tree
                               will be. Set at the max as default
        Returns:
            none
       """

        self.depth = depth
        self.states = [district]
        self.house_num = len(district.houses)

        # Randomize
        shuffle(self.states[0].houses)

    def run(self) -> District:
        """ Runs the depth first algorithm
        Returns:
            A district object that has the lowest found cost state
        """

        # Set the initial costs
        lowest_costs = float("inf")
        lowest_costs_state = None

        # Loop over stack until it is empty
        while len(self.states) > 0:
            state = self.return_next_state()

            # Prunes branches where a battery's capacity has been exceeded
            if self.valid_capacity(state) is True:# or self.valid_capacity(state) is False:

                if self.house_num - len(state.houses) < self.depth:
                    house = state.houses.pop()

                    for n, battery in enumerate(state.batteries):
                        child = deepcopy(state)
                        house_add = deepcopy(house)
                        create_cable(house_add, (battery.row, battery.column))
                        child.batteries[n].add_house(house_add)
                        child.assigned_houses += 1
                        
                        self.states.append(child)

                # A state at the desired depth has been found and can compare
                else:
                    state.district_dict[f"{state.costs_type}"] \
                        = state.return_cost()
                    
                    self.state_to_csv(state)

                    if state.district_dict[state.costs_type] < lowest_costs:
                        lowest_costs = state.district_dict[state.costs_type]
                        lowest_costs_state = deepcopy(state)

                print(f"{len(state.houses)} | {state.assigned_houses} | {len(self.states)}")

        return lowest_costs_state

    def return_next_state(self) -> District:
        """ Returns next state in the stack
        Returns:
            a District object at the end of the states list
        """

        return self.states.pop()

    def valid_capacity(self, district: District) -> bool:
        """ Determines whether the district is a valid solution for
            the depth that was given
        Params:
            district    (District): district object
        Returns:
            a bool that that determines whether or not a battery
            has exceeded its maximum capacity
        """

        for battery in district.batteries:
            if battery.left_over_capacity < 0:
                return False

        return True


    def state_to_csv(self, state: District) -> None:
        """ Appends state costs to a csv
        Params:
            state    (District): district object
        Returns:
            appends state to csv file containing a the costs
            of all the final states in the run
        """

        with open("output/csv/depth.csv", "a", newline="") as outfile:
            writer = csv.writer(outfile, delimiter=';')
            writer.writerow([state.return_cost()])
