def get_cable_corner(battery: tuple[int], house: tuple[int]) -> tuple[int]:
    """Generates the points from house to cable
        pre: tuples of battery and house location
        post: returns all corner points as tuples in a tuple"""
    points = [house]

    # Generate corners
    corners = [(house[0], battery[1])]

    for corner in corners:
        points.append(corner)

    points.append(battery)

    return tuple(points)

def get_cable_segments(corner_points: tuple[int]) -> tuple[int]:
    """ Returns the entire path between all corner points
        pre: corner points is a tuple of coordinate tuples
        post: returns a tuple of tuples of the cable coordinates"""
    # Adds first point of the list
    segment_points = [corner_points[0]]

    # Loops over each corner point
    for corner in range(len(corner_points) - 1):
        # Gets the distance between the last added point and the next corner
        diff_x = corner_points[corner + 1][0] - segment_points[-1][0]
        diff_y = corner_points[corner + 1][1] - segment_points[-1][1]

        # Loop for each segment point that should be added
        for point in range(diff_x + diff_y):
            last = segment_points[-1]

            # Break if final point is reached
            if last == corner_points[-1]:
                break

            # Walk on the y-axis if on the same column,
            if diff_x == 0:
                dist = corner_points[corner + 1][1] - last[1]
                segment_points.append((last[0], last[1] + int(dist/abs(dist))))
            # Or on the x-axis if on the same row
            else:
                dist = corner_points[corner + 1][0] - last[0]
                segment_points.append((last[0] + int(dist/abs(dist)), last[1]))

    return tuple(segment_points)

if __name__ == "__main__":
    # Test case
    test = get_cable_corner((50,128),(33,7))
    test2 = get_cable_segments(test)

    print(test2)
