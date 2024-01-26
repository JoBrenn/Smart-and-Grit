from code.algorithms.depth_first import DepthFirst

class BreadthFirst(DepthFirst):
    def __init__(self, district, depth):
        super().__init__(district, depth)

    def return_next_state(self):
        return self.stack.pop(0)