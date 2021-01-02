import random
import numpy as np

class InnerBoard():
    def __init__(self, id_index):
        self.state = np.array(['_']*9)
        self.state = np.reshape(self.state, (3,3))
        self.innerID = id_index
        self.winner = None

    def place_marker(self, marker, x, y):
        """ Updates the InnerBoard object to reflect the new move and returns 
        the InnerBoard object index where the next player must move

        Args:
            marker: The marker to place
            loc: The location that the given marker must be placed
        """
        self.state[x][y] = marker

    def print_inner(self):
        """ Visualization of the InnerBoard object
        """
        print(self.state)
    
    def set_state(self, state):
        """ USED FOR TESTING PURPOSES"""
        self.state = state

    def validate(self):
        """ Assesses the current state to see if it is terminal.

        This function assures determines whether the current configuration of 
        the InnerBoard state is terminal or not. If it is terminal, then the
        'conditions' attribute of the TictacPlayer class will be updated in the 
        corresponding square.

        Return:
            True if the current InnerBoard configuration is a terminal state. 
            There are 8 possible terminal configurations for the AI player. 
            Three horizontal lines, three vertical lines and two diagonal 
            conditions exist.
        """
        # vertical condition
        i = 0
        while i < 3:
            #print(row[0][0],row[1][0],row[2][0])
            if self.state[0][i] == self.state[1][i] == self.state[2][i] and str(self.state[0][i]) != '_':
                self.winner = self.state[0][i]
                return True
            i += 1
        
        # horizontal condition
        i = 0
        while i < 3:
            if self.state[i][0] == self.state[i][1] == self.state[i][2] and str(self.state[i][0]) != '_':
                self.winner = self.state[i][0]
                return True
            i += 1
        
        # diagonal (TL to BR) condition
        if self.state[0][0] == self.state[1][1] == self.state[2][2] and str(self.state[0][0]) != '_':
            self.winner = self.state[0][0]
            return True

        # diagonal (TR to BL) condition
        if self.state[0][2] == self.state[1][1] == self.state[2][0] and str(self.state[0][2]) != '_':
            self.winner = self.state[0][2]
            return True

        for row in self.state:
            if '_' in row:
                return False
        
        # If validation reaches this point, then there must be a tie in this 
        # InnerBoard. We will return True for terminal state, but set the 
        # winner attribute to 'T' for tie
        self.winner = 'T'
        return True

def main ():
    i1 = InnerBoard(0)
    i2 = InnerBoard(0)
    i3 = InnerBoard(0)
    i1.set_state(np.reshape(np.array(['X','_','_','X','_','_','X','_','_']), (3,3)))
    i2.set_state(np.reshape(np.array(['X','_','_','_','X','_','_','_','X']), (3,3)))
    i3.set_state(np.reshape(np.array(['X','_','_','_','_','_','X','_','_']), (3,3)))
    i1.print_inner()
    print(i1.validate(), i1.winner)
    i2.print_inner()
    print(i2.validate(), i2.winner)
    i3.print_inner()
    print(i3.validate(), i3.winner)

main()