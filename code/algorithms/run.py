from code.modules.district import *
from code.algorithms.random import *
from code.algorithms.greedy import *

def runs_algorithms_to_costs(district_number: int, runs: int, alg_method: str) -> list[int]:
    """ Create list of outputs, used for mpl histogram."""
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
        create_cable(house_1, battery)

    output = district.return_output()
    return output

def run_random_assignment_shortest_distance(district, costs_type) -> list:
    """ Randomly assigns the houses in a district to batteries and
        lays connections along the shortest Manhattan distance.
        Plots the grid
        post: returns output list"""

    connections = random_assignment(district)
    for house in connections:
        battery = connections[house]
        # Add the house to the battery connection (such that dictionary is added)
        battery.add_house(house)
        create_cable(house, (battery.row, battery.column))
    district.district_dict[f"{district.costs_type}"] = district.return_cost()

    output = district.return_output()

    return output


def run_random_assignment_shortest_distance_with_capacity(district, costs_type) -> list:
    """ Randomly assigns the houses in a district to batteries with enough
        capacity and lays connections along the shortest Manhattan distance.
        Plots the grid
        post: returns output list"""

    connections = random_assignment_capacity(district)
    for house in connections:
        battery = connections[house]
        create_cable(house, (battery.row, battery.column))
    district.district_dict[f"{district.costs_type}"] = district.return_cost()
    output = district.return_output()

    return output

def run_greedy_assignment_shortest_walk(district, costs_type: str) -> list:
    """ Creates cables between houses and batteries that have
        been assigned using the greedy algorithm and plots this.
        Starts at a random house.
        post: returns output list"""

    # Uses greedy algorithm to assign houses to batteries
    connections = greedy_assignment(district)
    
    for n, house in enumerate(connections):
        battery = connections[house]
        if n == 0:
            create_cable(house, (battery.row, battery.column))
            
        else:
            shortest = tuple([battery.row, battery.column])
            shortest_dist = (abs(shortest[0] - house.row) + abs(shortest[1] - house.column))
            for cable in battery.cables:
                distance = (abs(cable[0] - house.row) + abs(cable[1] - house.column))
                #print(f"Shortest {shortest}")
                if distance < shortest_dist:
                    shortest = tuple([cable[0], cable[1]])
                    

            create_cable(house, shortest)

            for o, cable_2 in enumerate(house.cables):
                if o < len(house.cables) - 1 and tuple([battery.row, battery.column]) == cable_2:
                    print("-----------ERROR-----------")
                    print(f"House: {n}, Cable {o}, Coord: {cable_2}")


        battery.add_house_cables(house)
    output = district.return_output()

    return output
    """
    # Loops over each house in each battery to create cable paths
    for battery in district.batteries:
        for n, house in enumerate(battery.houses):
            if n == 0:
                create_cable(house, (battery.row, battery.column))
                
            else:
                shortest = tuple([battery.row, battery.column])
                shortest_dist = (abs(shortest[0] - house.row) + abs(shortest[1] - house.column))
                for cable in battery.cables:
                    distance = (abs(cable[0] - house.row) + abs(cable[1] - house.column))
                    #print(f"Shortest {shortest}")
                    if distance < shortest_dist:
                        shortest = tuple([cable[0], cable[1]])
                        

                create_cable(house, shortest)
                
                for o, cable_2 in enumerate(house.cables):
                    if o < len(house.cables) - 1 and tuple([battery.row, battery.column]) == cable_2:
                        print("-----------ERROR-----------")
                        print(f"House: {n}, Cable {o}, Coord: {cable_2}")


            battery.add_house_cables(house)
    district.district_dict[f"{district.costs_type}"] = district.return_cost()"""
    

def run_alg_manh(district, assign_method, costs_type: str) -> list:
    connections = assign_method(district)

    for n, house in enumerate(connections):
        battery = connections[house]
        if n == 0:
            #print(house)
            create_cable(house, (battery.row, battery.column))     
        else:
            shortest = tuple([battery.row, battery.column])
            shortest_dist = (abs(shortest[0] - house.row) + abs(shortest[1] - house.column))
            for cable in battery.cables:
                distance = (abs(cable[0] - house.row) + abs(cable[1] - house.column))
                #print(f"Shortest {shortest}")
                if distance < shortest_dist:
                    shortest = tuple([cable[0], cable[1]])
                    

            create_cable(house, shortest)

            for o, cable_2 in enumerate(house.cables):
                if o < len(house.cables) - 1 and tuple([battery.row, battery.column]) == cable_2:
                    print("-----------ERROR-----------")
                    print(f"House: {n}, Cable {o}, Coord: {cable_2}")


        battery.add_house_cables(house)

    district.district_dict[f"{district.costs_type}"] = district.return_cost()
    output = district.return_output()
    
    return output