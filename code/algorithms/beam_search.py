""" Beam Search algorithm.

File: beam_search.py

Authors:    Jonas Brenninkmeijer

Date: 22/01/24 (23/01/24)

Description:    The implementation of a Beam Search (BS) algorithm.
                Beam Search works by selecting the best N (Beam) states
                and pruning the rest. The Beam specified at 1 makes this
                algorithm Greedy, Beam of INF makes it Breadth First.

Usage:  from algorithms.beam_search import BeamSearch
"""
from copy import deepcopy
from random import randint, seed
from .manhattan_distance import create_cable
from code.modules.district import District
from code.modules.district import Battery
from code.modules.district import House


class BeamSearch:

    def __init__(self, district: District, beam: int) -> None:
        """Initialize BeamSearch class
        Params:
            district    (District): District object containing grid information
            beam        (int): The amount of branches to be included in the search.
                                When 1 -> Greedy, when inf -> Breadth First Search
        Returns:
            None
            Initialized BeamSearch object
        """
        # Create deepcopies of (empty) district
        self.district = deepcopy(district)
        self.houses = deepcopy(district.houses)

        # Set Beam
        self.beam = beam

        # Define state with only empty district
        self.states = [self.district]


    def update_states(self) -> None:
        """ Update states of search.

        Update states by connecting the batteries in the current states
        to the randomly selected house.
        Returns:
            None
            Updates self.states
        """
        # Select house for all states to incorporate
        house = self.random_avaliable_house()
        # N_start_states = len(self.states)

        # List to save new states
        new_states = []

        # Create new states for all current states
        for state in self.states:
            # House is connected to all batteries
            for index in range(len(state.batteries)):
                # Deepcopy district and house for new state
                district = deepcopy(state)
                house_new = deepcopy(house)
                battery = district.batteries[index]

                # print("Battery left:", battery.left_over_capacity)
                # print("House output:", house_new.output)


                if battery.left_over_capacity - house_new.output >= 0:
                    battery.add_house(house_new)
                    create_cable(house_new, (battery.row, battery.column))
                    new_states.append(district)

        # print(new_states)

        # Override old with new states
        if new_states:
            self.states = new_states


    def random_avaliable_house(self) -> House:
        """ Remove and return randomly a house for the list of houses.
        Returns:
            House object, removed from self.houses
        """
        random_index = randint(0,len(self.houses)-1)
        return self.houses.pop(random_index)

    def select_best(self) -> None:
        """ Select states with lowest costs.
        Amount of selected states depends on beam.
        Returns:
            None
            Keeps best states, removes rest
        """
        # List for costs of states
        costs = []

        # Returning the cost of a state and appending
        for state in self.states:
            costs.append(state.return_cost())

        # Zip the costs and states together in a list
        # Sort list according to the cost
        costs_states = list(zip(costs, self.states))
        sorted_states = sorted(costs_states, key = lambda x: x[0])

        # Keep the states from the start of the list until beam index
        self.states = [state for index, state in sorted_states[0:self.beam]]
        # print("Selected best. Current best:", self.states[0].return_cost())


    def run(self) -> District | None:
        """ Run the Beam Search algorithm.
        Searches the states with a width of the beam.
        CAUTION: Might take up a lot of time and space, depending on the beam.
        Returns:
            None
        """
        # While there are still avaliable houses
        while self.houses:
            # Update states
            self.update_states()

            # If there are more states than the beam:
            # select best
            if len(self.states) > self.beam:
                self.select_best()

        self.filter_valid_states()

        # Print the first five best states
        # print()
        # for index, state in enumerate(self.states):
        #     if index > 5:
        #         break
        #     print(f"State {index+1} cost: {state.return_cost()}")
        #
        # total = 0
        # for index, state in enumerate(self.states):
        #     if index > 5:
        #         break
        #     for battery in state.batteries:
        #         total += len(battery.houses)
        #     print(f"State {index+1} houses: {total}")
        #     total = 0

        # print(self.states)
        if self.states:
            print(f"At beam {self.beam} found:", self.states[0].return_cost())
            return self.states[0]
        else:
            return

    def filter_valid_states(self) -> None:
        valid_states = []
        included_houses = 0
        for state in self.states:
            for battery in state.batteries:
                included_houses += len(battery.houses)
            if included_houses == 150:
                valid_states.append(state)
            included_houses = 0
        self.states = valid_states
