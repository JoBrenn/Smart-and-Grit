""" Beam Search algorithm script.

File: beamsearch_script.py

Authors:    Jonas Brenninkmeijer

Date: 26/01/24 (29/01/24)

Description:    BeamSearchTuning object to enable to running on
                different 'beams' multiple times

Usage:  python3 beamsearch_script.py [district] [runs] [maximum beam]
"""

from code.algorithms.beam_search import BeamSearch
from code.modules.district import District
from random import seed
from json import dump
from time import time
import csv
import pickle
import os
import sys


class BeamSearchTuning:

    def __init__(self, district_number: int, runs: int, max_beam: int) -> None:
        """ Initialize beamsearch tuning
        Params:
            district_number    (int): district number
            runs               (int): number of runs 
            max_beam           (int): maximum beam width
        Returns:
            none
        """

        self.district_number = district_number
        self.district = District(district_number, "costs-own")
        self.runs = runs
        self.max_beam = max_beam
        self.file_name = f"District{self.district_number}-Runs{self.runs}-MaxBeam{self.max_beam}"

        self.outcomes = dict.fromkeys(range(1, max_beam + 1), None)
        self.best_states = dict.fromkeys(range(1, max_beam + 1), None)

        self.start_beam = 1
        self.start_runs_at = 0

        self.check_pickled()

    def check_pickled(self) -> bool:
        file_path_outcomes = f'output/pickle/{self.file_name}-outcomes.pkl'
        file_path_best_states = f'output/pickle/{self.file_name}-best_states.pkl'
        if os.path.isfile(file_path_outcomes) and os.path.isfile(file_path_best_states):
            print("Loaded pickled files")
            with open(file_path_outcomes, "rb") as infile:
                self.outcomes = pickle.load(infile)
            with open(file_path_best_states, "rb") as infile:
                self.best_states = pickle.load(infile)
            self.set_start()
            return True
        return False

    def set_start(self):
        if self.outcomes:
            self.start_beam = max([beam for beam in self.outcomes if self.outcomes[beam]])
            self.start_runs_at = len(self.outcomes[self.start_beam])

    def create_pickle(self):
        with open(f'output/pickle/{self.file_name}-outcomes.pkl', 'wb') as outfile:
            pickle.dump(self.outcomes, outfile)
        with open(f'output/pickle/{self.file_name}-best_states.pkl', 'wb') as outfile:
            pickle.dump(self.best_states, outfile)

    def create_csv(self):
        with open(f"output/csv/{self.file_name}.csv", "w", newline="") as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(["beam","time","valid-runs","costs"])

    def add_to_csv(self, beam: int, time: int):
        with open(f"output/csv/{self.file_name}.csv", "a", newline="") as outfile:
            writer = csv.writer(outfile, delimiter=',')
            valid_outcomes = self.count_valid_outcomes(self.outcomes[beam])
            writer.writerow([beam, time, valid_outcomes, self.outcomes[beam]])

    def create_JSON(self):
        with open(f"output/JSON/{self.file_name}.json", "w") as outfile:
            dump(self.best_states, outfile, indent=4)

    def count_valid_outcomes(self, outcomes: list[int]) -> int:
        return len(outcomes) - outcomes.count(0)

    def calculate_state_cost(self, state):
        return state.return_cost() if state else 0

    def add_to_outcomes(self, beam: int, cost: int) -> None:
        if self.outcomes[beam]:
            self.outcomes[beam].append(cost)
        else:
            self.outcomes[beam] = [cost]

    def select_best_state(self, beam: int, state: District, cost: int):
        if cost and cost == max(self.outcomes[beam]):
            self.best_states[beam] = state.return_output()

    def run_tuning(self):
        try:
            print("Start tuning.")
            if not self.check_pickled():
                self.create_csv()
            for beam in range(self.start_beam, self.max_beam + 1):
                start_time = time()
                print("\nBeam:", beam)
                for i in range(self.start_runs_at, self.runs):
                    seed(i)
                    beamsearch = BeamSearch(self.district, beam)
                    output = beamsearch.run(i)
                    output_cost = self.calculate_state_cost(output)
                    self.add_to_outcomes(beam, output_cost)
                    self.select_best_state(beam, output, output_cost)
                    self.start_runs_at = 0
                end_time = time()
                elapsed_time = round(end_time - start_time, 2)
                print(f"\nBeam took {elapsed_time}s.")
                self.add_to_csv(beam, elapsed_time)
            self.create_JSON()
            print(self.outcomes)
            return True
        except:
            self.create_pickle()
            return False


if __name__ == "__main__":
    beamsearch_tuning = BeamSearchTuning(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    if beamsearch_tuning.run_tuning():
        print("Success.")
    else:
        print("Failed.")
