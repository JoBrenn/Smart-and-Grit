""" Experiments concerning HillClimber algorithm

File: hill_climb_experiment.py

Author:    Kathy Molenaar

Date: 26/01/24

Description:

Contains functions in which experiments concerning Hill Climber
happen.

Usage:
from experiments.hillclimber.hill_climb_experiment import ...
"""

from code.algorithms.hill_climber import HillClimber
from code.modules.district import District

import csv
from copy import deepcopy
import matplotlib.pyplot as plt

def hillclimb_one_climb(district: District) -> None:
    """ Runs hillclimber iteration one time and adds all costs to csv file
        Params:
            district         (District): District object from which we want to start
        Returns:
            none
            alters csv file with cost outputs
    """
    
    hc = HillClimber(district)

    with open("results/hillclimber/hillclimber.csv", 'w', newline='') as output_file,\
        open("results/hillclimber/hillclimber_penalty.csv", 'w', newline='') as output_penalty:
        result_writer = csv.writer(output_file, delimiter=',')
        result_writer_penalty = csv.writer(output_penalty, delimiter=',')
        
        
        # Make copy of empty district, such that always start with empty
        district_empty = copy.deepcopy(district)
        
        # Initialize a random district configuration
        district_work = copy.deepcopy(hc.random_start_state(district_empty))

        unchanged_count = 0
        
        for iteration in range(hc.iterations_total + 1):
            # Stop when the state hasn't improved N times
            if unchanged_count == 1000 - 1:
                return district_work
            else:
                previous_district = copy.deepcopy(district_work)
                # Go over to switch when we have a valid solution
                if hc.check_valid(previous_district) is True:
                    district_work = hc.one_switch_iteration(district_work)
                else:
                    district_work = hc.one_change_iteration(district_work)
                result_writer.writerow([district_work.return_cost()])
                result_writer_penalty.writerow([hc.return_total_cost(district_work)])
                print(hc.return_total_cost(previous_district))
                print(hc.return_total_cost(district_work))
                # If output is unchanged, add one to count
                if previous_district.return_output() == district_work.return_output():
                    unchanged_count += 1
                else:
                    unchanged_count = 0
            
def hillclimb_one_climb_graph_costs():
    fig, ax = plt.subplots()
    
    with open("results/hillclimber/hillclimber.csv", 'r') as f:
        reader = csv.reader(f)
        values = [int(row[0]) for row in reader]
    ax.plot(values, label='HillClimber costs (no constraint)')
    ax.set_title('Hill Climber')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Costs')
    fig.savefig("results/hillclimber/one_climb.png")
    plt.show()

def hillclimb_one_climb_graph_penalty():
    fig, ax = plt.subplots()
    
    with open("results/hillclimber/hillclimber_penalty.csv", 'r') as f:
        reader = csv.reader(f)
        #for cost in reader:
        #    print(cost)
        values = [float(row[0]) for row in reader]
    ax.plot(values, label='HillClimber costs (with constraint)')
    ax.set_title('Hill Climber')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Costs')
    fig.savefig("results/hillclimber/one_climb_penalty.png")
    plt.show()