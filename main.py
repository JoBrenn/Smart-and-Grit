""" Main to run the code in this repository

File: main.py

Authors:    Kathy Molenaar
            Jesper Vreugde
            Jonas Brenninkmeijer

Date: 10/01/24 (11/01/24)

Description:
Depending on input gives a vizualization of data.

Usage:  python3 main.py [argument 1]
        argument 1:     - format:   returns output-format.json vizualization
                        - 1-3:      returns specified district vizualization
"""

import code.helpers.helpers as hlp


if __name__ == "__main__":

    method, data, runs, district = None, None, None, None

    print("Running SmartGrid main", end="\n\n")

    # Get method input
    method = hlp.get_method_input()

    # General Methods LOAD and Format
    if method in {"format", "load"}:
        data = hlp.run_general_method(method)

    # Algo Methods:
    else:
        # Select district between 1 - 3
        district = hlp.get_district_input()

        # Select runs >0
        runs = hlp.get_runs_input()

        # Run selected algorithm
        data = hlp.run_algo_method(method, district, runs)

        # Write data to JSON
        hlp.write_data_to_JSON(data, method, district, runs)

    # Plot data
    hlp.plot_data(data, method, runs, district)
