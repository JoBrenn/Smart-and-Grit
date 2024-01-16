print(output[0])
total_cables = 0
for battery in output[1:]:
    for house in battery["houses"]:
        total_cables += len(house["cables"])
print(total_cables)
print(f"Total cable cost is: {total_cables * 9}")
print(total_cables, f"+ 25000 for batteries is: {total_cables * 9 + 25000}")
