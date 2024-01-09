from house import House
from battery import Battery

class District:

    def __init__(self, district: int) -> None:
        self.district = district
        self.house = []
        self.costs_shared: int
        self.batteries: list[Battery] = []
        self.houses: list[House] = []
        
        self.load_houses(f"../data/district_{district}/district-{district}_houses.csv")
        self.load_batteries(f"../data/district_{district}/district-{district}_batteries.csv")
    
    def load_houses(self, filename: str):
        """ loads the houses from csv file and adds them to list"""
        number_lines = 0
        with open(filename) as f:
            for line in f:
                number_lines += 1
                
        with open(filename) as f:
            # skip first line
            line = f.readline()
            for i in range(0, number_lines - 1):
                line = f.readline()
                house_data = line.strip().split(",")
                house = House(house_data[0], house_data[1], house_data[2])
                self.houses.append(house)

    def load_batteries(self, filename: str):
        """ loads the batteries from csv file and adds them to list"""
        number_lines = 0
        with open(filename) as f:
            for line in f:
                number_lines += 1
                
        with open(filename) as f:
            # skip first line
            line = f.readline()
            for i in range(1, number_lines):
                line = f.readline()
                battery_data = line.strip().split(",")
                # remove " character that comes with csv
                battery_data[0] = battery_data[0].translate({ord('"'): None})
                battery_data[1] = battery_data[1].translate({ord('"'): None})
                battery = Battery(battery_data[0], battery_data[1], battery_data[2], 5000)
                self.batteries.append(battery)

