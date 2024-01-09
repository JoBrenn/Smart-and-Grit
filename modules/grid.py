import os

from house import House
from battery import Battery


class Grid:

<<<<<<< HEAD
    def __init__(self) -> None:
        self.district: int = os.getcwd().split("/")[-1].split("_")[-1]
        self.costs_shared: int = costs-shared
        self.batteries: list[Battery] = []
        self.houses: list[House] = []

    def battery_to_house(self) -> int:
        pass
