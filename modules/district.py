from house import House
from battery import Battery
import json

class District:

    def __init__(self, district: int, costs_type: str) -> None:
        self.district = district
        self.costs_type = costs_type
        self.costs: int = 0
        self.batteries: list[Battery] = []
        self.houses: list[House] = []
        self.district_dict = {"disctrict": self.district, f"{costs_type}": self.costs}
        self.output: list[dict] = [self.district_dict]
        
        # load the houses and batteries
        self.load_houses(f"../data/district_{district}/district-{district}_houses.csv")
        self.load_batteries(f"../data/district_{district}/district-{district}_batteries.csv")
    
    def load_houses(self, filename: str):
        """ loads the houses from csv file and adds them to list"""

        with open(filename) as f:
            next(f)
            for line in f:
                house_data = line.strip().split(",")
                house = House(house_data[0], house_data[1], house_data[2])
                self.houses.append(house)
                # add total house cable costs to total costs
                self.costs += house.cable_costs             

    def load_batteries(self, filename: str):
        """ loads the batteries from csv file and adds them to list"""
                
        with open(filename) as f:
            next(f)
            for line in f:
                battery_data = line.strip().split(",")
                # remove " character that comes with csv
                battery_data[0] = battery_data[0].translate({ord('"'): None})
                battery_data[1] = battery_data[1].translate({ord('"'): None})
                battery = Battery(battery_data[0], battery_data[1], battery_data[2], 5000)
                self.batteries.append(battery)
                # add costs of battery to total costs
                self.costs += battery.price
                # add battery dictionary to the output list
                self.output.append(battery.battery_dict)

    def return_output(self):
        """ returns the output list in wanted format"""
        return json.dumps(self.output)
        
district = District(1, "costs-own")
print(district.return_output())

