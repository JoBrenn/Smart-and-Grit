# Smart-and-Grit
Nowadays, lots of houses contribute to their own energy consumption via solar panels or other installations. More often than not, these installations produce more energy than needed for own consumption. However, the current infrastructure does not hold into account these surplusses. In able to store these surplusses, batteries need to be placed along the grid.\
The goal is to find the best cable configuration for three given districts. Where the location of the batteries, the location of the houses and their outputs are given.\
In order to do this, there are a couple of requirements, namely:
- No battery can be connected to another battery, also not via a house.
- No house can be connected to two batteries.
- There can be multiple cables along a grid segments. However, they are considered different cables. 
- At first, all houses must have their own cable to a battery (indicated by 'costs-own'). A shared cables configuration is indicated by 'costs-shared'.

## Objective Function
SmartGrid is a minimalisation problem. The amount of cable segments needs to be minimised. The amount of batteries is given. 
The costs of the different aspects are as follows:
- Battery (B): 5000
- Cable (C): 9

The Objective Function of this problem, and thus the costs of a district configuration, can be stated as:

    Z = B * 5000 + C * 9


# Usage

## Requirements

All code has been written in Python 3.10.12.

All needed requirements can be installed by running: 

        pip install -r requirements.txt
## Run
Running of: python3 main.py gives the following option screen:

<img src="images/main_screen.png" width="400">


Where typing 'help' in the method option gives a description of the possible methods.

Typing 'combine' in the method option shows a list of output files. Selecting one of these
indices runs the combine_cables algorithm on said output file. This creates a 'costs-shared'
 configuration from the selected 'costs-own' configuration.
 
<img src="images/combine.png" width="400">


## Structure
Here the most imported directories are stated:
- /code: constains all code (.py files)
    - /algorithms: contains all algorithms
    - /helpers: contains all helpers
    - /modules: contains all classes
    - /visualisation: contains all code concerning the visualisations
- /experiments: contains all code for the experiments
    - /hillclimber: contains hillclimber experiment script
    - /simulatedannealing: contains simulatedannealing experiment script
    - /beamsearch: contains beamsearch experiment script
    - /times: contains all timed experiment scripts 
        - results_timed.md: contains the results of the timed experiment for all algorithms
- /results: contains all found results

## Experiment
In /experiments/, tuning experiments can be conducted by running the script functions in /simulatedannealing/, /beamsearch/ and /hillclimber/.

### Simulated Annealing
The file simulatedannealing_experiment contains multiple functions.\
Where in the function simulannealing_temp_comparison different temperatures are compared.
This comparison can then be visualized via either the function simulannealing_temp_comparison_mean_graph() or 
simulannealing_temp_comparison_lowest_graph. Where the mean cost and the lowest cost are compared respectively.

### Beam search
The file beamsearschscript.py contains a BeamSearchTuning class. 
After creating an instance of this class by specifying the district number, \
the amount of runs and the largest allowed beam. The run_tuning() method can be executed \
after which the results will be written to a csv and the best result will be stored as a .json file

### Timed experiment
The file time_scripts.py contains a script to run different algorithms for a certain amount of time. 
In this script, the algorithm will be run continuously for 2700 seconds. The costs of each state will be written to a csv file in the /output/ folder and the amount of runs will be printed in the terminal window.
This file can be used to compare the different algorithms. However, this timed experiment can be called via python3 main.py, by
indicating 'experiments' as method and then 'timed'. This being able to run it via main has however made the elements 
within time_scripts.py slower. The results in results_timed.md have therefore been run straight from the root for optimal
comparison.

A timed experiment can be ran by using:

        python3 time_scripts.py <method>

where the method can be one of closest, beamsearch, hillclimber, simulated or depthfirst

## Tests
To run tests, run the following code:

        python3 -m pytest code/<directory>/

Specify the directory to be tested. The following directories contain tests:
- /code (always to be specified)
    - /algorithms
    - /modules

Example:

        python3 -m pytest code/modules/

# Authors
- Jonas Brenninkmeijer (JoBrenn)
- Kathy Molenaar (kathymolenaar)
- Jesper Vreugde (JesVre)
