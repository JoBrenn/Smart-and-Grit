

from code.visualisation.visualize import *
import csv

filename = "output/csv/costs_hc.csv"
values = []
with open(filename, "r") as f:
    read = csv.reader(f)
    for row in read:
        values.append(int(row[0]))


plot_output_histogram(values, "simulatedannealing", 318, 1)