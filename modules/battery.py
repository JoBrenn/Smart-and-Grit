""" Model of Battery class

File: battery.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 09/01/24 (11/01/24)

Description:    This Battery class can be used to initialize a Battery object.

Usage:  from models.battery import Battery
"""
from modules.house import House


class Battery:

    def __init__(self, x: int, y: int, capacity: float, price: int) -> None:
        self.row = x
        self.column = y
        self.capacity: float  = capacity
        self.left_over_capacity: float = capacity
        self.price = price
        # list of houses connected to battery
        self.houses = []
        # initialize battery dictionary
        self.battery_dict = {"location": self.get_coordinate(self.row, self.column), "capacity": float(self.capacity), "houses": self.houses}

    def get_coordinate(self, x: int, y: int) -> str:
        """ returns string of coordinates"""
        return str(x) + "," + str(y)

    def add_house(self, house: House) -> None:
        """" adds a house to the collection of houses connected to the battery"""
        self.houses.append(house.house_dict)
        self.left_over_capacity -= house.max_output
