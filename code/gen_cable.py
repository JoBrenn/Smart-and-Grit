

def get_cable_points(battery: tuple[int], house: tuple[int]) -> tuple[int]:
    """Generates the points from house to cable"""
    points = [house, (house[0], battery[1]), battery]

    return tuple(points)


def get_cable_segments(cable_points: tuple[int]) -> tuple[int]:
    segment_points = [cable_points[0]]


    for main_point in range(len(cable_points) - 1):
        diff_x = segment_points[main_point][0] - cable_points[main_point + 1][0]
        diff_y = segment_points[main_point][1] - cable_points[main_point + 1][1]


        for point in range(diff_x + diff_y):
            last = segment_points[-1]

            if diff_x == 0:
                dist = last[1] - main_point[1]
                points.append(last[0], last[1] + (dist/abs(dist)))
            else:
                dist = last[0] - main_point[0]
                points.append(last[0] + dist/abs(dist), last[1] )


    # Append the final point, the battery
    segment_points.append(cable_points[-1])

    return tuple(segment_points)

test = get_cable_points((38,12),(33,7))
test2 = get_cable_segments(test)

print(test2)
