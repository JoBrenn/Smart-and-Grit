from code.algorithms.depth_first import DepthFirst #, BreadthFirst
from code.algorithms.breadth_first import BreadthFirst
from code.algorithms.closest import *
from code.modules.district import District
from code.visualisation.visualize import plot_output
from code.algorithms.combine_cables import *
from code.algorithms.manhattan_distance import *




#test_depth_district(district)
#test_depth()
#print(district.return_json_output())

#closest = run_closest(10)



"""print(district.batteries[0].houses[0].cables)
print()
print(district.houses[0].cables)"""
#plot_output(closest)
district = District(1, "costs-own")


depth = DepthFirst(district, 5)
result = depth.run()
plot_output(result.return_output())

"""
closest = Closest(district, 10)
closest_2 = closest.run()
if closest.return_valid():
    output = closest_2.return_output()
    plot_output(output)


print(closest.return_output()[0])
plot_output(closest.return_output())
closest_2 = combine_district(closest.return_output())

#print(closest_2[0][0])

print(closest_2[0][0])
plot_output(closest_2[0])"""

