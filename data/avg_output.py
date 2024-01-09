avg = 0
houses = 0
total_output = 0

with open("./data/district_1/district-1_houses.csv", "r") as f:
    for line in f:
        if houses == 0:
            houses += 1
            continue
        house_output = line.split(",")[2].strip()
        total_output += float(house_output)
        houses += 1

avg = total_output / houses
print(avg)
