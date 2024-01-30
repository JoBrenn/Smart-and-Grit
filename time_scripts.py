import subprocess
import time

start = time.time()
n_runs = 0

while time.time() - start < 2700:
    print(f"run: {n_runs}")
    subprocess.call(["timeout", "500", "python3", "run_algs.py"])
    n_runs += 1