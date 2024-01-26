from code.algorithms.hill_climber import HillClimber
from code.algorithms.simulatedannealing import Simulatedannealing
from code.modules.district import District

import csv
from copy import deepcopy
import matplotlib.pyplot as plt

def simulannealing_one_climb(district: District) -> None:
    """ Runs simulated annealing iteration one time and adds all costs to csv file
        Params:
            district         (District): District object from which we want to start
        Returns:
            none
            alters csv file with cost outputs
    """
    sim = Simulatedannealing(district, 1000)

    with open("results/simulatedannealing/simulatedannealing.csv", 'w', newline='') as output_file,\
        open("results/simulatedannealing/simulatedannealing_penalty.csv", 'w', newline='') as output_penalty:
        result_writer = csv.writer(output_file, delimiter=',')
        result_writer_penalty = csv.writer(output_penalty, delimiter=',')
        
        
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
                result_writer.writerow([district_work.return_cost()])
                result_writer_penalty.writerow([sim.return_total_cost(district_work)])
                print(sim.return_total_cost(previous_district))
                print(sim.return_total_cost(district_work))
                # If output is unchanged, add one to count
                if previous_district.return_output() == district_work.return_output():
                    unchanged_count += 1
                else:
                    unchanged_count = 0
        # Reset iterations and temperature
        sim.iterations = 0
        sim.temp = sim.temp_0

def simulannealing_one_climb_graph_costs():
    fig, ax = plt.subplots()
    
    with open("results/simulatedannealing/simulatedannealing.csv", 'r') as f:
        reader = csv.reader(f)
        #for cost in reader:
        #    print(cost)
        values = [int(row[0]) for row in reader]
    ax.plot(values, label='Simulated annealing costs (no constraint)')
    ax.set_title('Simulated annealing')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Costs')
    fig.savefig("results/simulatedannealing/one_climb.png")
    plt.show()
    
def simulannealing_one_climb_graph_penalty():
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
    
def simulannealing_temp_comparison(district):
    for temp in range(2700, 3100, 100):
        values = []
        #for i in range(100):
            