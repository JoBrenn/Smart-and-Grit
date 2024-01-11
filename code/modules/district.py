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

import json

class District:

    def __init__(self, district: int, costs_type: str) -> None:
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
        """ Load the houses from csv file. Creates house objects
            and adds them to list.
            pre: filename"""

        with open(filename) as f:
            next(f)
            for line in f:
                house_data = line.strip().split(",")
                house = House(house_data[0], house_data[1], house_data[2])
                self.houses.append(house)
                # Add total house cable costs to total costs
                self.costs += house.cable_costs

    def load_batteries(self, filename: str) -> None:
        """ Load the houses from csv file. Creates house objects
            and adds them to list.
            pre: filename"""

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
<<<<<<< HEAD
=======

>>>>>>> 2dd0b541e0be6a3d7539cb5f8e63ed3926a4046b
