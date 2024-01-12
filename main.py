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
from code.visualisation.visualize_output import *
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
            print("Options:")
            print("--help: display help manual")
            print("--randrwalk:  Randomly assigns houses to batteries." + \
                                "Creates cable path thorugh randomly taking random steps until destination is reached")
            print("--randmanh: Randomly assigns houses to batteries. " +  \
                    "Creates the cable path through the Manhattan distance from house to battery")
            print("--greedmanh: Uses greedy algorithm to assign houses and batteries. " + \
                    "Creates the cable path through the Manhattan distance from house to battery")
    # Shows output of one district between 1 - 3
    elif sys.argv[1].isnumeric() and 1 <= int(sys.argv[1]) <= 3:
        district = District(int(sys.argv[1]), "costs-own")
        # Defaults to first method if none are selected   
        if len(sys.argv) == 3:
            alg_method = sys.argv[2]
        else: 
            alg_method = "--randrwalk"

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
            district_random_walk = District(int(sys.argv[1]), "costs-own")    
            connections = random_assignment(district_random_walk.batteries, district_random_walk.houses)
            house_1 = list(connections.keys())[0]
            battery = connections[house_1]
            battery.add_house(house_1)
            points_walked = random_walk((int(house_1.row), int(house_1.column)), (int(battery.row), int(battery.column)), 50)
            # Add a cable segment between all the points visited in the random walk
            for i in range(len(points_walked) - 1):
                house_1.add_cable_segment((points_walked[i][0], points_walked[i][1]),\
                                (points_walked[i + 1][0], points_walked[i + 1][1]))
            plot_output(district_random_walk.return_output(), "Random + random walk")

        elif alg_method == "--randmanh":
            """
                Here we again apply a random assignment of houses to batteries,
                not taking the capacity into account. Instead of a random walk,
                we now implement the shortest Manhattan distance.
            """
            
            district_random_shortest = District(int(sys.argv[1]), "costs-own")
            connections = random_assignment(district_random_shortest.batteries, district_random_shortest.houses)
            for house in connections:
                battery = connections[house]
                # Add the house to the battery connection (such that dictionary is added)
                battery.add_house(house)
                district_random_shortest.create_cable(house, battery)
            plot_output(district_random_shortest.return_output(), "Random + Manhattan")
            
            print(f"The cost for random assignment and shortest Manhattan distance in district {district.district} is {district_random_shortest.return_cost()}.")
            
        elif alg_method == "--greedmanh":
            """
                Here we apply a greedy algorithm. A house is assigned to the battery
                with the most capacity left. The path of the cable is created using 
                the Manhattan distance from the house towards the battery
            """
            district = District(int(sys.argv[1]), "costs-own")

            greedy_assignment(district)
            
            for battery in district.batteries:
                for house in battery.houses: 
                    district.create_cable(house, battery)
            plot_output(district.return_output(), "Greedy + Manhattan")

            print(f"The cost for random assignment and shortest Manhattan distance in district {district.district} is {district.return_cost()}.")

    else:
        print("Invalid input.")


    