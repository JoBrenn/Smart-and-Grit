from house import House
from battery import Battery


class Grid:

    def __init__(self, size: int) -> None:
        self.size = size
        # evt: 0 op lege plaats
        self.grid: list[list[House | Battery | int]] = []