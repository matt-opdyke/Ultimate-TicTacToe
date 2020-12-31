import random
import numpy as np

class InnerBoard():
    def __init__(self, id_index):
        self.state = [['_']*3] * 3
        self.innerID = id_index

    def place_marker(self, marker, x, y):
        """ Updates the InnerBoard object to reflect the new move and returns 
        the InnerBoard object index where the next player must move

        Parameters:
            marker: The marker to place
            loc: The location that the given marker must be placed
        """
        self.state = self.state[x][y]

    def print_inner(self):
        """ Visualization of the InnerBoard object
        """
        print(self.state)

