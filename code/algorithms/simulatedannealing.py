from .hill_climber import HillClimber
from code.modules.district import District

import math
import random
import copy

class Simmulatedannealing(HillClimber):
    
    def __init__(self, district: District, iterations: int, temperature: float = 100):
        # Use init of the Hillclimber class
        super().__init__(district)
        
        # Starting temperature
        self.temp_0 = temperature
        # Current temperature
        self.temp = temperature
        
        self.iterations = 0
        self.iterations_total = iterations
        
    def linear_temperature_change(self) -> None:
        """ Temperature becomes zero when all 1000 unchanged iterations have passed"""
        # Reset temperature after we are done with one run of HillClimber
        if self.temp == 0:
            self.temp = self.temp_0
        else:
            self.temp = self.temp_0 - (self.temp_0 / self.iterations_total)*self.iterations
        #print(self.temp)
        

        
    """ 
        Alter all functions where we accept a new solution or not
    """
    def one_change_iteration(self, district: District) -> District:
        """ Run one iteration of applying a random change
        Switches with probability.
        Params:
            district    (District): District object
        Returns:
            (list) either altered or original district output list
        """
        
        old_district = copy.deepcopy(district)
        old_cost = self.return_total_cost(district)
        # Apply a random change
        new_district = self.random_change(district, "costs-own")
        new_cost = self.return_total_cost(district)
        
        # Minimize value, so new minus old
        cost_difference = old_cost - new_cost
        #print(cost_difference)
        
        if cost_difference == 0:
            self.linear_temperature_change()
            return old_district
        elif self.temp == 0:
            self.linear_temperature_change()
            return old_district
        else:
            # When the new cost is lower garantee a state change 
            #if new_cost < old_cost:
                #self.linear_temperature_change()
                #return new_district
            # If cost equal or higher accept it with probability
            #else:
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
        Switches change back when cost has worsened.
        Params:
            district    (District): District object
        Returns:
            (list) either altered or original district output list
        """
        
        old_district = copy.deepcopy(district)
        output = copy.deepcopy(district.return_output())
        old_cost = self.return_total_cost(district)
        # Apply a random change
        new_district = self.random_switch(district, "costs-own")
        new_cost = self.return_total_cost(district)
        
        # Minimize value, so new minus old
        cost_difference = old_cost - new_cost
        
        # Make sure you cannot go from good solution to non solution
        if self.check_valid(old_district) is True and self.check_valid(new_district) is False:
            self.linear_temperature_change()
            return old_district
            
        if cost_difference == 0:
            self.linear_temperature_change()
            return old_district
        elif self.temp == 0:
            self.linear_temperature_change()
            return old_district
        else:
            # When the new cost is lower garantee a state change 
            #if new_cost < old_cost:
                #self.linear_temperature_change()
                #return new_district
            # If cost equal or higher accept it with probability
            #else:
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
        
    def one_entire_iteration_switch(self, district: District, N: int) -> District:
        """ Run one iteration of hill_climber when true go over to switch change
        Chooses random begin state.
        Params:
            district    (District): District object
            N           (int):      Stop when N times not improved
        Returns:
            none
        """
        
        # Make copy of empty district, such that always start with empty
        district_empty = copy.deepcopy(district)
        
        # Initialize a random district configuration
        district_work = copy.deepcopy(self.random_start_state(district_empty))

        unchanged_count = 0
        
        for iteration in range(self.iterations_total - 1):
            self.iterations += 1
            print(self.iterations)
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
                print(self.return_total_cost(previous_district))
                print(self.return_total_cost(district_work))
                # If output is unchanged, add one to count
                if previous_district.return_output() == district_work.return_output():
                    unchanged_count += 1
                else:
                    unchanged_count = 0
                print(self.check_valid(district_work))
        # Reset iterations
        self.iterations = 0
        
        return district_work
    