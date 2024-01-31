from subprocess import call
from time import time

                                                                 
def run_time_script(method: str) -> None:
    """ Runs the chosen algorithm consecutively for 2700 seconds
        Params:
            method(str):    Algorithm method
        Returns:
            None
    """
    start = time.time()
    n_runs = 0

    while time.time() - start < 2700:
        print(f"run: {n_runs}")
        call(["timeout", "500", "python3", "-m", "experiments.timed.run_algs",\
               f"{method}"])
        n_runs += 1
