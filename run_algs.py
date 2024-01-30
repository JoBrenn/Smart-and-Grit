from code.modules.district import District


#from code.algorithms.closest import Closest
#from code.algorithms.depth_first import DepthFirst
#from code.algorithms.breadth_first import BreadthFirst
#from code.algorithms.beam_search import BeamSearch
from code.algorithms.hill_climber import HillClimber
#from code.algorithms.simulatedannealing import Simulatedannealing

import csv


district = District(1, "costs-own")

#closest = Closest(district, 10)
hillclimb = HillClimber(district)
print("started")
state = hillclimb.run_hill_climber(district, 1, 1000)
print("completed")

succeeded = 0

if state:
    print(state.return_cost())
    succeeded += 1

with open(f"output/csv/test.csv", "a", newline="") as outfile:
    writer = csv.writer(outfile, delimiter=',')
    print(state.return_cost())
    writer.writerow([state.return_cost()])

print(succeeded)

"""
beamsearch = BeamSearch(district, 3)

state = beamsearch.run()
succeeded = 0

if state:
    print(state)
    print(state.return_cost())
    succeeded += 1

print(succeeded)"""
