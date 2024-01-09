class Battery:
    
    def __init__(self, x: int, y: int, capacity: float, price: int) -> None:
        self.row = x
        self.column = y
        self.capacity = capacity
        self.price = price