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
from code.visualisation.visualize import plot_output
from code.modules.district import District
from code.algorithms.random import *
from code.algorithms.greedy import *
from code.algorithms.run import *
from code.helpers.helpers import *


if __name__ == "__main__":
    # At least 1 argument
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        print("Usage: python3 main.py <district> --<method> [options]")
    # Shows format output
    elif sys.argv[1] == "--format":
        data = load_JSON_output("data/output-format.json")
        plot_output(data)
    # Shows the user a manual
    elif sys.argv[1] == "--help":
            print("Usage: python3 main.py <district> --[method]")
            print("Methods:")
            print("--help: display help manual")
            print("--format: display formatted output")
            print("--h[isto[gram]]: Get histogram of N runs of random assignment Manhattan distance algorithm.")
            print("--randrwalk:  Randomly assigns houses to batteries. " + \
                                "Creates cable path through randomly taking random steps until destination is reached")
            print("--randmanh: Randomly assigns houses to batteries. " +  \
                    "Creates the cable path through the Manhattan distance from house to battery")
            print("--greedmanh: Uses greedy algorithm to assign houses to batteries. " + \
                    "Creates the cable path through the Manhattan distance from house to battery")
            print("--greedmanhcap: Uses greedy algorithm to assign houses to batteries. " + \
                    "Creates the cable path through the Manhattan distance from house to battery")
    elif sys.argv[1] in ["--h", "--histo", "--histogram"]:
        if len(sys.argv) < 4 or sys.argv[2] == "--help" or not sys.argv[3].isnumeric():
            print("Usage: python3 main.py --histogram --<method> <distrinct> [runs]")
        else:
            # Default value
            runs = 10

            if len(sys.argv) == 4:
                alg_method = sys.argv[2]
                district_number = int(sys.argv[3])
            elif len(sys.argv) == 5:
                alg_method = sys.argv[2]
                district_number = int(sys.argv[3])
                runs = int(sys.argv[4])

            outputs = runs_algorithms_to_costs(district_number, runs, alg_method)
            plot_output_histogram(outputs, alg_method, runs)

    # Shows output of one district between 1 - 3
    elif sys.argv[1] in ["--randmanh", "--randmanhcap", "--randrwalk", "--greedmanh"]:
        if len(sys.argv) < 3 or sys.argv[2] == "--help" or not sys.argv[2].isnumeric():
            print("Usage: python3 main.py --<method> <district>")
        else:
            alg_method = sys.argv[1]
            district = District(int(sys.argv[2]), "costs-own")
            method = "costs-own"

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

                output = run_random_assignment_random_walk(district)
                method = "Random + random walk"

            elif alg_method == "--randmanh":
                """
                    Here we again apply a random assignment of houses to batteries,
                    not taking the capacity into account. Instead of a random walk,
                    we now implement the shortest Manhattan distance.
                """

                output = run_random_assignment_shortest_distance(district, method)
                method = "Random + Manhattan"

            elif alg_method == "--randmanhcap":
                """
                    Here we again apply a random assignment of houses to batteries,
                    not taking the capacity into account. Instead of a random walk,
                    we now implement the shortest Manhattan distance.
                """

                output = run_random_assignment_shortest_distance_with_capacity(district, method)
                method = "Random + Manhattan + Capacity"
            elif alg_method == "--greedmanh":
                """
                    Here we apply a greedy algorithm. A house is assigned to the battery,
                    starting at a random house, with the most capacity left.
                    The path of the cable is created using the shortest Manhattan distance
                    from the house towards the battery
                """

                output = run_greedy_assignment_shortest_walk(district, method)
                # print(f"The cost for greedy assignment and shortest Manhattan distance in district {district.district} is {district.return_cost()}.")
                method = "Greedy + Manhattan"

            # Plot the output
            plot_output(output, alg_method, district, method)

            # Write output to JSON file
            write_output_to_JSON(output, alg_method[2:])

    else:
        print("Invalid input.")
