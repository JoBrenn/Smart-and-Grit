""" Breadth first algorithm. Subclass of the ClosestFirst class

File: breadth_first.py

Author:    Jesper Vreugde

Date: 26/01/24

Description:    This subclass inherits its properties from the DepthFirst class
                Instead of the next state being chosen from a stack, it is 
                picked from a queue

Usage:  from code.algorithms.breadth_first import BreadthFirst
"""

from code.algorithms.depth_first import DepthFirst
from code.modules.district import District

class BreadthFirst(DepthFirst):
    """ BreadthFirst algorithm classes
        Subclass of DepthFirst

    Methods:            
        return_next_state()         returns the next item in the queue
    """
    def __init__(self, district, depth) -> None:
        """ Initializes the BreadthFirst class
            Params:
                district    (District): Distrisct object
                depth       (int): Tha maximum depth that the Depth search tree
                            will be. Set at the max as default
            Returns
                None
        """
        
        super().__init__(district, depth)

    def return_next_state(self) -> District:
        """ Returns the next element of the queue
            Returns:
                District object removed from the beginning of the states list
        """
        return self.states.pop(0)