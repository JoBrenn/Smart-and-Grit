from code.algorithms.beam_search import BeamSearch
from code.modules.district import District


district = District(1, "costs-own")

beam_search = BeamSearch(district, 100)

beam_search.run()
