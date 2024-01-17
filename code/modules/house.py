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
    """ House class

    Methods:
        get_coordinate():       return string of coordinates
        add_cable_segment():    add coordinate to cable connection of house
        return_cable_length():  return lenght of cable associated with house
    """
    
    def __init__(self, house_id: int, coordinate: tuple[int], max_output: float) -> None:
        """ Initialize House object
        Params:
            house_id        (int):          assigned number of house
            coordinate      (tuple[int]):   coordinates of the house
            max_output      (float):        output of the house
        """
        self.house_id = house_id
        self.row = coordinate[0]
        self.column = coordinate[1]
        self.output = max_output
        self.cables = []
        self.str_cables = []
        # Initialize house dictionary
        self.house_dict = {"location": self.get_coordinate((self.row, self.column)),
                           "output": float(self.output), "cables": self.str_cables}

    def get_coordinate(self, coordinate: tuple[int]) -> str:
        """ Return string form of given coordinate
        Params:
            coordinate    (tuple[int]): given coordinate
        Returns:
            (str) coordinate in form "x,y"
        """
            
        return str(coordinate[0]) + "," + str(coordinate[1])

    def add_cable_segment(self, coordinate: tuple[int]) -> None:
        """ Add a cable coordinate to the house
        Creates cable point for house
        Params:
            coordinate    (tuple[int]): given coordinate
        Returns:
            none
            adds coordinate to cables list of house
        """

        self.str_cables.append(self.get_coordinate((coordinate[0], coordinate[1])))
        self.cables.append(coordinate)

    def return_cable_length(self) -> int:
        """ Return length of cable associated with house
        Returns:
            (int) length of cable
        """
            
        return len(self.cables) - 1