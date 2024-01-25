from code.modules.district import District
from code.modules.battery import Battery
from code.modules.house import House
from random import shuffle
from code.algorithms.manhattan_distance import return_manhattan_distance, create_cable

class Closest:
    """TODO
    """
    def __init__(self, district, max_runs):
        self.district = district
        self.max_runs = max_runs
        shuffle(self.district.houses)

    def run(self):
        for house in self.district.houses:
            closest_dist = float('inf')
            closest_bat = None

            for battery in self.district.batteries:
                #if battery.left_over_capacity > house.output:
                dist = return_manhattan_distance(house, tuple([battery.row, battery.column]))

                if dist < closest_dist:
                    closest_dist = dist
                    closest_bat = battery

            if closest_bat != None:      
                closest_bat.add_house(house)
                create_cable(house, [closest_bat.row, closest_bat.column])
            

    def is_valid(self):
        if len(self.district.houses) == 0:
            return True
        return False
    
        """ 
        if max_runs == 0: 
                print("Max runs reached")
                return False
        else:
            print(f"HOUSE NOT ASSIGNED {house.row}, {house.column}")
            max_runs -= 1
            district = run_closest(max_runs)
            break"""







def run_closest(max_runs):
    district = District(1, "costs-own")
    #print(district)

    shuffle(district.houses)
    """for battery in district.batteries:
        print(f"id: {battery.battery_id} cap: {battery.left_over_capacity}")"""

    for house in district.houses:
        closest_dist = float('inf')
        closest_bat = None

        for battery in district.batteries:
            #if battery.left_over_capacity > house.output:
            dist = return_manhattan_distance(house, tuple([battery.row, battery.column]))

            if dist < closest_dist:
                closest_dist = dist
                closest_bat = battery

        if closest_bat != None:      
            closest_bat.add_house(house)
            create_cable(house, [closest_bat.row, closest_bat.column])
        elif max_runs == 0: 
            print("Max runs reached")
            return False
        else:
            print(f"HOUSE NOT ASSIGNED {house.row}, {house.column}")
            max_runs -= 1
            district = run_closest(max_runs)
            break

    district.district_dict["costs-own"] = district.return_cost()

    return district
    