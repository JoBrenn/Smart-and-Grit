""" Module of HillClimber class

File: hill_climber.py

Author:    Kathy Molenaar

Date: 19/01/24

Description:

This HillClimber class runs the HillClimber algorithm on a given district
Here we make use of constraint relaxation; we start with a random state.
First our small change consists of choosing one random house and re-assigning
it to a random battery. When we have reached a good solution
we change our small change to choosing two random houses and swapping their battery
connections. This change is only accepted when the state remains a good solution.

Usage:  from code.algorithms.hill_climber import HillClimber
"""

from code.modules.district import District
from code.modules.district import Battery
from code.modules.district import House
from code.algorithms.manhattan_distance import get_cable_points, create_cable

from random import choice
from copy import deepcopy, copy
import csv


class HillClimber:
    """ HillClimber algorithm class

    Methods:
        random_start_state():       create random start configuration of district
        random_change():            change random house-battery connection
        random_switch():            swap two random house-battery connections
        return_penalty():           return battery capacity exceedance penalty
        return_total_cost():        return cost of district plus penalty
        check_valid():              check whether district configuration is valid
        one_change_iteration():     one iteration of changing
        one_switch_iteration():     one iteration of swapping
        one_entire_iteration():     one iteration of hill climber
        run_hill_climber():         runs one entire iteration n times
    """
    
    
    def __init__(self, district: District, iterations: int = 100000) -> None:
        """ Initialize HillClimber
        Params:
            district    (District): district upon which we want to apply HillClimber
        """
        self.district_empty = deepcopy(district)
        self.district = deepcopy(district)
        self.total_cost = self.return_total_cost(district)
        
        # Initialize iterations
        self.iterations = 0
        self.iterations_total = iterations
    
    def random_start_state(self, district: District) -> District:
        """ Randomly assign houses to batteries, not taking capacity into account
        Creates connections via Manhattan distance
        Params:
            district    (District): district object
        Returns:
            (District) random configurated District object
        """
        
        # Take the empty district as initial configuration
        for house in district.houses: 
            battery = choice(district.batteries)
            # Add the house to the battery connection
            battery.add_house(house)
            create_cable(house, (battery.row, battery.column))
        district.district_dict[f"{district.costs_type}"] = district.return_cost()

        return district

    def random_change(self, district: District, costs_type: str) -> District:
        """ Randomly change one house-battery connection
        Alters this change in all relevant structures
        Params:
            district      (District):  district object
            costs_type    (float):     indication of costs-shared or costs-own
        Returns:
            (District) altered district object
        """
        
        # Get random house from district
        random_house = choice(district.houses)
        dictionary = deepcopy(random_house.house_dict)

        # Find old battery connection
        for battery in district.batteries:
            if random_house in battery.houses:
                old_battery = battery
        
        # Delete the house from the battery in output dictionary
        index = district.output.index(old_battery.battery_dict)
        one = deepcopy(district.output[index])
        district.output[index]["houses"].remove(dictionary)

        # Delete house from old battery
        old_battery.delete_house(random_house)
        
        random_house.cables.clear()
        random_house.str_cables.clear()
        
        # Clear cables in house dictionary
        random_house.house_dict["cables"].clear()
                      
        # Determine new random battery
        new_battery = choice(district.batteries)
        # Create new Manhattan cable
        create_cable(random_house, (new_battery.row, new_battery.column))
        
        # Add new cables to house dictionary
        random_house.house_dict["cables"] = random_house.str_cables
        
        # Add house to new battery
        new_battery.add_house(random_house)

        # Add house to battery in output dictionary
        index_new = district.output.index(new_battery.battery_dict)
        dictionary_new = deepcopy(random_house.house_dict)
        
        # Reset first element in dictionary, so that the cost is accurate
        district.output[0] = {"district": district.district,\
                             f"{costs_type}": self.return_total_cost(district)}

        return district

    def random_switch(self, district: District, costs_type: str) -> District:
        """ Randomly switch two house-battery connections
        Alters this change in all relevant structures
        Params:
            district      (District):  district object
            costs_type    (float):     indication of costs-shared or costs-own
        Returns:
            (District) altered district object
        """
        
        # Get random different houses from district
        houses = district.houses.copy()
        random_house_1 = choice(district.houses)
        houses.remove(random_house_1)
        random_house_2 = choice(houses)
        dictionary_1 = deepcopy(random_house_1.house_dict)
        dictionary_2 = deepcopy(random_house_2.house_dict)
        
        # Find batteries connected
        for battery in district.batteries:
            if random_house_1 in battery.houses:
                battery_1 = battery
            if random_house_2 in battery.houses:
                battery_2 = battery
        
        # Delete the houses from the batteries in output dictionary
        index_1 = district.output.index(battery_1.battery_dict)
        index_2 = district.output.index(battery_2.battery_dict)
        district.output[index_1]["houses"].remove(dictionary_1)
        district.output[index_2]["houses"].remove(dictionary_2)
        
        # Delete houses from old batteries
        battery_1.delete_house(random_house_1)
        battery_2.delete_house(random_house_2)
        
        # Delete old cables in House classes
        random_house_1.cables.clear()
        random_house_2.cables.clear()
        random_house_1.str_cables.clear()
        random_house_2.str_cables.clear()
        
        # Clear cables in house dictionaries
        random_house_1.house_dict["cables"].clear()
        random_house_2.house_dict["cables"].clear()
                      
        # Create new Manhattan cables
        create_cable(random_house_1, (battery_2.row, battery_2.column))
        create_cable(random_house_2, (battery_1.row, battery_1.column))
        
        # Add new cables to house dictionary
        random_house_1.house_dict["cables"] = random_house_1.str_cables
        random_house_2.house_dict["cables"] = random_house_2.str_cables
        
        # Add houses to new batteries
        battery_1.add_house(random_house_2)
        battery_2.add_house(random_house_1)

        # Add new cables to house dictionaries
        random_house_1.house_dict["cables"] = random_house_1.str_cables
        random_house_2.house_dict["cables"] = random_house_2.str_cables
        
        # Add house to battery in output dictionary
        index_new_1 = district.output.index(battery_1.battery_dict)
        dictionary_new_2 = random_house_2.house_dict
        index_new_2 = district.output.index(battery_2.battery_dict)
        dictionary_new_1 = random_house_1.house_dict
        
        # Reset first element in dictionary, so that the cost is accurate
        district.output[0] = {"district": district.district,\
                             f"{costs_type}": self.return_total_cost(district)}

        
        return district

        
    def return_penalty(self, battery: Battery) -> float:
        """ Return the penalty for a given battery object
        Every capacity surplus is +10
        Params:
            battery     (Battery): Battery object in district
        Returns:
            (float) penalty associated with battery capacity
        """
        
        penalty = 0
        
        capacity = battery.return_capacity()
        # If capacity is negative, then we assign a penalty
        if capacity < 0:
            penalty = abs(capacity) * 10
          
        return penalty
        
    def return_total_cost(self, district: District) -> float:
        """ Return the total cost associated with district
        Adds both the cost and the penalties
        Params:
            district    (District): District object
        Returns:
            (float) cost of district 
        """
        
        penalty_cost = 0
        
        for battery in district.batteries:
            #print(battery.left_over_capacity)
            penalty_cost += self.return_penalty(battery)
        #print(district.return_cost())
        total_cost = district.return_cost() + penalty_cost
        
        return total_cost

    def check_valid(self, district: District) -> bool:
        """ Check whether found configuration is valid
        Uses comparison of costs with or without penalty
        Params:
            district    (District): District object
        Returns:
            (bool) true when configuration is valid
        """

        for battery in district.batteries:
            if self.return_penalty(battery) != 0:
                return False
        
        return True
        
    def one_change_iteration(self, district: District) -> District:
        """ Run one iteration of applying a random change
        Switches change back when cost has worsened.
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
            
        # Change state when the cost is lower or equal
        if new_cost < old_cost:
            return new_district
            
        return old_district

    def one_switch_iteration(self, district: District) -> District:
        """ Run one iteration of applying a random switch
        Switches change back when cost has worsened.
        Params:
            district    (District): District object
        Returns:
            (District) either altered or original district
        """

        old_district = deepcopy(district)
        output = deepcopy(district.return_output())
        old_cost = self.return_total_cost(district)
        # Apply a random change
        new_district = self.random_switch(district, "costs-own")
        new_cost = self.return_total_cost(district)
        
        # Make sure you cannot go from good solution to non solution
        if self.check_valid(old_district) is True\
        and self.check_valid(new_district) is False:
            return old_district
            
        # Change state when the cost is lower 
        if new_cost < old_cost:
            return new_district
            
        return old_district   

    def one_entire_iteration(self, district: District, N: int) -> District:
        """ Run one iteration of HillClimber
        Chooses random begin state.
        Stops when N times not improved or after self.iterations
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
            # Stop when the state hasn't improved N times
            if unchanged_count == N - 1:
                # Reset iterations
                self.iterations = self.iterations_total
                return district_work
            else:
                previous_district = deepcopy(district_work)
                # Go over to switch when we have a valid solution
                if self.check_valid(previous_district) is True:
                    district_work = self.one_switch_iteration(district_work)
                else:
                    district_work = self.one_change_iteration(district_work)
                # If output is unchanged, add one to count
                if previous_district.return_output() == district_work.return_output():
                    unchanged_count += 1
                else:
                    unchanged_count = 0
        
        return district_work
    
                
    def run_hill_climber(self, district: District, n: int, N: int) -> District:
        """ Run the hill_climber algorithm n times
        Params:
            district (District): district we want to run 
            n   (int):           number of iterations of algorithm
            N   (int):           maximum repeat number
        Returns:
            (District)  district with lowest cost after n iterations
        """
        
        # Start with empty initial district
        district_empty = deepcopy(district)

        # Initialize working district
        district_work = self.one_entire_iteration(district_empty, N)
        file = f"output/csv/costs_hc.csv"
        with open(file, 'w', newline='') as filecsv:
            writer = csv.writer(filecsv)
            writer.writerow([district_work.return_cost()])
        #print(district_work.return_cost())
        for i in range(n - 1):
            print(i)
            previous_district = deepcopy(district_work)
            district_work = self.one_entire_iteration(district_empty, N)
            old_cost = self.return_total_cost(previous_district)
            new_cost = self.return_total_cost(district_work)
            #print(district_work.return_cost())
            with open(file, 'a', newline='') as filecsv:
                writer = csv.writer(filecsv)
                writer.writerow([district_work.return_cost()])
            if new_cost > old_cost:
                district_work = previous_district
        
        district_work.output[0] = {"district": district_work.district,\
                                  f"{district_work.costs_type}":\
                                  district_work.return_cost()}
                                  
        filename = f"output/JSON/best_output_switch_combination.json"
        with open(filename, "w") as f:
            f.write(district_work.return_json_output())
        with open("output.json", "w") as outfile:
            outfile.write(district_work.return_json_output())
        file = f"output/csv/costs_hc.csv"
            
        return district_work
