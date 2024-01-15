from code.modules.district import *
from code.algorithms.random import *
from code.algorithms.greedy import *

def runs_algorithms_to_costs(district_number, runs, alg_method) -> list:
    outputs = []

    for run in range(runs):
        district = District(district_number, "costs-own")
        if alg_method == "--randrwalk":
            output = run_random_assignment_random_walk(district)
        elif alg_method == "--randmanh":
            output = run_random_assignment_shortest_distance(district, "costs-own")
        # elif alg_method == "--greedmanh":
        #     output = run_greedy_assignment_shortest_walk(district, ...)
        else:
            return 0
        outputs.append(output[0]["costs-own"])

    return outputs
