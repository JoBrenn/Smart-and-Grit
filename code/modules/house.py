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
        #self.cable_costs: int = 0

    def get_coordinate(self, x: int, y: int) -> str:
        """ Return string configuration of coordinates.
            pre: x and y integer coordinates
            post: returns string of coordinates seperated by comma"""
        return str(x) + "," + str(y)

    def add_cable_segment(self, coordinate: tuple[int]) -> None:
        """ Add a cable segment and its cost to cable connection of house.
            pre: integer coordinates of the begin and the end of cable segment
            post: return None"""
        
        # TODO
        #
        """ Fout zit denk ik hier. Kabelpunten worden altijd 2x toegevoegd ongeacht of het
        beginpunt het vorige eindpunt is waardoor de output JSON er vreemd uit komt te zien.
        Waarscshijnlijk restant van oude gen_cable.py voor het omschrijven
        """ 
        #
        #

        self.cables.append(self.get_coordinate(coordinate[0], coordinate[1]))
        # Add cable costs
        #self.cable_costs += 9

    def return_cable_length(self) -> int:
        """ Determines the length of the cable associated to the house
            post: integer of the length of cable"""
            
        return len(self.cables)