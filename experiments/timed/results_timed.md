# Results

The following results were collected by running each algorithm repeatedly for 2700 seconds.

The full CSV's containing the state costs of each run are located at: /experiments/timed/results/

Note: these results were all obtained by running time_scripts.py from the root, and not thorugh main.py
Doing so via the latter method would result in noticable performance loss, and so fewer runs would be performed.

| algorithm           | runs     | solutions | lowest costs |
| -----------------:  | :------: | :-------: | :----------: |
| Closest             | 10189    | 10189     | 57742        |
| BeamSearch (Beam 5) | 64       | 31        | 58885        |
| HillClimber         | 12       | 12        | 57049        |
| SimulatedAnnealing  | 6        | 6         | 64762        |
