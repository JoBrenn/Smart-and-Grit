def greedy_assignment(district):
    """ Adds each house to the battery with the most capacity left
        pre: an instance of the District class"""
    max_capacity = 0
    
    for house in district.houses:
        # Determines battery with most capacity
        max_battery = None
        max_capacity = 0

        for battery in district.batteries:
            if battery.left_over_capacity > max_capacity and \
               battery.left_over_capacity >= house.output:
                max_capacity = battery.left_over_capacity
                max_battery = battery
            
        # Quickfix for now
        if max_battery != None:
            max_battery.add_house(house)
            
