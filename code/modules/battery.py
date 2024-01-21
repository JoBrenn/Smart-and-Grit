""" Module of Battery class

File: battery.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 09/01/24 (11/01/24)

Description:    This Battery class can be used to initialize a Battery object.

Usage:  from models.battery import Battery
"""
from code.modules.house import House


class Battery:
    """ Battery class

    Methods:
        get_coordinate():       return string of coordinates
        add_house():            add house to list of connected houses to battery
    """

    def __init__(self, battery_id: int, coordinate: tuple[int], capacity: float, price: int) -> None:
        """ Initialize Battery object
        Params:
            battery_id    (int):        assigned number of battery
            coordinate    (tuple[int]): coordinates of the battery
            capacity      (float):      capacity of the battery
            price         (int):        price of the battery
        """
        self.battery_id = battery_id
        self.row = coordinate[0]
        self.column = coordinate[1]
        self.capacity = capacity
        self.left_over_capacity: float = capacity
        self.price = price
        # List of houses connected to battery
        self.houses = []
        self.cables = set()
        # Initialize battery dictionary
        self.battery_dict = {"location": self.get_coordinate((self.row, self.column)),
                             "capacity": float(self.capacity), "houses": []}

    def get_coordinate(self, coordinate: tuple[int]) -> str:
        """ Return string form of given coordinate
        Params:
            coordinate    (tuple[int]): given coordinate
        Returns:
            (str) coordinate in form "x,y"
        """

        return str(coordinate[0]) + "," + str(coordinate[1])

    def add_house(self, house: House) -> None:
        """ Add house to list of houses connected to battery
        Params:
            house    (House): house class object
        Returns:
            none
            adds house object to houses list
        """

        self.houses.append(house)
        self.battery_dict["houses"].append(house.house_dict)
        # Reduce the leftover capacity of the battery
        self.left_over_capacity -= house.output
        
    def delete_house(self, house: House) -> None:
        self.houses.remove(house)
        self.left_over_capacity += house.output

    def return_capacity(self) -> float:
        """ Return the leftover capacity of the battery
        Returns:
            (float) leftover capacity of battery
        """

        return self.left_over_capacity

    def add_house_cables(self, house) -> None:
        """ Adds the cable points of a House instance to the Battery instance

        """
        for cable in house.cables:
            self.cables.add(cable)
