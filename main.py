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
from code.gen_cable import *
 
   
if __name__ == "__main__":
    # At least 1 argument
    if len(sys.argv) < 2:
        print("Usage: python3 main.py [desired district]")
    # Shows format output
    elif sys.argv[1] == "format":
        data = load_JSON_output("output/output-format.json")
        plot_output(data)
    # Shows output of one district between 1 - 3
    elif sys.argv[1].isnumeric() and 1 <= int(sys.argv[1]) <= 3:
        district = District(int(sys.argv[1]), "costs-own")    

        """
            Here we apply a random assignment of houses to batteries,
            not taking the capacity into account. Furthermore is a 
            random walk used for the connections between house and
            batttery.
        """
        """connections = random_assignment(district.batteries, district.houses)
        print(connections)
        for house in connections:
            battery = connections[house]
            # Add the house to the battery connection (such that dictionary is added)
            battery.add_house(house)
            points_walked = random_walk(int(house.row), int(house.column), int(battery.row), int(battery.column), 50)
            # Add a cable segment between all the points visited in the random walk
            for i in range(len(points_walked) - 1):
                house.add_cable_segment(points_walked[i][0], points_walked[i][1],\
                                  points_walked[i + 1][0], points_walked[i + 1][1])
        plot_output(district.return_output())
        """

        # Testing greedy algorithm
        greedy_assignment(district)
        house_num = 0
        for bat_num, battery in enumerate(district.batteries):
            for house in battery.houses:
                print("House {:3} Battery {:}".format(house_num + 1, bat_num + 1))
                house_num += 1

                corners = get_cable_corner()
                segments = get_cable_segments(corners)

                

                

        plot_output(district.return_output())



    else:
        print("Invalid input.")


    