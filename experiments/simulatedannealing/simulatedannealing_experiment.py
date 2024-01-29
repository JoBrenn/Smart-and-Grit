""" Experiments concerning Simulatedannealing algorithm

File: simulatedannealing_experiment.py

Author:    Kathy Molenaar

Date: 26/01/24

Description:

Contains functions in which experiments concerning Simulated Annealing
happen.

Usage:
from experiments.simulatedannealing.simulatedannealing_experiment import ...
"""

from code.algorithms.hill_climber import HillClimber
from code.algorithms.simulatedannealing import Simulatedannealing
from code.modules.district import District

import csv
import matplotlib.pyplot as plt
from copy import deepcopy
from statistics import mean 


def simulatedannealing_add_costs_to_list(district: District,\
                                         iterations: int = 1000,\
                                         temp: float = 4000) -> list:
    """ Runs simulated annealing iteration one time and adds all costs to list
        Params:
            district         (District): District object from which we want to start
        Returns:
            none
            alters lists with cost outputs
    """
    
    sim = Simulatedannealing(district, iterations, temp)
    costs = []
    costs_with_penalty = []

    # Make copy of empty district, such that always start with empty
    district_empty = deepcopy(district)
    
    # Initialize a random district configuration
    district_work = deepcopy(sim.random_start_state(district_empty))

    unchanged_count = 0
    
    for iteration in range(sim.iterations_total + 1):
        # Stop when the state hasn't improved N times
        if unchanged_count == 1000 - 1:
            return district_work
        else:
            previous_district = deepcopy(district_work)
            # Go over to switch when we have a valid solution
            if sim.check_valid(previous_district) is True:
                district_work = sim.one_switch_iteration(district_work)
            else:
                district_work = sim.one_change_iteration(district_work)
            costs.append([district_work.return_cost()])
            costs_with_penalty.append([sim.return_total_cost(district_work)])
            # If output is unchanged, add one to count
            if previous_district.return_output() == district_work.return_output():
                unchanged_count += 1
            else:
                unchanged_count = 0
    # Reset iterations and temperature
    sim.iterations = 0
    sim.temp = sim.temp_0
    
    return costs, costs_with_penalty
    
    
def simulatedannealing_one_climb(district: District, iteration: int = 10000) -> None:
    """ Runs simulated annealing iteration one time and adds all costs to csv file
        Params:
            district         (District): District object from which we want to start
        Returns:
            none
            alters csv file with cost outputs
    """

    costs, costs_with_penalty = simulatedannealing_add_costs_to_list(district, iteration)
    
    with open("results/simulatedannealing/simulatedannealing.csv", 'w', newline='') as output_file,\
        open("results/simulatedannealing/simulatedannealing_penalty.csv", 'w', newline='') as output_penalty:
        result_writer = csv.writer(output_file, delimiter=',')
        result_writer_penalty = csv.writer(output_penalty, delimiter=',')
        
        result_writer.writerows(costs)
        result_writer_penalty.writerows(costs_with_penalty)

def simulatedannealing_one_climb_graph_costs():
    """ Displays the costs of the iterations in a graph
        Params:
            district         (District): District object from which we want to start
        Returns:
            none
    """

    fig, ax = plt.subplots()
    
    with open("results/simulatedannealing/simulatedannealing.csv", 'r') as f:
        reader = csv.reader(f)
        values = [int(row[0]) for row in reader]

    ax.plot(values, label='Simulated annealing costs (no constraint)')
    ax.set_title('Simulated annealing')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Costs')
    fig.savefig("results/simulatedannealing/one_climb.png")
    plt.show()
    
def simulatedannealing_one_climb_graph_penalty():
    """ Displays the costs including penalties of the iterations in a graph
        Params:
            district         (District): District object from which we want to start
        Returns:
            none
    """
    fig, ax = plt.subplots()
    
    with open("results/simulatedannealing/simulatedannealing_penalty.csv", 'r') as f:
        reader = csv.reader(f)
        #for cost in reader:
        #    print(cost)
        values = [float(row[0]) for row in reader]
    ax.plot(values, label='Simulated annealing costs (with constraint)')
    ax.set_title('Simulated annealing')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Costs')
    fig.savefig("results/simulatedannealing/one_climb_penalty.png")
    plt.show()
    
def simulatedannealing_temp_comparison(district):
    """ Runs simulated annealing for different temperatures to compare them
        Creates csv for all temperatures, where rows are mean, min, max
        Params:
            district         (District): District object from which we want to start
        Returns:
            none
            adds mean, lowest and highest cost to csv for all temperatures
    """
    
    # Test for different temperatures
    for temp in range(3800, 4200, 100):
        all_costs = []
        all_costs_penalty = []

        # Repeat simulated annealing 100 times
        for n in range(100):
            print(f"Running Simulated {n}")
            costs_it, costs_it_penalty\
            = simulatedannealing_add_costs_to_list(district, 100, temp)
            all_costs.append(costs_it)
            all_costs_penalty.append(costs_it_penalty)

        results = []
        
        # Add for all iterations mean, minimum and maximum
        for iteration_costs in all_costs:
            for iteration in zip(*iteration_costs):
                results.append((mean(iteration), min(iteration), max(iteration)))
        
        # Add all iteration results to csv indicated with temperature
        with open(f"results/simulatedannealing/simulatedannealing_temp_{temp}.csv", 'w', newline='') as f:
            result_writer = csv.writer(f, delimiter=',')
            for result in results:
                result_writer.writerow(result)
                
def simulatedannealing_temp_comparison_mean_graph():
    """ Displays the mean costs of the iterations for all temperatures
        in one graph
        Params:
            district         (District): District object from which we want to start
        Returns:
            none
    """
    
    fig, ax = plt.subplots()
    mean_costs = []
    
    # Read in mean costs for all temperatures for all iterations
    for temp in range(3800, 4200, 100):
        with open(f"results/simulatedannealing/simulatedannealing_temp_{temp}.csv", 'r') as f:
            reader = csv.reader(f)
            mean_costs.append([float(row[0]) for row in reader])
    
    # Add for all temperatures graph 
    for temp, mean_cost in zip(range(3800, 4200, 100), mean_costs):
        ax.plot(mean_cost, label=f'Temperature {temp}')
        
    ax.legend(loc='upper right')
    ax.set_title('Simulated annealing temperatures n = 100')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Costs')
    fig.savefig("results/simulatedannealing/simulatedannealing_temp_mean.png")
    plt.show()
    
def simulatedannealing_temp_comparison_lowest_graph():
    """ Displays the lowest costs of the iterations for all temperatures
        in one graph
        Params:
            district         (District): District object from which we want to start
        Returns:
            none
    """
    
    fig, ax = plt.subplots()
    lowest_costs = []
    
    # Read in mean costs for all temperatures for all iterations
    for temp in range(3800, 4200, 100):
        with open(f"results/simulatedannealing/simulatedannealing_temp_{temp}.csv", 'r') as f:
            reader = csv.reader(f)
            lowest_costs.append([float(row[1]) for row in reader])
    
    # Add for all temperatures graph 
    for temp, lowest_cost in zip(range(3800, 4200, 100), lowest_costs):
        ax.plot(lowest_cost, label=f'Temperature {temp}')
        
    ax.legend(loc='upper right')
    ax.set_title('Simulated annealing temperatures n = 100')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Costs')
    fig.savefig("results/simulatedannealing/simulatedannealing_temp_lowest.png")
    plt.show()
    
def simulatedannealing_tuning(district: District, n: int):
    """ Tunes the simulated annealing parameters
        Creates n simulated annealing run for all combinations
        Adds best to csv file
        Params:
            district         (District): District object from which we want to start
        Returns:
            none
    """
    
    with open(f"results/simulatedannealing/simulatedannealing_tuning.csv", 'w', newline='') as f:
        result_writer = csv.writer(f, delimiter=',')    
        for temp in range(3800, 4200, 100):
            for iterations in range(8000, 14000, 2000):
                print(f"Running simulated annealing for\
                temp = {temp} and iterations = {iterations}")
                simul = Simulatedannealing(district, iterations, temp)
                district_work = simul.run_hill_climber(district, n, 1000)
                result_writer.writerow([district_work.return_cost()])
            