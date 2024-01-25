""" Module of simulated annealing class

File: simulatedannealing.py

Author:    Kathy Molenaar

Date: 23/01/24

Description:    This simulatedannealing class runs the HillClimber algorithm on a given district,
                where changes have been made to make it a simulatedannealing algorithm.

Usage:  from code.algorithms.simulatedannealing import Simmulatedannealing
"""

from .hill_climber import HillClimber
from code.modules.district import District

import math
import random
import copy

class Simmulatedannealing(HillClimber):
    """ Simmulatedannealing algorithm class

    Methods:
        linear_temperature_change():    linearly alters the temperature
        one_change_iteration():     one iteration of changing random house-battery connection
        one_switch_iteration():     one iteration of swapping two random house-battery connections
        one_entire_iteration():     one iteration of choosing random state and making lots of changes
    """
    
    def __init__(self, district: District, iterations: int, temperature: float = 100):
        """ Initialize Simmulatedannealing
        Params:
            district    (District): district upon which we want to apply simulatedannealing
            iterations  (int):      number of iterations (small changes) we want to run each time
            temperature (float):    begin temperature of our model
        """
        # Use init of the Hillclimber class
        super().__init__(district)
        
        # Starting temperature
        self.temp_0 = temperature
        # Current temperature
        self.temp = temperature
        
        # Initialize iterations
        self.iterations = 1
        self.iterations_total = iterations
        
    def linear_temperature_change(self) -> None:
        """ Linearly alter the temperature
        Becomes zero when all iterations have passed
        Returns:
            none
            alters self.temp
        """
        
        self.temp = self.temp_0 - (self.temp_0 / self.iterations_total) * self.iterations
        
    def one_change_iteration(self, district: District) -> District:
        """ Run one iteration of applying a random change
        Allow change with probability 2**(old_cost - new_cost)/self.temp
        Params:
            district    (District): District object
        Returns:
            (District) either altered or original district
        """
        
        old_district = copy.deepcopy(district)
        old_cost = self.return_total_cost(district)
        # Apply a random change
        new_district = self.random_change(district, "costs-own")
        new_cost = self.return_total_cost(district)
        
        # Minimize value, so new minus old
        cost_difference = old_cost - new_cost
        print(cost_difference)
        
        if cost_difference == 0:
            self.linear_temperature_change()
            return old_district
        # When temperature zero return old 
        elif self.temp == 0:
            self.linear_temperature_change()
            return old_district
        else:
            #print(self.temp)
            # Determine the probability
            probability = 2**(cost_difference / self.temp)
            # Change state with probability
            if random.random() < probability:
                # Update temperature
                self.linear_temperature_change()
                return new_district
            
        # Update temperature
        self.linear_temperature_change()
        
        return old_district
    
    def one_switch_iteration(self, district: District) -> District:
        """ Run one iteration of applying a random switch
        Allow change with probability 2**(old_cost - new_cost)/self.temp
        Params:
            district    (District): District object
        Returns:
            (District) either altered or original district
        """
        
        old_district = copy.deepcopy(district)
        output = copy.deepcopy(district.return_output())
        old_cost = self.return_total_cost(district)
        # Apply a random change
        new_district = self.random_switch(district, "costs-own")
        new_cost = self.return_total_cost(district)
        
        # Minimize value
        cost_difference = old_cost - new_cost
        print(cost_difference)
        
        # Make sure you cannot go from good solution to non solution
        if self.check_valid(old_district) is True and self.check_valid(new_district) is False:
            self.linear_temperature_change()
            return old_district
            
        #if cost_difference == 0:
        #    self.linear_temperature_change()
        #    return old_district
        if self.temp == 0:
            self.linear_temperature_change()
            return old_district
        else:
            #print(self.temp)
            # Determine the probability
            probability = 2**(cost_difference / self.temp)
            # Change state with probability
            if random.random() < probability:
                # Update temperature
                self.linear_temperature_change()
                return new_district
            
        # Update temperature
        self.linear_temperature_change()
        
        return old_district
        
    def one_entire_iteration(self, district: District, N: int) -> District:
        """ Run one iteration of simulated annealing when true go over to switch change
        Chooses random begin state.
        Stops when N times not improved or after self.iterations
        Params:
            district    (District): District object
            N           (int):      stop when N times not improved or after self.iterations
        Returns:
            (District) district configuration with lowest found cost 
        """
        
        # Make copy of empty district, such that always start with empty
        district_empty = copy.deepcopy(district)
        
        # Initialize a random district configuration
        district_work = copy.deepcopy(self.random_start_state(district_empty))

        unchanged_count = 0
        
        for iteration in range(self.iterations_total + 1):
            self.iterations += 1
            #print(self.iterations)
            # Stop when the state hasn't improved N times
            if unchanged_count == N - 1:
                # Reset iterations
                self.iterations = self.iterations_total
                return district_work
            else:
                previous_district = copy.deepcopy(district_work)
                # Go over to switch when we have a valid solution
                if self.check_valid(previous_district) is True:
                    district_work = self.one_switch_iteration(district_work)
                else:
                    district_work = self.one_change_iteration(district_work)
                #print(self.return_total_cost(previous_district))
                #print(self.return_total_cost(district_work))
                # If output is unchanged, add one to count
                if previous_district.return_output() == district_work.return_output():
                    unchanged_count += 1
                else:
                    unchanged_count = 0
                #print(self.check_valid(district_work))
                
        # Reset iterations and temperature
        self.iterations = 0
        self.temp = self.temp_0
        
        return district_work
    