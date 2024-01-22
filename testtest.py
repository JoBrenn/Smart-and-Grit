from code.algorithms.hill_climber import *
from code.modules.district import District
from code.visualisation.visualize import plot_output
from code.algorithms.Samenvoeg import *

import json
#district = District(1, "costs-own")
#print(district.return_cost())
#random_start_state(district)
#print(district.return_cost())
#print(random_change(district).return_cost())
#one_change_iteration(district)
#district = run_hill_climber(district, 500, 1000)
#district = run_hill_climber_2(district, 500, 1000)
#print(district.return_cost())
#print(check_valid(district))
#plot_output(district.return_output(), "hill_climber_2", 1, "Hill Climber with switch")

# Convert json to list again
filename = f"output/JSON/test-output.json"
with open(filename, "r") as f:
        test_output = json.load(f)
#print(test_output)
new_output = combine_district(test_output)
plot_output(new_output, "samenvoeg-test", 1, "samenvoeg-test")