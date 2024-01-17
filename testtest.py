from code.algorithms.hill_climber import *
from code.modules.district import District
district = District(1, "cost-own")
#random_start_state(district)
#print(district.return_cost())
#print(random_change(district).return_cost())
one_change_iteration(district)