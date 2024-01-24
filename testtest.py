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
#hill = HillClimber(district)
#dishil = hill.run_hill_climber(district, 1, 1000)
#simul = Simmulatedannealing(district, 10000)
#district = simul.run_hill_climber(district, 10, 1000)
#district = run_hill_climber_2(district, 500, 1000)
#print(district.return_cost())
#print(check_valid(district))
#plot_output(district.return_output(), "hill_climber_2", 1, "Hill Climber with switch")

# Convert json to list again
#filename = f"output/JSON/test-output.json"
#with open(filename, "r") as f:
#    test_output = copy.deepcopy(json.load(f))
#test_output = copy.deepcopy(test_output)
filename2 = f"output/JSON/output_500_times_switch_combination_cable_combine.json"
with open(filename2, "r") as f2:
    output = json.load(f2)

plot_output(output, "Test-combined", 1, "Test-combined")