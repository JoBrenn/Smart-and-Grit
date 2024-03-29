""" Module of House class

File: house.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 09/01/24 (31/01/24)

Description:
This House class can be used to initialize a house object.

Usage:  from code.modules.house import House
"""


class House:
    """ House class

    Methods:
        convert_coordinate_to_str():   return coordinates in string form "x,y"
        add_cable_segment():           add coordinate to cable connection of house
        return_cable_length():         return length of house cable
        delete_cables():               delete house cable
    """

    def __init__(self, house_id: int, coordinate: tuple[int, int],
                 max_output: float) -> None:
        """ Initialize House object
        Params:
            house_id        (int):          assigned number of house
            coordinate      (tuple[int]):   coordinate of the house
            max_output      (float):        output of the house
        """

        self.house_id = house_id
        self.row = coordinate[0]
        self.column = coordinate[1]
        self.output = max_output
        self.cables: list[tuple[int, int]] = []
        self.str_cables: list[str] = []

        # Initialize house dictionary
        self.house_dict = {"location": self.convert_coordinate_to_str((self.row,
                                                            self.column)),
                           "output": float(self.output),
                           "cables": self.str_cables}

    def convert_coordinate_to_str(self, coordinate: tuple[int, int]) -> str:
        """ Return string form of given coordinate
        Params:
            coordinate    (tuple[int]): given coordinate
        Returns:
            (str) coordinate in form "x,y"
        """

        return str(coordinate[0]) + "," + str(coordinate[1])

    def add_cable_segment(self, coordinate: tuple[int, int]) -> None:
        """ Add a cable coordinate to the house
            Creates cable point for house
        Params:
            coordinate    (tuple[int]): given coordinate
        Returns:
            none
            adds coordinate to cables list of house
        """

        self.str_cables.append(self.convert_coordinate_to_str((coordinate[0],
                                                    coordinate[1])))
        self.cables.append(coordinate)

    def return_cable_length(self) -> int:
        """ Return length of house cable
        Returns:
            (int) length of cable
        """

        return len(self.cables) - 1

    def delete_cables(self) -> None:
        """ Delete all house cables
        Returns:
            none
            alters cables and str_cables list and dictionary
        """

        # Delete old cables in House class
        self.cables.clear()
        self.str_cables.clear()

        # Clear cables in house dictionary
        self.house_dict["cables"].clear()
