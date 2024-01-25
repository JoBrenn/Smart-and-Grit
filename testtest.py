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
simul = Simmulatedannealing(district, 20000)
district = simul.run_hill_climber(district, 10, 1000)
#district = run_hill_climber_2(district, 500, 1000)
#print(district.return_cost())
#print(check_valid(district))
plot_output(district.return_output(), "simulatedannealing", 1, "simulatedannealing")

# Convert json to list again
#filename = f"output/JSON/test-output.json"
#with open(filename, "r") as f:
#    test_output = copy.deepcopy(json.load(f))
#test_output = copy.deepcopy(test_output)
#filename2 = f"output/JSON/output_samenvoegvoorbeeld_presentatie - Copy.json"
#filename = f"output/JSON/district_1/hillclimber/output_hill_climber_500_1.json"
#with open(filename, "r") as f2:
#    output = run(json.load(f2), 10000)

#plot_output(output, "Hill Climber district 1", 1, "Hill Climber district 1")