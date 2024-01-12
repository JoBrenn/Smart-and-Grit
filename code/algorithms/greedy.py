def greedy_assignment(district):
    """ Adds each house to the battery with the most capacity left
        pre: an instance of the District class"""
    max_capacity = 0
    
    for house in district.houses:
        # Determines battery with most capacity
        for battery in district.batteries:
            #print(battery.left_over_capacity)
            if battery.left_over_capacity > max_capacity and \
               battery.left_over_capacity >= house.output:
                #print("True")
                max_capacity = battery.left_over_capacity
                max_battery = battery
                max_capacity = 0

        max_battery.add_house(house)
