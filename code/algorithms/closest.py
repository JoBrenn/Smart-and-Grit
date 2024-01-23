from code.modules.district import District
from code.modules.battery import Battery
from code.modules.house import House
from code.algorithms.manhattan_distance import return_manhattan_distance, create_cable

def run_closest(district):
    for house in district.houses:
        closest_dist = float('inf')
        closest_bat = district.batteries[0]

        for battery in district.batteries:
            if battery.left_over_capacity > house.output:
                dist = return_manhattan_distance(house, tuple([battery.row, battery.column]))

                if dist < closest_dist:
                    closest_dist = dist
                    closest_bat = battery
                
        closest_bat.add_house(house)
        create_cable(house, [closest_bat.row, closest_bat.column])
    
    return district.return_output()
    