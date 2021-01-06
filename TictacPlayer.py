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

        self.winner = None

    def heuristic(self, state=board):
        """ Calculates the game heuristic value of the given state.

        This function will calculate the game heuristic value of the current state that will later be used in determining the ideal move for the AI 
        player. This calculation will be used within the Minimax algorithm when 
        assessing states.

        Args:
            state: The state to which the heuristic is calculated.

        Return:
            The game heuristic value of the specified state.
        """
        if self.board_validation():
            return float('inf')

    def calculate_pos(self, num):
        x = num // 3
        y = num % 3
        return x, y

    def succ(self, targetID, stateboard):
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
        x, y = self.calculate_pos(targetID)

        if not self.board[x][y].validate():
            return self.inner_succ(x, y)

        x, y, index = 0, 0, 0
        while index < 9:
            x, y = self.calculate_pos(targetID)
            index += 1
            if self.board[x][y].validate():
                continue
            successors += self.inner_succ(x, y)

        return successors

    def inner_succ(self, x, y):
        """ A helper function for the successor function.
        """
        successors = []
        index = 0
        for i in self.board[x][y].state:
            for j in i:
                if str(j) not in self.markers:
                    curr = copy.deepcopy(self.board)
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

    def take_turn(self):
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
            top, mid, bot = [], [], []
            for inner in row:
                inner = inner.print_inner(verbose=False)
                top += list(inner[0])
                mid += list(inner[1])
                bot += list(inner[2])
            print(top, mid, bot, sep='\n')

    def prompt_input(self):
        move = input("Please enter your move: ")
        try:
            return [int(move[0]), int(move[1])]
        except ValueError:
            print(
                "ERROR: invalid usage. Please enter your input as {int}{int}")
            self.prompt_input()

    def op_move(self):
        self.print_state()
        move = self.prompt_input()
        targetInner = move[0]
        x, y = self.calculate_pos(targetInner)
        targetSpace = move[1]
        row, col = self.calculate_pos(targetSpace)
        self.board[x][y].place_marker(self.op_marker, row, col)
        self.print_state()
    
    def start_game(self):
        player = random.choice([0,1])
        while self.winner == None:
            if player == 0:
                self.take_turn()
            elif player == 1:
                self.op_move()



def main():
    ttp = TictacPlayer()
    ttp.op_move()


main()
