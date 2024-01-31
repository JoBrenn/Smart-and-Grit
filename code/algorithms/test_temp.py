### FUNC depth
def add_new_state(self, n, state, house, battery) -> None:
        """ 
            Params:
                state:      (District) a district state to be added
                battery:    (Battery) a battery 
            Returns: 
                None
        """
        child = copy.deepcopy(state)
        house_add = copy.deepcopy(house)
        create_cable(house_add, (battery.row, battery.column))
        child.batteries[n].add_house(house_add)
        self.states.append(child)

### CLOSEST
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

            return district           

    district.district_dict["costs-own"] = district.return_cost()

    return district

### DEPTH


def test_depth_district(district):
    depth = 5#len(district.houses)
    stack = [district]

    #state_set = set()
    lowest_costs = float('inf')
    lowest_costs_state = None

    houses = copy.deepcopy(district.houses)
    total = 0

    while len(stack) > 0:
        state = stack.pop()
        curr_depth = len(district.houses) - len(houses)

        # TODO Prunen

        #print("len: {:2} statelen: {:2} depth: {:2} stacklen: {:2}"\
         #   .format(len(houses),state.assigned_houses,curr_depth,len(stack)))
        """if state.assigned_houses == 1:
            print("train")

        if state.assigned_houses == 7:
            print("train2")"""



        if state.assigned_houses < depth and valid_cap(state):

            house = houses[state.assigned_houses]
            #print(house)
            for n, battery in enumerate(state.batteries):

                child = copy.deepcopy(state)
                house_add = copy.deepcopy(house)
                #house cables = []
                create_cable(house_add, (battery.row, battery.column))
                child.batteries[n].add_house(house_add)

                child.assigned_houses += 1
                # house_2 = copy.deepcopy()
                #child.batteries[n].append(house_2)
                stack.append(child)

        else:
            #print(f"{state.return_json_output()}")
            total += 1
            # check solution

            state.district_dict[f"{state.costs_type}"] = state.return_cost()
            #print(state.return_cost())

            if state.district_dict[district.costs_type] < lowest_costs:
                lowest_costs = state.district_dict[district.costs_type]
                lowest_costs_state = copy.deepcopy(state)
            #plot_output(state.return_output())

    #print(f"Lowest: {lowest_costs}")
    #print(total)
    #plot_output(lowest_costs_state.return_output())



district = District(1, "costs-own")

def valid_cap(state):
    for battery in state.batteries:
        if battery.left_over_capacity < 0:
            #print("Not valid")
            return False

        #print("Valid")
        return True


# Example code from Lecture Constructive algorithm by Bas Terwijn
def test_depth():
    depth = 11
    stack = [""]
    while len(stack) > 0:
        state = stack.pop()
        #print(state)
        #print("stack")
        if len(state) < depth:
            for i in ["1","2","3","4","5"]:
                child = copy.deepcopy(state)
                child += i
                # print(child)
                stack.append(child)
       # else:
            # check solution
            #print(state)
