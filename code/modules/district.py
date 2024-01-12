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
                house = House(int(house_data[0]), int(house_data[1]), float(house_data[2]))
                self.houses.append(house)

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
                battery = Battery(int(battery_data[0]), int(battery_data[1]), float(battery_data[2]), 5000)
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
        """ Return the distric costs, given list of houses
            pre: list of house objects, needed since
                 cables are added after"""
        for house in self.houses:
            # Add total house cable costs to total costs
            self.costs += house.cable_costs
        return self.costs
    
    def get_cable_points(self, house: tuple[int], battery: tuple[int]) -> tuple[int]:
        """ Generates the points between which a cable must be layed from house
            to battery, following the shortest Manhatten distance 
            From house first up or down then left or right"""
           
        points = [house, (house[0], battery[1]), battery]
        return tuple(points)
    
    def create_cable(self, house: House, battery: Battery) -> None:
        """ Creates entire cable connection between house and battery
            following shortest manhatten distance. 
            Again following from house first up or donw then left or right"""
        
        cable_points = self.get_cable_points((house.row, house.column), (battery.row, battery.column))
        
        # House y minus in between y
        y_distance = cable_points[0][1] - cable_points[1][1]
        # In between x minus battery x
        x_distance = cable_points[1][0] - cable_points[2][0]
        
        # Start at the house
        x_current = house.row
        y_current = house.column
        
        # Check whether we need to go up or down
        if y_distance > 0:
            # Down
            for step in range(y_distance):
                house.add_cable_segment((x_current, y_current), (x_current, y_current - 1))
                y_current -= 1
        elif y_distance < 0:
            # Up
            for step in range(abs(y_distance)):
                house.add_cable_segment((x_current, y_current + 1), (x_current, y_current))
                y_current += 1
       
       # Check whether we need to go left or right
        if x_distance > 0:
            # Left
            for step in range(x_distance):
                house.add_cable_segment((x_current, y_current), (x_current - 1, y_current))
                x_current -= 1
        elif x_distance < 0:
            # Right
            for step in range(abs(x_distance)):
                house.add_cable_segment((x_current, y_current), (x_current + 1, y_current))
                x_current += 1