""" Closest assignment algoritm

File: closest.py

Author:    Jesper Vreugde

Date: 26/01/24

Description:
This algorithm assigns each house to the closest battery
that is measured Manhattan distance. This algorithm will can be
run again until a solution has been found where the maximum capacity
of each battery has not been exceeded

Usage:  from code.algorithms.closest import Closest
"""

from code.modules.district import District
from code.algorithms.manhattan_distance import return_manhattan_distance, \
                                               create_cable

from copy import deepcopy
from random import shuffle


class Closest:
    """ Closest algorithm classes

    Methods:
        run():            runs the closest assignment algorithm
        return_valid()    determines whether solution is valid
    """

    def __init__(self, old_district: District, max_runs: int = 10):
        """ Initialize Closest class
        Params:
            district    (District): Distrisct object
            max_runs    (int): The maximum recursion runs in case a valid
                               solution has not been found
        """

        self.old_district = old_district
        self.max_runs = max_runs

        self.district = None

    def run(self) -> District:
        """ Runs the closest assignnment algorithm
            Returns:
                District object of final solution
        """

        self.district = deepcopy(self.old_district)
        shuffle(self.district.houses)

        # Runs while loop until all houses have been assigned
        # or max_runs have been reached
        while len(self.district.houses) > 0:
            house = self.district.houses.pop()
            closest_dist = float('inf')
            closest_bat = None

            # Loops over each battery to find the closest distance
            for battery in self.district.batteries:

                # Battery should have capacity left
                if battery.left_over_capacity > house.output:
                    dist = return_manhattan_distance(house,
                                                     tuple([battery.row,
                                                            battery.column]))

                    if dist < closest_dist:
                        closest_dist = dist
                        closest_bat = battery

            # Assigns house if compatible battery has been found
            if closest_bat is not None:
                closest_bat.add_house(house)
                create_cable(house, [closest_bat.row, closest_bat.column])

            # Recursively reruns algorithm until valid solution has been found
            # or the max amount of runs has been reached
            elif self.max_runs == 0:
                print("Max runs reached. Solution is not valid")

            else:
                self.max_runs -= 1
                print(f"HOUSE ON ({house.row}, {house.column}) NOT ASSIGNED."
                      + f" Retries left: {self.max_runs}")
                self.district = self.run()
                
        if self.district != None:
            self.district.district_dict["costs-own"] = self.district.return_cost()

        return self.district

    def return_valid(self) -> bool:
        """ A function to determine whether the solution is valid
            Returns:
                a bool that shows whether the solution is valid or not
                prints the amount of unassigned houses
        """

        # Returns false if house has not been assigned
        if len(self.district.houses) != 0 or self.district is None:
            invalid_batteries = 0
            for battery in self.district.batteries:
                if battery.left_over_capacity < 0:
                    invalid_batteries += 1
            print(f"{len(self.district.houses)} not assigned. " +
                  f"{invalid_batteries} batteries have \
                  exceeded their capacity")

            return False

        return True
