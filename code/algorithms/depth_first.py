import copy

from code.modules.district import District
from code.modules.district import Battery
from code.modules.district import House
from code.algorithms.manhattan_distance import *
from code.visualisation.visualize import plot_output
from random import shuffle

class DepthFirst:
    def __init__(self, district, depth = 5):#: int = len(district.houses)) -> None:
        """ Initialize Depth First class
        Params:
            district    (District): Distrisct object
            depth       (int): Tha maximum depth that the Depth search tree
                               will be. Set at the max as default"""

        self.depth = depth
        self.stack = [district]
        self.house_num = len(district.houses)
        # Randomize
        shuffle(self.stack[0].houses)

    def run(self):
        """
            Returns """
        # Set the initial costs to be the 
        lowest_costs = float("inf")
        lowest_state = None

        # Loop over stack until it is empty
        while len(self.stack) > 0:
            state = self.return_next_state()
            #print(state.houses)

            #print(self.valid_capacity(state))
            if self.valid_capacity(state) == True:
                #print(len(state.houses))
                #print(self.depth)
                if self.house_num - len(state.houses) < self.depth:
                    print(self.house_num - len(state.houses))
                    #print(self.depth)
                    house = state.houses.pop()
                    

                    for n, battery in enumerate(state.batteries):
                        child = copy.deepcopy(state)
                        house_add = copy.deepcopy(house)

                        create_cable(house_add, (battery.row, battery.column))
                        child.batteries[n].add_house(house_add)
                        #house_2 = copy.deepcopy()
                        #child.batteries[n].append(house_2)
                        self.stack.append(child)

                else:
                    #print(f"{state.return_json_output()}")
                    # Check solution
                    state.district_dict[f"{state.costs_type}"] = state.return_cost()
                    #print(state.return_cost())

                    if state.district_dict[district.costs_type] < lowest_costs:
                        lowest_costs = state.district_dict[district.costs_type]
                        lowest_costs_state = copy.deepcopy(state)

        return lowest_costs_state


    def return_next_state(self):
        """ Returns next state in the stack
            Returns:
        """
        return self.stack.pop()

    def valid_capacity(self, district) -> bool: 
        """ TODO
            Returns:

        """
        for battery in district.batteries:
            if battery.left_over_capacity < 0:
                return False
        return True


def test_depth_district(district):
    depth = 5#len(district.houses)
    stack = [district]

    #state_set = set()
    lowest_costs = float('inf')
    lowest_costs_state = None

    houses = copy.deepcopy(district.houses)
    total = 0

    while len(stack) > 0:
        state = stack.pop()
        curr_depth = len(district.houses) - len(houses)

        # TODO Prunen

        #print("len: {:2} statelen: {:2} depth: {:2} stacklen: {:2}"\
         #   .format(len(houses),state.assigned_houses,curr_depth,len(stack)))
        """if state.assigned_houses == 1:
            print("train")

        if state.assigned_houses == 7:
            print("train2")"""



        if state.assigned_houses < depth and valid_cap(state):

            house = houses[state.assigned_houses]
            #print(house)
            for n, battery in enumerate(state.batteries):

                child = copy.deepcopy(state)
                house_add = copy.deepcopy(house)
                #house cables = []
                create_cable(house_add, (battery.row, battery.column))
                child.batteries[n].add_house(house_add)

                child.assigned_houses += 1
                # house_2 = copy.deepcopy()
                #child.batteries[n].append(house_2)
                stack.append(child)

        else:
            #print(f"{state.return_json_output()}")
            total += 1
            # check solution

            state.district_dict[f"{state.costs_type}"] = state.return_cost()
            #print(state.return_cost())

            if state.district_dict[district.costs_type] < lowest_costs:
                lowest_costs = state.district_dict[district.costs_type]
                lowest_costs_state = copy.deepcopy(state)
            #plot_output(state.return_output())

    #print(f"Lowest: {lowest_costs}")
    #print(total)
    #plot_output(lowest_costs_state.return_output())



district = District(1, "costs-own")

def valid_cap(state):
    for battery in state.batteries:
        if battery.left_over_capacity < 0:
            #print("Not valid")
            return False

        #print("Valid")
        return True


# Example code from Lecture Constructive algorithm by Bas Terwijn
def test_depth():
    depth = 11
    stack = [""]
    while len(stack) > 0:
        state = stack.pop()
        #print(state)
        #print("stack")
        if len(state) < depth:
            for i in ["1","2","3","4","5"]:
                child = copy.deepcopy(state)
                child += i
                # print(child)
                stack.append(child)
       # else:
            # check solution
            #print(state)
