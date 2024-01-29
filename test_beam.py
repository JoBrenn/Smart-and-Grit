from code.algorithms.beam_search import BeamSearch
from code.modules.district import District
import json

district = District(1, "costs-own")

beam = 5
beam_search = BeamSearch(district, beam)

states = beam_search.run()

data = states[0].return_output()

with open(f"output/JSON/BeamSearch{beam}.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
