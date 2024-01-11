from modules.house import House

class Battery:

    def __init__(self, x: int, y: int, capacity: float, price: int) -> None:
        self.row = x
        self.column = y
        self.capacity = capacity
        self.left_over_capacity = capacity
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
        self.left_over_capacity -= house.max_output
