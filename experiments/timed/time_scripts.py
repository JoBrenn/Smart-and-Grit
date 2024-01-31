""" Script to run timed algorithm test

File: time_scripts.py

Authors:    Jesper Vreugde

Date: 26/01/24 (31/01/24)

Description:
This is a script to run a timed test for different algorithms

Usage:  from experiments.timed.time_script import run_time_script
"""

from subprocess import call
from time import time

                                                                 
def run_time_script(method: str) -> None:
    """ Runs the chosen algorithm consecutively for 2700 seconds
        Params:
            method(str):    Algorithm method
        Returns:
            None
    """
    start = time()
    n_runs = 0

    while time() - start < 2700:
        print(f"run: {n_runs}")
        call(["timeout", "500", "python3", "-m", "experiments.timed.run_algs",\
               f"{method}"])
        n_runs += 1
