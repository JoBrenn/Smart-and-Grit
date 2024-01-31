""" Module of simulated annealing class

File: simulatedannealing.py

Author:    Kathy Molenaar

Date: 23/01/24 (31/01/24)

Description:
This class runs the HillClimber algorithm on a given district,
where changes have been made to make it a simulatedannealing algorithm.

Usage:  from code.algorithms.simulatedannealing import Simmulatedannealing
"""

from .hill_climber import HillClimber
from code.modules.district import District

from random import random
from copy import deepcopy


class Simulatedannealing(HillClimber):
    """ Simulatedannealing algorithm class

    Methods:

    linear_temperature_change():linearly alters the temperature
    one_change_iteration():     changing random house-battery connection
    one_switch_iteration():     swapping two random house-battery connections
    one_entire_iteration():     one iteration of starting with random state
    """

    def __init__(self, district: District, iterations: int = 10000,
                 temperature: float = 4100):
        """ Initialize Simmulatedannealing
        Params:
            district    (District): district
            iterations  (int):      number of small changes we want to run
            temperature (float):    begin temperature of our model
        """

        # Use init of the HillClimber class
        super().__init__(district)

        # Starting temperature
        self.temp_0 = temperature

        # Current temperature
        self.temp = temperature

        # Initialize iterations
        self.iterations = 0
        self.iterations_total = iterations

    def linear_temperature_change(self) -> None:
        """ Linearly alter the temperature
        Becomes zero when all iterations have passed
        Returns:
            none
            alters self.temp
        """

        self.temp = self.temp_0 -\
            (self.temp_0 / self.iterations_total) * self.iterations

    def one_change_iteration(self, district: District) -> District:
        """ Run one iteration of applying a random change
        Allow change with certain probability
        Params:
            district    (District): District object
        Returns:
            (District) either altered or original district
        """

        old_district = deepcopy(district)
        old_cost = self.return_total_cost(district)

        # Apply a random change
        new_district = self.random_change(district, "costs-own")
        new_cost = self.return_total_cost(district)

        # Minimize value, so new minus old
        cost_difference = old_cost - new_cost

        if cost_difference == 0:
            self.linear_temperature_change()
            return old_district

        # When temperature zero return old
        elif self.temp == 0:
            self.linear_temperature_change()
            return old_district
        else:
            # Determine the probability
            probability = 2**(cost_difference / self.temp)

            # Change state with probability
            if random() < probability:
                # Update temperature
                self.linear_temperature_change()
                return new_district

        # Update temperature
        self.linear_temperature_change()

        return old_district

    def one_switch_iteration(self, district: District) -> District:
        """ Run one iteration of applying a random switch
        Allow change with certain probability
        Params:
            district    (District): District object
        Returns:
            (District) either altered or original district
        """

        old_district = deepcopy(district)
        old_cost = self.return_total_cost(district)

        # Apply a random change
        new_district = self.random_switch(district, "costs-own")
        new_cost = self.return_total_cost(district)

        # Minimize value
        cost_difference = old_cost - new_cost

        # Make sure you cannot go from good solution to non solution
        if self.check_valid(old_district) is True\
           and self.check_valid(new_district) is False:
            self.linear_temperature_change()
            return old_district

        if self.temp == 0:
            self.linear_temperature_change()
            return old_district
        else:
            # Determine the probability
            probability = 2**(cost_difference / self.temp)

            # Change state with probability
            if random() < probability:
                # Update temperature
                self.linear_temperature_change()
                return new_district

        # Update temperature
        self.linear_temperature_change()

        return old_district

    def one_entire_iteration(self, district: District, N: int) -> District:
        """ Run one iteration of simulated annealing
        Chooses random begin state.
        Stops after self.iterations, since N same iterations will never happen
        Params:
            district    (District): District object
            N           (int):      maximum repeat number
        Returns:
            (District) district configuration with lowest found cost
        """

        # Make copy of empty district, such that always start with empty
        district_empty = deepcopy(district)

        # Initialize a random district configuration
        district_work = deepcopy(self.random_start_state(district_empty))

        unchanged_count = 0

        for iteration in range(self.iterations_total + 1):
            self.iterations += 1

            previous_district = deepcopy(district_work)

            # Go over to switch when we have a valid solution
            if self.check_valid(previous_district) is True:
                district_work = self.one_switch_iteration(district_work)
            else:
                district_work = self.one_change_iteration(district_work)

        # Reset iterations and temperature
        self.iterations = 0
        self.temp = self.temp_0

        return district_work
