import random
import copy
from code.modules.district import District
from code.modules.district import Battery
from code.modules.district import House
from code.algorithms.manhattan_distance import get_cable_points, create_cable

"""Hill Climber with constraint relaxation where penalty is equal to capacity surplus"""

class HillClimber:
    """ HillClimber algorithm class

    Methods:
        random_start_state():       create random start configuration for given district
        random_change():            takes random house and randomly assigns it to different battery
        random_switch():            takes two random houses and switches batteries assignments
        return_penalty():           return battery capacity exceedance penalty
    """
    
    def __init__(self, district: District) -> None:
        self.district_empty = copy.deepcopy(district)
    
    def random_start_state(self, district: District) -> District:     
        """ Randomly assign houses to batteries, not taking capacity into account
        Creates dictionary, where houses are keys and batteries values
        Creates connections via Manhattan distance
        Params:
            district    (District): district object
        Returns:
            (list) output list
        """
        
        # Take the empty district as initial configuration
        for house in district.houses: 
            battery = random.choice(district.batteries)
            # Add the house to the battery connection (such that dictionary is added)
            battery.add_house(house)
            create_cable(house, (battery.row, battery.column))
        district.district_dict[f"{district.costs_type}"] = district.return_cost()

        return district

    def random_change(self, district: District, costs_type: str) -> District:
        """ Randomly change one house-battery connection
        Alters this change in the connection dictionary
        Params:
            batteries          (list): list of batteries in district
            connection_dict    (dict): dictionary where houses are keys and batteries values
        Returns:
            (District) altered district object
        """
        
        # Get random house from district
        random_house = random.choice(district.houses)
        dictionary = copy.deepcopy(random_house.house_dict)

        # Find old battery connection
        for battery in district.batteries:
            if random_house in battery.houses:
                old_battery = battery
        
        # Delete the house from the battery in output dictionary
        index = district.output.index(old_battery.battery_dict)
        one = copy.deepcopy(district.output[index])
        district.output[index]["houses"].remove(dictionary)

        # Delete house from old battery
        old_battery.delete_house(random_house)
        
        random_house.cables.clear()
        random_house.str_cables.clear()
        
        # Clear cables in house dictionary
        random_house.house_dict["cables"].clear()
                      
        # Determine new random battery
        new_battery = random.choice(district.batteries)
        # Create new Manhattan cable
        create_cable(random_house, (new_battery.row, new_battery.column))
        
        # Add new cables to house dictionary
        random_house.house_dict["cables"] = random_house.str_cables
        
        # Add house to new battery
        new_battery.add_house(random_house)

        # Add house to battery in output dictionary
        index_new = district.output.index(new_battery.battery_dict)
        dictionary_new = copy.deepcopy(random_house.house_dict)
        #district.output[index_new]["houses"].append(dictionary_new)
        
        # Reset first element in dictionary, so that the cost is accurate
        district.output[0] = {"district": district.district, f"{costs_type}": self.return_total_cost(district)}

        return district

    def random_switch(self, district: District, costs_type: str) -> District:
        # Get random different houses from district
        houses = district.houses.copy()
        random_house_1 = random.choice(district.houses)
        houses.remove(random_house_1)
        random_house_2 = random.choice(houses)
        dictionary_1 = copy.deepcopy(random_house_1.house_dict)
        dictionary_2 = copy.deepcopy(random_house_2.house_dict)
        
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
        #district.output[index_new_1]["houses"].append(dictionary_new_2)
        index_new_2 = district.output.index(battery_2.battery_dict)
        dictionary_new_1 = random_house_1.house_dict
        #district.output[index_new_2]["houses"].append(dictionary_new_1)
        
        # Reset first element in dictionary, so that the cost is accurate
        district.output[0] = {"district": district.district, f"{costs_type}": self.return_total_cost(district)}

        output = district.return_output()
        
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
            (list) either altered or original district output list
        """
        old_district = copy.deepcopy(district)
        output = copy.deepcopy(district.return_output())
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
            (list) either altered or original district output list
        """
        old_district = copy.deepcopy(district)
        output = copy.deepcopy(district.return_output())
        old_cost = self.return_total_cost(district)
        # Apply a random change
        new_district = self.random_switch(district, "costs-own")
        new_cost = self.return_total_cost(district)
        
        # Make sure you cannot go from good solution to non solution
        if self.check_valid(old_district) is True and self.check_valid(new_district) is False:
            return old_district
            
        # Change state when the cost is lower 
        if new_cost < old_cost:
            return new_district
            
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
        
        # Keep going until the state hasn't improved N times
        while unchanged_count < N - 1:
            previous_district = copy.deepcopy(district_work)
            # Go over to switch when we have a valid solution
            if self.check_valid(previous_district) is True:
                district_work = self.one_switch_iteration(district_work)
            else:
                district_work = self.one_change_iteration(district_work)
            print(self.return_total_cost(previous_district))
            print(self.return_total_cost(district_work))
            #print(return_total_cost(previous_district))
            #print(return_total_cost(district_work))
            # If output is unchanged, add one to count
            if previous_district.return_output() == district_work.return_output():
                unchanged_count += 1
            else:
                unchanged_count = 0
                
            #print(check_valid(district_work))
            
        return district_work
                
    def run_hill_climber(self, district: District, n: int, N: int) -> District:
        """ Run the hill_climber algorithm n times
        Params:
            n   (int): number of iterations of algorithm
        Returns:
            none
            runs the algorithm and changes the state when better 
            cost after each step
        """
        
        # Start with empty initial district
        district_empty = copy.deepcopy(district)

        # Initialize working district
        district_work = self.one_entire_iteration_switch(district_empty, N)
        
        for i in range(n - 1):
            print(i)
            previous_district = copy.deepcopy(district_work)
            district_work = self.one_entire_iteration_switch(district_empty, N)
            old_cost = self.return_total_cost(previous_district)
            new_cost = self.return_total_cost(district_work)
            if new_cost > old_cost:
                district_work = previous_district
            # Probeersel met goeie solution
            if self.check_valid(district_work) is False:
                district_work = previous_district
        
        district_work.output[0] = {"district": district_work.district, f"{district_work.costs_type}": district_work.return_cost()}
        filename = f"output/JSON/best_output_switch_combination.json"
        with open(filename, "w") as f:
            f.write(district_work.return_json_output())
        with open("output.json", "w") as outfile:
            outfile.write(district_work.return_json_output())
            
        return district_work
