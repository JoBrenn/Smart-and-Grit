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

    def __init__(self, x: int, y: int, capacity: float, price: int) -> None:
        self.row = x
        self.column = y
        self.capacity = capacity
        self.left_over_capacity: float = capacity
        self.price = price
        # List of houses connected to battery
        self.houses = []
        # Initialize battery dictionary
        self.battery_dict = {"location": self.get_coordinate(self.row, self.column), 
                             "capacity": float(self.capacity), "houses": self.houses}

    def get_coordinate(self, x: int, y: int) -> str:
        """ Return string configuration of coordinates.
            pre: x and y integer coordinates
            post: returns string of coordinates seperated by comma"""
            
        return str(x) + "," + str(y)

    def add_house(self, house: House) -> None:
        """" Adds a house to the collection of houses connected to the battery.
             pre: house Object
             post: return None"""
             
        self.houses.append(house.house_dict)
        # Reduce the leftover capacity of the battery
        self.left_over_capacity -= house.output
