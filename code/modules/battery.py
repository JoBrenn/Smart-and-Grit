""" Module of Battery class

File: battery.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 09/01/24 (11/01/24)

Description:
This Battery class can be used to initialize a Battery object.

Usage:  from code.modules.battery import Battery
"""

from code.modules.house import House


class Battery:
    """ Battery class

    Methods:
        get_coordinate():       return coordinates in string form "x,y"
        add_house():            add house to battery connection
        delete_house():         delete house from battery connection
        return_capacity():      return battery capacity
        add_house_cables():     add cables of house to battery cable network
    """

    def __init__(self, battery_id: int, coordinate: tuple[int],
                 capacity: float, price: int) -> None:
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
        self.battery_dict = {"location": self.get_coordinate((self.row,
                                                              self.column)),
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
        """ Add house to battery connection
        Params:
            house    (House): house class object
        Returns:
            none
            adds house object to houses list and battery dictionary
            reduce house output from battery capacity
        """

        self.houses.append(house)
        self.battery_dict["houses"].append(house.house_dict)

        # Reduce the leftover capacity of the battery
        self.left_over_capacity -= house.output

    def delete_house(self, house: House) -> None:
        """ Delete house from battery connection
        Params:
            house    (House): house class object
        Returns:
            none
            removes house object from houses list
            add house output to battery capacity
        """

        self.houses.remove(house)
        self.left_over_capacity += house.output

    def return_capacity(self) -> float:
        """ Return the leftover capacity of the battery
        Returns:
            (float) leftover capacity of battery
        """

        return self.left_over_capacity

    def add_house_cables(self, house) -> None:
        """ Add cables of house to battery cable network
        Params:
            house    (House): house class object
        Returns:
            none
            adds cables associated with house to battery
            cables list
        """

        for cable in house.cables:
            self.cables.add(cable)
