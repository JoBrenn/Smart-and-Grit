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

import json


if __name__ == "__main__":
    # At least 1 argument
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        print("Usage: python3 main.py <district> --<method> [options]")
    elif sys.argv[1] == "--load":
        try:
            if sys.argv[2] == "--format":
                print('cool')
                with open("output/output-format.json", "r") as f:
                    content = f.read()
                    data = json.loads(content)
            else:
                with open(f"output/JSON/{sys.argv[2]}", "r") as f:
                    content = f.read()
                    data = json.loads(content)
            plot_output(data)
        except:
            print("Usage: python3 --load <JSON_file>")

    # Shows format output
    elif sys.argv[1] == "--format":
        data = load_JSON_output("output/output-format.json")
        plot_output(data)
    # Shows the user a manual
    elif sys.argv[1] == "--help":
            print("Usage: python3 main.py <district> --[method]")
            print("Methods:")
            print("  --help:\t\t Display help manual")
            print("  --format:\t\t Display formatted output")
            print("  --h[isto[gram]]:\t Get histogram of N runs of random assignment Manhattan distance algorithm.")
            print("  --randrwalk:\t\t Randomly assigns houses to batteries. " + \
                                "Creates cable path through randomly taking random steps until destination is reached.")
            print("  --randmanh:\t\t Randomly assigns houses to batteries. \t\t\t\t(Manhattan Distance)")
            print("  --greedmanh:\t\t Uses greedy algorithm to assign houses to batteries. \t\t(Manhattan Distance)")
            print("  --greedmanhcap:\t Uses greedy algorithm to assign houses to capped batteries. \t(Manhattan Distance) ")
    elif sys.argv[1] in ["--h", "--histo", "--histogram"]:
        if len(sys.argv) < 4 or sys.argv[2] == "--help" or \
         not sys.argv[3].isnumeric() or not 1 <= int(sys.argv[3]) <= 3:
            print("Usage: python3 main.py --histogram --<method> <district> [runs]")
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
            plot_output_histogram(outputs, alg_method, runs, district_number)

    # Shows output of one district between 1 - 3
    elif sys.argv[1] in ["--randmanh", "--randmanhcap", "--randrwalk", "--greedmanh"]:
        if len(sys.argv) < 3 or sys.argv[2] == "--help" or not sys.argv[2].isnumeric():
            print("Usage: python3 main.py --<method> <district>")
        else:
            alg_method = sys.argv[1]
            district_number = int(sys.argv[2])
            district = District(district_number, "costs-own")
            cost_type = "costs-own"

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
                merge = False
                method = "Random + random walk"

            elif alg_method == "--randmanh":
                """
                    Here we again apply a random assignment of houses to batteries,
                    not taking the capacity into account. Instead of a random walk,
                    we now implement the shortest Manhattan distance.
                """
                #output = run_random_assignment_shortest_distance(district, method)
                assignment = random_assignment 
                method = "Random + Manhattan"

            elif alg_method == "--randmanhcap":
                """
                    Here we again apply a random assignment of houses to batteries,
                    not taking the capacity into account. Instead of a random walk,
                    we now implement the shortest Manhattan distance.
                """

                assignment = random_assignment_capacity
                method = "Random + Manhattan + Capacity"
                merge = False
                print(district.is_valid())

            elif alg_method == "--greedmanh":
                """
                    Here we apply a greedy algorithm. A house is assigned to the battery,
                    starting at a random house, with the most capacity left.
                    The path of the cable is created using the shortest Manhattan distance
                    from the house towards the battery
                """

                #output = run_greedy_assignment_shortest_walk(district, method)
                assignment = greedy_assignment
                merge = True
               
                # print(f"The cost for greedy assignment and shortest Manhattan distance in district {district.district} is {district.return_cost()}.")
                method = "Greedy + Manhattan"

            if alg_method != "--randrwalk":
                output = run_alg_manh(district, assignment, merge, cost_type)

            # Write output to JSON file
            write_output_to_JSON(output, alg_method[2:], district_number)

            # Plot the output
            plot_output(output, alg_method, district_number, method)



    else:
        print("Invalid input.")
