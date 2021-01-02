import random
import numpy as np
import copy
from InnerBoard import *


class TictacPlayer:
    """This class implements the AI player for the Ultimate Tic-Tac-Toe game.

    Within this class, the Artificial Intelligence player for the game is 
    created. This player utilizes a Minimax Algorithm to assess which move is 
    most appropriate for execution.

    Attributes:
        my_marker: The AI's marker as a string representation of 'X' or 'O'.
        op_marker: The AI's opponent's marker represented in the same manner.
        board: The board represented as a 3x3 numpy array of InnerBoard objects.
        condition: The state of the larger board in terms of a smaller game
    """
    board = []
    markers = ['X', 'O']

    def __init__(self):
        """ Initializes the TictacPlayer object with either 'X' or 'O' randomly 
        and shapes the board into a 3x3 numpy array of InnerBoard objects.
        """
        self.my_marker = random.choice(self.markers)
        if self.my_marker == self.markers[1]:
            self.op_marker = self.markers[0]
        else:
            self.op_marker = self.markers[1]

        i = 0
        while i < 9:
            self.board.append(InnerBoard(i))
            i += 1
        
        self.board = np.array(self.board)
        self.board = np.reshape(self.board, (3, 3))

        self.condition = InnerBoard(-1)


    def heuristic(self, state):
        """ A function to calculate the current game heuristic value of the 
        given state
        """
        pass

    def succ(self, state, targetID):
        """ A function used to find all successor states of the current state.

        This function will be used by the Minimax Algorithm to calculate 
        possible moves and assess them to select the best possible move. 
        Assessment will be conducted by the heuristic function.

        Args:
            state: The current state to which we are calculating successors
            targetID: The InnerBoard object's ID where the AI must make a move

        Return:
            A list of the valid successor states with respect to the argument 
            'state'. Note that there are at most 9 successor states because the 
            AI may only place a piece in one of the InnerBoard objects, which 
            only contains 9 possible spaces.
        """
        successors = []

        # Calculate the row and column of the InnerBoard where the AI must move 
        # based on it's targetID
        x = targetID // 3
        y = targetID % 3

        index = 0
        for i in state[x][y].state:
            for j in i:
                if str(j) not in self.markers:
                    curr = copy.deepcopy(state)
                    row = index // 3
                    col = index % 3
                    curr[x][y].place_marker(self.my_marker, row, col)
                    successors.append(curr)
                index += 1
        return successors

    def max_val(self, state):
        """ The max value function for the Minimax algorithm
        """
        pass

    def min_val(self, state):
        """ The min value function for the Minimax algorithm 
        """
        pass

    def take_turn(self, states):
        """ Executes the AI's next calculated move
        """
        pass

    def board_validation(self):
        """ Checks to see if the current configuration is terminal
        """
        return self.condition.validate()


    def print_state(self, state=board):
        state = np.reshape(state, (3, 3))
        for row in state:
            for inner in row:
                inner.print_inner()


def mainTictacPlayer():
    ttp = TictacPlayer()
    successors = ttp.succ(ttp.board, 4)
    successors[0][1][1].print_inner()
    print()
    ttp.print_state(successors[0])
    #print(ttp.succ.__doc__)


#mainTictacPlayer()
