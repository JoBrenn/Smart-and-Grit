""" Module of District class

File: district.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 09/01/24 (11/01/24)

Description:
This District class can be used to initialize a District object.

Usage:  from modules.district import District
"""

from code.modules.battery import Battery
from code.modules.house import House

from typing import Any
import json


class District:
    """ District class

    Methods:
        load_houses():          loads houses from data/
        load_batteries():       loads batteries from data/
        return_cost():          return total cost of district
        return_output():        return data in list format
        return_json_output():   return data in string format
        is_valid():             check whether district configuration is valid
    """

    def __init__(self, district: int, costs_type: str) -> None:
        """ Initialize District object
        Params:
            district    (int): number of district (between 1 and 3)
            costs_type  (str): type of costs ("costs-own" or "costs-shared")
        """

        self.district = district
        self.costs_type = costs_type
        self.batteries: list[Battery] = []
        self.houses: list[House] = []
        self.district_dict = {"district": self.district, f"{costs_type}": 0}
        self.output: list[dict[str, Any]] = [self.district_dict]

        # Load the houses and batteries
        f_house = f"data/district_{district}/district-{district}_houses.csv"
        f_bat = f"data/district_{district}/district-{district}_batteries.csv"
        self.load_houses(f_house)
        self.load_batteries(f_bat)

    def load_houses(self, filename: str) -> None:
        """ Load the houses from csv file.
        Creates house objects and adds them to list.
        Params:
            filename    (str): filename string
        Returns:
            none
            list of house objects is initialized
        """

        # Load in house information
        with open(filename) as f:
            next(f)
            for n, line in enumerate(f):
                house_data = line.strip().split(",")

                # Create House objects
                house = House(n, (int(house_data[0]), int(house_data[1])),
                              float(house_data[2]))
                self.houses.append(house)

    def load_batteries(self, filename: str) -> None:
        """ Load the batteries from csv file
        Creates battery objects and adds them to list.
        Params:
            filename    (str): filename string
        Returns:
            none
            list of battery objects is initialized
        """

        # Load in battery information
        with open(filename) as f:
            next(f)
            for i, line in enumerate(f):
                battery_data = line.strip().split(",")

                # Remove " character that comes with csv
                battery_data[0] = battery_data[0].translate({ord('"'): None})
                battery_data[1] = battery_data[1].translate({ord('"'): None})
                battery = Battery(i, (int(battery_data[0]),
                                  int(battery_data[1])),
                                  float(battery_data[2]), 5000)
                self.batteries.append(battery)

                # Add battery dictionary to the output list
                self.output.append(battery.battery_dict)

    def return_cost(self) -> int:
        """ Determine total cost of the district
        Uses length of house cables and battery costs
        Returns:
            (int) total cost of district
        """

        cost = 0

        for battery in self.batteries:
            for house in battery.houses:
                if house.return_cable_length() != -1:
                    cost += house.return_cable_length() * 9
            cost += battery.price

        return cost

    def return_output(self) -> list[dict[str, Any]]:
        """ Return output in list format
        Returns:
            (list) output
        """

        return self.output

    def return_json_output(self) -> str:
        """ Return output in json format
        Returns:
            (str) json of output
        """

        return json.dumps(self.output)

    def is_valid(self) -> bool:
        """ Check whether solution is valid
        Checks if all houses have cable connections and
        if all 150 houses are connected.
        Returns:
            (bool) true when solution is valid
        """

        number_houses = 0

        for battery in self.return_output()[1:]:
            for house in battery["houses"]:
                # When House connection is empty returns false
                number_houses += 1
                if len(house["cables"]) == 0:
                    return False

        return True
