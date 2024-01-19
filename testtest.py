from code.algorithms.hill_climber import *
from code.modules.district import District
from code.visualisation.visualize import plot_output

district = District(1, "costs-own")
#print(district.return_cost())
#random_start_state(district)
#print(district.return_cost())
#print(random_change(district).return_cost())
#one_change_iteration(district)
#district = run_hill_climber(district, 500, 1000)
district = run_hill_climber_2(district, 100, 1000)
print(district.return_cost())
print(check_valid(district))
plot_output(district.return_output(), "hill_climber_2", 1, "Hill Climber with switch")

