from house import House

class Battery:
    
    def __init__(self, x: int, y: int, capacity: float, price: int) -> None:
        self.row = x
        self.column = y
        self.capacity = capacity
        self.price = price
        # list of houses connected to battery
        self.houses = []
        # initialize battery dictionary
        self.battery_dict = {"location": self.get_coordinate(self.row, self.column), "capacity": self.capacity, "houses": self.houses}
    
    def get_coordinate(self, x: int, y: int) -> str:
            """ returns string of coordinates"""
            return str(x) + "," + str(y)   
            
    def add_house(self, house: House):
        """" adds a house to the collection of houses connected to the battery"""
        self.houses.append(house.house_dict)
        
