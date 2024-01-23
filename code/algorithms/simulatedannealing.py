from .hillclimber import HillClimber
from code.modules.district import District

class Simmulatedannealing(HillClimber):
    
    def __init__(self, district: District, temp: float):
        # Use init of the Hillclimber class
        super().__init__(district)
        
        # Starting temperature
        self.temp_0 = temp
        # Current temperature
        self.temp = temp
        
    def linear_temperature_change(self) -> None:
        self.temp = self.temp - (self.temp_0 / self.iterations)
        
    def check_solution(self, district: District) -> None: