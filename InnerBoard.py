import random
import numpy as np


class InnerBoard():
    """This class creates the InnerBoard object.

    This class implements the InnerBoard object and a few methods for
    functionality, such as for placing markers and terminal state validation.
    The larger game board is comprised of nine InnerBoard objects in a 3x3
    numPy array.

    Attributes:
        state: The current game state of the InnerBoard.
        innerID: The index of the InnerBoard within the larger board.
        winner: String representation of which player won the InnerBoard,
          'T' if the result is a tie
    """

    def __init__(self, id_index):
        """Initializes the InnerBoard object.

        Creates the InnerBoard object as a 3x3 numPy array with the specified 
        ID for the InnerBoard. The default for winner is None as no one has won 
        an empty InnerBoard.
        """
        self.state = np.array(['_']*9)
        self.state = np.reshape(self.state, (3, 3))
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

    def print_inner(self, verbose=True):
        """ Visualization of the InnerBoard object

        This method will either print the InnerBoard object to console, or return the state depending on the value of verbose.

        Args:
            verbose: Determines if the state will be printed or returned.

        Return:
            The InnerBoard object's state if verbose is set to False.
        """
        if verbose == False:
            return self.state
        print(self.state)

    def set_state(self, state):
        """ USED FOR TESTING PURPOSES"""
        self.state = state

    def inner_heuristic(self, my_mark, op_mark):
        """Calculates the heuristic of the InnerBoard.

        This function serves to calculate the heuristic on a smaller scale for
        the InnerBoard. This smaller heuristic will be compounded with the
        heuristic of the other InnerBoards to calculate the heuristic of the
        larger game board.

        Return:
            The heuristic of this InnerBoard.
        """
        # TODO implement heuristic func for InnerBoard

        score = 0

        # vertical condition
        i = 0
        vert_flip = np.transpose(self.state)
        while i < 3:
            unique, counts = np.unique(vert_flip[i], return_counts=True)
            count = dict(zip(unique, counts))
            if my_mark in count and op_mark not in count:
                if count[my_mark] == 1:
                    score += 10
                elif count[my_mark] == 2:
                    score += 100
                elif count[my_mark] == 3:
                    score += 1000
            i += 1

        # horizontal condition
        i = 0
        while i < 3:
            unique, counts = np.unique(self.state[i], return_counts=True)
            count = dict(zip(unique, counts))
            if my_mark in count and op_mark not in count:
                if count[my_mark] == 1:
                    score += 10
                elif count[my_mark] == 2:
                    score += 100
                elif count[my_mark] == 3:
                    score += 1000
            i += 1

        # diagonal (TL to BR) condition
        tlbr = [self.state[0][0], self.state[1][1], self.state[2][2]]
        unique, counts = np.unique(tlbr, return_counts=True)
        count = dict(zip(unique, counts))
        if my_mark in count and op_mark not in count:
            if count[my_mark] == 1:
                score += 10
            elif count[my_mark] == 2:
                score += 100
            elif count[my_mark] == 3:
                score += 1000

        # diagonal (TR to BL) condition
        trbl = [self.state[0][2], self.state[1][1], self.state[2][0]]
        unique, counts = np.unique(trbl, return_counts=True)
        count = dict(zip(unique, counts))
        if my_mark in count and op_mark not in count:
            if count[my_mark] == 1:
                score += 10
            elif count[my_mark] == 2:
                score += 100
            elif count[my_mark] == 3:
                score += 1000
        
        return score

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
            conditions exist. Additionally, if the InnerBoard is full (meaning 
            all 9 spaces are occupied by a marker) and there is no winning 
            line, then the winner attribute is set to 'T' for tie.
        """
        # vertical condition
        i = 0
        while i < 3:
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
