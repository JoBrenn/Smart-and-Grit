""" Main to run the code in this repository.

File: main.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 10/01/24 (11/01/24)

Description:   Depending on input gives a vizualization of data.

Usage:  python3 main.py [argument 1]
        argument 1:     - format:   returns output-format.json vizualization
                        - 1-3:      returns specified district vizualization
"""
from code.helpers.helpers import *


if __name__ == "__main__":

    method, data, runs, district = None, None, None, None

    print("Running SmartGrid main", end="\n\n")

    # Get method input (LOCATION: code/helpers/helpers.py)
    method = get_method_input()

    # General Methods LOAD and Format
    if method in {"format", "load"}:
        data = run_general_method(method)
    # Algo Methods:
    else:
        # Select district between 1 - 3 (LOCATION: code/helpers/helpers.py)
        district = get_district_input()

        # Select runs >0 (LOCATION: helpers)
        runs = get_runs_input(method)

        # Run algorithm (LOCATION: code/helpers/helpers.py)
        data = run_algo_method(method, district, runs)

        # Write data to JSON (LOCATION: code/helpers/helpers.py)
        write_data_to_JSON(data, method, district, runs)

    # Plot data (LOCATION: code/helpers/helpers.py)
    plot_data(data, method, runs, district)
