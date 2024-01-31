import subprocess
import time
import sys

start = time.time()
n_runs = 0

if len(sys.argv) == 2 and sys.argv[1] in ["closest", "beamsearch",\
                                          "random", "hillclimber", \
                                          "simulated", "depthfirst", "ooo"]:
    method = sys.argv[1]
    while time.time() - start < 2700:
        print(f"run: {n_runs}")
        subprocess.call(["timeout", "500", "python3", "-m", \
                         "experiments.timed.run_algs", f"{method}"])
        n_runs += 1

else:
    print("Usage: python3 time_scripts.py <algorithm>")
    print("Algorithms: random, closest, beamsearch, hillclimber, simulated,\
                                                                 depthfirst")