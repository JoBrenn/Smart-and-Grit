class House:
    
    def __init__(self, x: int, y: int, max_output: float) -> None:
        self.row = x
        self.column = y
        self.output = max_output
        # initialize house dictionary
        self.house_dict = {"location": self.get_coordinate(self.row, self.column), "output": self.output, "cables": []}
        
    def get_coordinate(self, x: int, y: int) -> str:
        """ returns string of coordinates"""
        return str(x) + "," + str(y) 
        
    def add_cable(self, x_begin: int, y_begin: int, x_end: int, y_end: int):
        """ adds a cable segment to cable connection of house"""
        self.house_dict["cables"].append(self.get_coordinate(x_begin, y_begin))
        self.house_dict["cables"].append(self.get_coordinate(x_end, y_end))
        