from .hill_climber import HillClimber
from code.modules.district import District

import math
import random
import copy

class Simmulatedannealing(HillClimber):
    
    def __init__(self, district: District, temp: float):
        # Use init of the Hillclimber class
        super().__init__(district)
        
        # Starting temperature
        self.temp_0 = temp
        # Current temperature
        self.temp = temp
        
    def linear_temperature_change(self) -> None:
        """ Temperature goes to zero when all iterations have passed"""
        self.temp = (self.temp_0 / self.iterations)
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
        # Make sure temperature is not zero
        assert self.temp != 0
        
        # Add iteration 
        self.iterations += 1
        
        old_district = copy.deepcopy(district)
        old_cost = self.return_total_cost(district)
        # Apply a random change
        new_district = self.random_change(district, "costs-own")
        new_cost = self.return_total_cost(district)
        
        # Minimize value, so new minus old
        cost_difference = new_cost - old_cost
        print(cost_difference)
        
        if cost_difference == 0:
            self.linear_temperature_change()
            return new_district
            
        else:
            # Determine the probability
            probability = math.exp(-cost_difference / self.temp)
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
        
        # Add iteration 
        self.iterations += 1
        
        old_district = copy.deepcopy(district)
        output = copy.deepcopy(district.return_output())
        old_cost = self.return_total_cost(district)
        # Apply a random change
        new_district = self.random_switch(district, "costs-own")
        new_cost = self.return_total_cost(district)
        
        # Minimize value, so new minus old
        cost_difference = new_cost - old_cost
        
        # Make sure you cannot go from good solution to non solution
        if self.check_valid(old_district) is True and self.check_valid(new_district) is False:
            self.linear_temperature_change()
            return old_district
            
        if cost_difference == 0:
            self.linear_temperature_change()
            return new_district
            
        else:
            # Determine the probability
            probability = math.exp(-cost_difference / self.temp)
            # Change state with probability
            if random.random() < probability:
                # Update temperature
                self.linear_temperature_change()
                return new_district
            
        # Update temperature
        self.linear_temperature_change()
        
        return old_district
    