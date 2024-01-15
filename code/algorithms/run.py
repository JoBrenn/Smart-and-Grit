from code.modules.district import *
from code.algorithms.random import *
from code.algorithms.greedy import *

def runs_algorithms_to_costs(district_number, runs, alg_method) -> list[int]:
    outputs = []

    for run in range(runs):
        district = District(district_number, "costs-own")
        if alg_method == "--randmanh":
            output = run_random_assignment_shortest_distance(district, "costs-own")
        elif alg_method == "--randmanhcap":
            output = run_random_assignment_shortest_distance_with_capacity(district, "costs-own")
        else:
            return 0
        outputs.append(output[0]["costs-own"])

    return outputs

def run_random_assignment_random_walk(district) -> list:
    """ Randomly assigns the first house in a district to a battery and
        lays a connection along the shortest Manhattan distance.
        Plots the grid
        post: returns output list"""

    connections = random_assignment(district.batteries, district.houses)
    house_1 = list(connections.keys())[0]
    battery = connections[house_1]
    battery.add_house(house_1)
    points_walked = random_walk((int(house_1.row), int(house_1.column)), (int(battery.row), int(battery.column)), 50)
    # Add a cable segment between all the points visited in the random walk
    for i in range(len(points_walked) - 1):
        house_1.add_cable_segment((points_walked[i][0], points_walked[i][1]),\
                        (points_walked[i + 1][0], points_walked[i + 1][1]))

    output = district.return_output()
    return output

def run_random_assignment_shortest_distance(district, costs_type) -> list:
    """ Randomly assigns the houses in a district to batteries and
        lays connections along the shortest Manhattan distance.
        Plots the grid
        post: returns output list"""

    connections = random_assignment(district.batteries, district.houses)
    for house in connections:
        battery = connections[house]
        # Add the house to the battery connection (such that dictionary is added)
        battery.add_house(house)
        district.district_dict[costs_type] += create_cable(house, battery)

    output = district.return_output()

    return output


def run_random_assignment_shortest_distance_with_capacity(district, costs_type) -> list:
    """ Randomly assigns the houses in a district to batteries with enough
        capacity and lays connections along the shortest Manhattan distance.
        Plots the grid
        post: returns output list"""

    connections = random_assignment_capacity(district.batteries, district.houses)
    for house in connections:
        battery = connections[house]
        district.district_dict[costs_type] += create_cable(house, battery)

    output = district.return_output()

    return output

def run_greedy_assignment_shortest_walk(district, costs_type: str) -> list:
    """ Creates cables between houses and batteries that have
        been assigned using the greedy algorithm and plots this.
        Starts at a random house.
        post: returns output list"""

    start = randint(0, len(district.houses) - 1)
    # Uses greedy algorithm to assign houses to batteries
    greedy_assignment(district, start)

    # Loops over each house in each battery to create cable paths
    for battery in district.batteries:
        for house in battery.houses:
            district.district_dict[costs_type] += create_cable(house, battery)

    output = district.return_output()

    return output

def run_greedy_assignment_shortest_walk(district, costs_type: str) -> list:
    """ Creates cables between houses and batteries that have
        been assigned using the greedy algorithm and plots this.
        Starts at a random house.
        post: returns output list"""

    start = randint(0, len(district.houses) - 1)
    # Uses greedy algorithm to assign houses to batteries
    greedy_assignment(district, start)

    # Loops over each house in each battery to create cable paths
    for battery in district.batteries:
        for house in battery.houses:
            district.district_dict[costs_type] += create_cable(house, battery)

    output = district.return_output()

    return output
