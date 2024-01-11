""" Module of District class.

File: district.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 09/01/24 (11/01/24)

Description:    This District class can be used to initialize a District object.

Usage:  from modules.district import District
"""
from code.modules.battery import Battery
from code.modules.house import House
from code.algorithms.random import *

import json

class District:
    """ District class.

    Methods:
        load_houses():          Loads houses from data/
        load_batteries():       Loads batteries from data/
        return_output():        Returns data in object in list format
        return_json_output():   Returns data in object in string format
    """

    def __init__(self, district: int, costs_type: str) -> None:
        """ Initialize District object.

        Params:
            district    (int): Number of district (between 1 and 3)
            costs_type  (str): Type of costs (either "costs-own" or "costs-shared")
        """
        self.district = district
        self.costs_type = costs_type
        self.costs: int = 0
        self.batteries: list[Battery] = []
        self.houses: list[House] = []
        self.district_dict = {"district": self.district, f"{costs_type}": self.costs}
        self.output: list[dict] = [self.district_dict]

        # Load the houses and batteries
        self.load_houses(f"data/district_{district}/district-{district}_houses.csv")
        self.load_batteries(f"data/district_{district}/district-{district}_batteries.csv")

    def load_houses(self, filename: str) -> None:
        """ Load the houses from csv file.

        Creates house objects and adds them to list.

        Params:
            filename    (str): Takes form of data/district_<district-number>/district-<district-number>_houses.csv

        Returns:
            none
            list of house objects is initialized
        """

        with open(filename) as f:
            next(f)
            for line in f:
                house_data = line.strip().split(",")
                house = House(house_data[0], house_data[1], house_data[2])
                self.houses.append(house)
                # Add total house cable costs to total costs
                self.costs += house.cable_costs

    def load_batteries(self, filename: str) -> None:
        """ Load the batteries from csv file.

        Creates battery objects and adds them to list.

        Params:
            filename    (str): Takes form of data/district_<district-number>/district-<district-number>_batteries.csv

        Returns:
            none
            list of battery objects is initialized
        """

        with open(filename) as f:
            next(f)
            for line in f:
                battery_data = line.strip().split(",")
                # Remove " character that comes with csv
                battery_data[0] = battery_data[0].translate({ord('"'): None})
                battery_data[1] = battery_data[1].translate({ord('"'): None})
                battery = Battery(battery_data[0], battery_data[1], battery_data[2], 5000)
                self.batteries.append(battery)
                # Add costs of battery to total costs
                self.costs += battery.price
                # Add battery dictionary to the output list
                self.output.append(battery.battery_dict)

    def return_output(self) -> list:
        """ Return the desired output in list form."""

        return self.output

    def return_json_output(self) -> str:
        """ Convert and return output to json string."""

        return json.dumps(self.output)

    def return_cost(self) -> int:
        """ Return the distric costs"""
        
        return self.costs
    
    def random_algorithm(self):
        """ code for application of random_algorithm"""
        # Dictionary with connections
        connections = random_assignment(self, self.batteries, self.houses)
        for house in connections:
            battery = connections[house]
            points_walked = random_walk(self, int(house.row), int(house.column), int(battery.row), int(battery.column), 50)
            # Add a cable segment between all the points visited in the random walk
            for i in range(len(points_walked)):
                house.add_cable_segment(self, points_walked[i][0], points_walked[i][1],\
                                  points_walked[i + 1][0], points_walked[i + 1][1])

    def random_one_house(self):
        """ code for application of one house random_algorithm"""
        # Dictionary with connections
        house_one = self.houses[0]
        battery = self.batteries[random.randint(0, len(self.batteries) - 1)]
        points_walked = random_walk(self, int(house_one.row), int(house_one.column), int(battery.row), int(battery.column), 50)
        # Add a cable segment between all the points visited in the random walk
        for i in range(len(points_walked)):
            house_one.add_cable_segment(self, points_walked[i][0], points_walked[i][1],\
                                    points_walked[i + 1][0], points_walked[i + 1][1])