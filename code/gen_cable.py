

def get_cable_points(battery: tuple[int], house: tuple[int]) -> tuple[int]:
    """Generates the points from house to cable
       From house first up or down then left or right"""
    points = [house, (house[0], battery[1]), battery]
    print(points)
    return tuple(points)



def get_cable_segments(cable_points: tuple[int]) -> tuple[int]:
    segment_points = [cable_points[0]]

    
    for main_point in range(len(cable_points) - 1):
        diff_x = cable_points[main_point + 1][0] - segment_points[main_point][0]
        diff_y = cable_points[main_point + 1][1] - segment_points[main_point][1]
        print(diff_y)
        
        
        for point in range(diff_x + diff_y):
            last = segment_points[-1]
            if last == cable_points[-1]:
                break

            print(f"Old {segment_points[-1]}")
            
            if diff_x == 0:
                dist = cable_points[main_point + 1][1] - last[1]
                print(f"Dist {dist}")
                segment_points.append((last[0], last[1] + int(dist/abs(dist))))
            else:
                dist = cable_points[main_point + 1][0] - last[0]
                print(f"Dist {dist}")
                segment_points.append((last[0] + int(dist/abs(dist)), last[1]))
            #print(f"New {segment_points[-1]}")
            

            print(f"Add {int(dist/abs(dist))}")


    # Append the final point, the battery
    #segment_points.append(cable_points[-1])

    return tuple(segment_points)

test = get_cable_points((38,12),(33,7))
test2 = get_cable_segments(test)

print(test2)