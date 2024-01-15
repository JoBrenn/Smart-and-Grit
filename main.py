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
        print("Usage: python3 main.py <district> --[method]")
    # Shows format output
    elif sys.argv[1] == "format":
        data = load_JSON_output("output/output-format.json")
        plot_output(data)
    # Shows the user a manual
    elif sys.argv[1] == "--help":
            print("Usage: python3 main.py <district> --[method]")
            print("Methods:")
            print("--help: display help manual")
            print("--randrwalk:  Randomly assigns houses to batteries. " + \
                                "Creates cable path through randomly taking random steps until destination is reached")
            print("--randmanh: Randomly assigns houses to batteries. " +  \
                    "Creates the cable path through the Manhattan distance from house to battery")
            print("--greedmanh: Uses greedy algorithm to assign houses to batteries. " + \
                    "Creates the cable path through the Manhattan distance from house to battery")
    elif sys.argv[1] in ["h", "histo", "histogram"]:
        if sys.argv[2].isnumeric() and 1 <= int(sys.argv[1]) <= 3:
            if len(sys.argv) == 3:
                runs = 10
                alg_method = "--randmanh"
            elif len(sys.arg) == 4 and sys.argv[3].isnumeric():
                runs == sys.argv[3]
                alg_method = "--randmanh"
            elif len(sys.arg) == 5 and sys.argv[3][:1] == "--" and sys.argv[4].isnumeric():
                runs == sys.argv[4]
                alg_method = sys.argv[3]
            else:
                print("python3 main.py histo <distrinct> --[method] [runs]")

            outputs = []




            plot_output_histogram(outputs)


        else:
            print("Please specify distrinct.")


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

            run_random_assingment_random_walk(district)

        elif alg_method == "--randmanh":
            """
                Here we again apply a random assignment of houses to batteries,
                not taking the capacity into account. Instead of a random walk,
                we now implement the shortest Manhattan distance.
            """

            run_random_assignment_shortest_distance(district)

        elif alg_method == "--greedmanh":
            """
                Here we apply a greedy algorithm. A house is assigned to the battery
                with the most capacity left. The path of the cable is created using
                the shortest Manhattan distance from the house towards the battery
            """

            run_greedy_assignment_shortest_walk(district)


    else:
        print("Invalid input.")
