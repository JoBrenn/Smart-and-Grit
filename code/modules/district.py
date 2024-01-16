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
        self.batteries: list[Battery] = []
        self.houses: list[House] = []
        self.district_dict = {"district": self.district, f"{costs_type}": 0}
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
            for n, line in enumerate(f):
                house_data = line.strip().split(",")
                house = House(n, int(house_data[0]), int(house_data[1]), float(house_data[2]))
                self.houses.append(house)

    def load_batteries(self, filename: str) -> None:
        """ Load the batteries from csv file
        Creates battery objects and adds them to list.
        Params:
            filename    (str): Takes form of data/district_<district-number>/district-<district-number>_batteries.csv
        Returns:
            none
            list of battery objects is initialized
        """

        with open(filename) as f:
            next(f)
            for i, line in enumerate(f):
                battery_data = line.strip().split(",")
                # Remove " character that comes with csv
                battery_data[0] = battery_data[0].translate({ord('"'): None})
                battery_data[1] = battery_data[1].translate({ord('"'): None})
                battery = Battery(i, int(battery_data[0]), int(battery_data[1]), float(battery_data[2]), 5000)
                self.batteries.append(battery)
                # Add battery dictionary to the output list
                self.output.append(battery.battery_dict)
    
    def return_cost(self) -> int:
        """ Return the distric costs, given list of houses
            pre: list of house objects, needed since
                 cables are added after"""
        
        cost = 0
        for house in self.houses:
            cost += house.return_cable_length() * 9
        for battery in self.batteries:
            cost += battery.price
        return cost
    
    def return_output(self) -> list:
        """ Return the desired output in list form."""  
        
        return self.output

    def return_json_output(self) -> str:
        """ Convert and return output to json string."""

        return json.dumps(self.output)

    def is_valid(self) -> bool:
        """ Checks wether we have found a valid solution"""
        
        number_houses = 0
        for battery in self.return_output()[1:]:
            for house in battery["houses"]:
                # When House connection is empty returns false
                number_houses += 1
                if len(house["cables"]) == 0:
                    return False
        if number_houses != 150:
            return False
            
        return True
