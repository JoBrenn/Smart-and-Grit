""" Module of House class.

File: house.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 09/01/24 (11/01/24)

Description:    This House class can be used to initialize a District object.

Usage:  from modules.house import House
"""
class House:

    def __init__(self, house_id: int, x: int, y: int, max_output: float) -> None:
        self.house_id = house_id
        self.row = x
        self.column = y
        self.output = max_output
        self.cables = []
        # Initialize house dictionary
        self.house_dict = {"location": self.get_coordinate(self.row, self.column),
                           "output": float(self.output), "cables": self.cables}
        # Costs of the cables associated with a house
        self.cable_costs: int = 0

    def get_coordinate(self, x: int, y: int) -> str:
        """ Return string configuration of coordinates.
            pre: x and y integer coordinates
            post: returns string of coordinates seperated by comma"""
        return str(x) + "," + str(y)

    def add_cable_segment(self, begin: tuple[int], end: tuple[int]) -> None:
        """ Add a cable segment and its cost to cable connection of house.
            pre: integer coordinates of the begin and the end of cable segment
            post: return None"""

        self.cables.append(self.get_coordinate(begin[0], begin[1]))
        self.cables.append(self.get_coordinate(end[0], end[1]))
        # Add cable costs
        self.cable_costs += 9
