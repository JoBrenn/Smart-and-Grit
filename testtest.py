from code.algorithms.hill_climber import *
from code.modules.district import District
from code.visualisation.visualize import plot_output
from code.algorithms.combine_cables import *
from code.algorithms.simulatedannealing import *

import json
district = District(1, "costs-own")
#print(district.return_cost())
#random_start_state(district)
#print(district.return_cost())
#print(random_change(district).return_cost())
#one_change_iteration(district)
simul = Simmulatedannealing(district, 1000)
district = simul.run_hill_climber(district, 10, 1000)
#district = run_hill_climber_2(district, 500, 1000)
#print(district.return_cost())
#print(check_valid(district))
plot_output(district.return_output(), "hill_climber_2", 1, "Hill Climber with switch")

# Convert json to list again
#filename = f"output/JSON/test-output.json"
#with open(filename, "r") as f:
#    test_output = copy.deepcopy(json.load(f))
#test_output = copy.deepcopy(test_output)
#filename2 = f"output/JSON/output_500_times_switch_combination_cable_combine.json"
#new_output = run(test_output, 10)
#with open(filename2, "w") as f2:
#    f2.write(json.dumps(new_output))

#plot_output(new_output, "Test-combined", 1, "Test-combined")