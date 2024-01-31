""" Script to run different algorithms

File: run_algs.py

Authors:    Jesper Vreugde

Date: 26/01/24 (31/01/24)

Description:
This is a script to run different algorithms and load them in csv file

Usage:  called by time_script.py, no independent usage
"""

from code.modules.district import District

from code.algorithms.closest import Closest
from code.algorithms.depth_first import DepthFirst
from code.algorithms.beam_search import BeamSearch
from code.algorithms.hill_climber import HillClimber
from code.algorithms.simulatedannealing import Simulatedannealing

from code.visualisation.visualize import plot_output

import csv
import sys


def append_to_csv(state: District, algorithm: str) -> None:
    """ Appends the state costs to a csv
        Pararms:
            state(District)     The district whose costs will be appended
            algorithm(str)      The name of the algorithm
        Returns
            None
            Appends the costs to a csv with the same name as the algorithm
    """
    with open(f"output/csv/{algorithm}.csv", "a", newline="") as outfile:
        writer = csv.writer(outfile, delimiter=';')
        writer.writerow([state.return_cost()])

district = District(1, "costs-own")

algorithm = sys.argv[1]

if algorithm == "closest":
    closest = Closest(district, 10)
    result = closest.run()
    append_to_csv(result, algorithm)

elif algorithm == "beamsearch":
    beamsearch = BeamSearch(district, 5)
    result = beamsearch.run()
    append_to_csv(result, algorithm)

elif algorithm == "depthfirst":
    depthfirst = DepthFirst(district, len(district.houses), True)
    result = depthfirst.run()

elif algorithm == "hillclimber":
    hillclimber = HillClimber(district)
    result = hillclimber.run_hill_climber(district, 1)
    append_to_csv(result, algorithm)

elif algorithm == "simulatedannealing":
    simulated = Simulatedannealing(district)
    result = simulated.run_hill_climber(district, 1)
    append_to_csv(result, algorithm)
    
else:
    print("Algorithm does not exist")
