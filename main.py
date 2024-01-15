""" Main to run the code in this repository.

File: main.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 10/01/24 (11/01/24)

Description:   Depending on input gives a vizualization of data.

Usage:  python3 main.py [argument 1]
        argument 1:     - format:   returns output-format.json vizualization
                        - 1-3:      returns specified district vizualization
"""
from code.visualisation.visualize import *
from code.modules.district import *
from code.algorithms.random import *
from code.algorithms.greedy import *
#from code.gen_cable import *
 
   
if __name__ == "__main__":
    # At least 1 argument
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 main.py [desired district] --[desired method]")
    # Shows format output
    elif sys.argv[1] == "format":
        data = load_JSON_output("output/output-format.json")
        plot_output(data)
    # Shows the user a manual
    elif sys.argv[1] == "--help":
            print("Usage: python3 main.py [desired district] --[desired method]")
            print("Methods:")
            print("--help: display help manual")
            print("--randrwalk:  Randomly assigns houses to batteries. " + \
                                "Creates cable path through randomly taking random steps until destination is reached")
            print("--randmanh: Randomly assigns houses to batteries. " +  \
                    "Creates the cable path through the Manhattan distance from house to battery")
            print("--greedmanh: Uses greedy algorithm to assign houses to batteries. " + \
                    "Creates the cable path through the Manhattan distance from house to battery")
    # Shows output of one district between 1 - 3
    elif sys.argv[1].isnumeric() and 1 <= int(sys.argv[1]) <= 3:
        district = District(int(sys.argv[1]), "costs-own")
        # Defaults to first method if none are selected   
        if len(sys.argv) == 3:
            alg_method = sys.argv[2]
        else: 
            alg_method = "--randmanh"
        
        district = District(int(sys.argv[1]), "costs-own")
        # Run different methods based on user input
        if alg_method == "--randrwalk":
            """
                Here we apply a random assignment of houses to batteries,
                not taking the capacity into account. Furthermore is a 
                random walk used for the connections between house and
                batttery.
                Takes quite some time and is really messy in visualisation, 
                so we only take the first house into account.
            """ 
            
            run_random_assignment_random_walk(district)
            method = "Random + random walk"
            
        elif alg_method == "--randmanh":
            """
                Here we again apply a random assignment of houses to batteries,
                not taking the capacity into account. Instead of a random walk,
                we now implement the shortest Manhattan distance.
            """
            
            run_random_assignment_shortest_distance(district)
            method = "Random + Manhattan"
            
        elif alg_method == "--greedmanh":
            """
                Here we apply a greedy algorithm. A house is assigned to the battery
                with the most capacity left. The path of the cable is created using 
                the shortest Manhattan distance from the house towards the battery
            """
            district = District(int(sys.argv[1]), "costs-own")
            # Uses greedy algorithm to assign houses to batteries
            greedy_assignment(district)
            
            # Loops over each house in each battery to create cable paths
            for battery in district.batteries:
                for house in battery.houses: 
                    district.create_cable(house, battery)
            print(f"The cost for greedy assignment and shortest Manhattan distance in district {district.district} is {district.return_cost()}.")
            plot_output(district.return_output(), "Greedy + Manhattan")
       
       # Plot the output
       plot_output(district.return_output(), method)
            
    else:
        print("Invalid input.")


    