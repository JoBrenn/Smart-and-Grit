# from math import abs

def cable_gen(house, battery) -> list[str]:
    house_coord = house.x, house.y
    battery_coord = battery.x, battery.y

    cable_connections = [str(house_coord).strip('()')]

    needed_cables_x = house_coord[0] - battery_coord[0]
    needed_cables_y = house_coord[1] - battery_coord[1]

    print(needed_cables_x)
    print(needed_cables_y)

    total_needed_cables = abs(needed_cables_x) + abs(needed_cables_y)
    print(total_needed_cables)

    laid_cables_x = 0
    laid_cables_y = 0

    




    for cable in range(total_needed_cables):
        if laid_cables_y <= needed_cables_y:
            print("Y")
            cable_coord_x = str(house_coord[0])
            cable_coord_y = str(house_coord[1] + laid_cables_y)
            laid_cables_y += 1
        elif laid_cables_x <= needed_cables_x:
            print("X")
            cable_coord_x = str(house_coord[0] + laid_cables_x)
            cable_coord_y = str(house_coord[0])
            laid_cables_x += 1
        else:
            break
        cable_connections.append(cable_coord_x + ', ' + cable_coord_y)

    return cable_connections

class House:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Battery:

    def __init__(self, x, y):
        self.x = x
        self.y = y


house = House(5, 10)
battery = Battery(5, 15)

print(cable_gen(house, battery))

# tuple = 2, 4
# print(str(tuple).strip('()'))
