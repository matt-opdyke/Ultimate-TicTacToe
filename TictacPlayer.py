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
        winner: Which player has won the larger board.
    """
    board = []
    markers = ['X', 'O']

    def __init__(self):
        """Initializes the TictacPlayer object.

        Creates the TictacPlayer object with either 'X' or 'O' randomly and
        shapes the board into a 3x3 numpy array of InnerBoard objects.
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

        self.first = False

    def condition_heuristic(self):
        """ Calculates the heuristic of the conditional board.

        This function will calculate the heuristic of the larger board. This is used within the heuristic function and weighted differently than the heuristic of an InnerBoard state.

        Return:
            The game heuristic value of the condition board.
        """
        return self.condition.inner_heuristic(self.my_marker, self.op_marker)

    def heuristic(self, state=board):
        """Calculates the game heuristic value of the given state.

        This function will calculate the game heuristic value of the current 
        state that will later be used in determining the ideal move for the AI
        player. This calculation will be used within the Minimax algorithm when
        assessing states.

        Args:
            state: The state to which the heuristic is calculated.

        Return:
            The game heuristic value of the specified state.
        """
        score = 0
        if self.board_validation():
            return float('inf')
        for row in state:
            for inner in row:
                score += inner.inner_heuristic(self.my_marker, self.op_marker)

        score += self.condition_heuristic() * 2

        return score

    def calculate_pos(self, num):
        """ Calculates the position in a board based on ID.

        A helper function to calculate the indices of a space within a board
        (InnerBoard or larger board) to be used when accessing/placing markers.

        Args:
            num: The given ID to be converted into indices.

        Return:
            The x and y coordinates of the specified ID.
        """
        x = num // 3
        y = num % 3
        return x, y

    def succ(self, targetID, state=board):
        """A function used to find all successor states of the current state.

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
        if int(targetID) == -1:
            pass
        else:
            x, y = self.calculate_pos(targetID)
            if not state[x][y].validate():
                return self.inner_succ(x, y)

        x, y, index = 0, 0, 0
        while index < 9:
            x, y = self.calculate_pos(index)
            index += 1
            if state[x][y].validate():
                continue
            successors += self.inner_succ(x, y)

        return successors

    def inner_succ(self, x, y):
        """A helper function for the successor function.

        This function serves to calculate successors of the current state with
        the specified InnerBoard.

        Args:
            x: The row of the target InnerBoard.
            y: the column of the specified InnerBoard.

        Return:
            A list of possible successor states within the InnerBoard. Note
            that 9 is the maximum amount of successor states that a single
            InnerBoard may contain.
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
                    successors.append((curr, index))
                index += 1
        return successors

    def max_val(self, state, targetID, depth):
        """The max value function for the Minimax algorithm.

        The maximum value function of the Minimax algorithm. This function is used concurrently with the minimum value function to reach the desired depth of the game tree.

        Args:
            state: The state used in the current iteration of max_val.
            targetID: where the next player must move.
            depth: The desired depth of the game tree.
        
        Return:
            The maximum heuristic found within the game tree.
        """

        # temp variable to hold heuristic for better runtime
        store = self.heuristic(state)

        if store == float('inf') or depth == 0:
            return store

        alpha = float('-inf')

        for successor in self.succ(targetID, state):
            alpha = max(alpha, self.min_val(
                successor[0], successor[1], depth-1))
        return alpha

    def min_val(self, state, targetID, depth):
        """The min value function for the Minimax algorithm.

        The minimum value function of the Minimax algorithm. This function is used concurrently with the maximum value function to reach the desired depth of the game tree.

        Args:
            state: The state used in the current iteration of min_val.
            targetID: where the next player must move.
            depth: The desired depth of the game tree.
        
        Return:
            The minimum heuristic found within the game tree.
        """
        store = self.heuristic(state)

        # if the state is terminal or max depth is reached, return the
        # heuristic of the current state
        if store == float('inf') or depth == 0:
            return store

        # initialize beta to infinity
        beta = float('inf')

        for successor in self.succ(targetID, state):
            beta = min(beta, self.max_val(successor[0], successor[1], depth-1))
        return beta
    
    def first_turn(self):
        """ Helper function for take_turn to randomly select the first turn.

        This function will randomly select a first move for the AI player. 
        Since there is no need to run the minimax algorithm over every single 
        space in the board, a random move will suffice.
        """
        inner = random.choice(range(9))
        space = random.choice(range(9))
        x,y = self.calculate_pos(inner)
        row, col = self.calculate_pos(space)
        self.board[x][y].place_marker(self.my_marker,row, col)
        return inner
    
    def update(self, new):
        """ Helper function for take_turn to update the board state.

        This function will update the current board's state to reflect the move selected by the AI player.

        Args:
            new: The new state that contains the AI player's move.
        """
        for x in range(3):
            for y in range(3):
                self.board[x][y].set_state(new[x][y].state)

    def take_turn(self, inner, depth):
        """Executes the AI's next calculated move.

        In order to take its turn, the AI player will use this function to connect the minimax algorithm and determine which move is the best option based on the heuristic.

        Args:
            inner: The specified InnerBoard where the AI player must move.
            depth: The given depth for the game tree calculations.
        
        Return:
            0: The first turn condition.
            1: Otherwise.
        """
        if self.first == True:
            self.first = False
            self.first_turn()
            return 0

        best_heur = float('-inf')

        best_state = None

        for state in self.succ(inner, self.board):

            if (self.board_validation() == True):
                best_state = state
                break

            current_value = self.min_val(state[0], inner, depth)
            print('current calculated')

            if current_value > best_heur:
                best_heur = current_value
                best_state = state
        #self.print_state(best_state)
        #print(type(self.board), type(best_state))
        self.update(best_state[0])
        return best_state[1]

    def board_validation(self):
        """Checks to see if the current configuration is terminal.

        This function checks the state of the condition attribute and validates it. Since condition is represented by an InnerBoard object, the validate function may be utilized.

        Return:
            True if the board is in a terminal state, otherwise false.
        """
        return self.condition.validate()

    def print_state(self, state=board):
        """Prints the current game state to the console.

        This function visualizes the board state and prints it to the console
        for the human player.

        Args:
            state: specifies which state to print, defaults to current state.
        """
        state = np.reshape(state, (3, 3))
        for row in state:
            top, mid, bot = [], [], []
            for inner in row:
                inner = inner.print_inner(verbose=False)
                top.append(list(inner[0]))
                mid.append(list(inner[1]))
                bot.append(list(inner[2]))
            print(top, mid, bot, sep='\n')
            print()

    def prompt_input(self, targetInner):
        """Facilitates retrieving the user input.

        This function will take the user input in the form of two integers and
        parse it into a two element list. It also assures that the input is
        valid. Upon invalid input, prints an error message and prompts for new
        input.

        Return:
            A two element list holding 0) the specified InnerBoard and 1) the
            specified space within the given InnerBoard.

        Raises:
            ValueError: A ValueError was thrown as the input is invalid.
        """
        move = input("Please enter your move: ")
        try:
            ret = [int(move[0]), int(move[1])]
            if ret[0] != targetInner and targetInner != -1:
                print('That is not the correct inner board! Try again.')
                self.prompt_input(targetInner)
            x,y = self.calculate_pos(ret[0])
            row,col=self.calculate_pos(ret[1])
            if self.board[x][y].state[row][col] != '_':
                print('That space is already occupied! Try again.')
                self.prompt_input(targetInner)
            return ret
        except ValueError:
            print(
                "ERROR: invalid usage. Please enter your input as {int}{int}")
            self.prompt_input(targetInner)

    def op_move(self, targetInner):
        """Allows the human opponent to select their move.

        Facilitates the prompting for user input, parsing the input into
        coordinates then placing the correct marker.

        Return:
            The InnerBoard where the AI player must move next turn.
        """
        self.print_state()
        move = self.prompt_input(targetInner)
        inner_select = move[0]
        x, y = self.calculate_pos(inner_select)
        space_select = move[1]
        row, col = self.calculate_pos(space_select)
        self.board[x][y].place_marker(self.op_marker, row, col)
        return targetInner

    def start_game(self):
        """The driver method for the class.

        The application will begin by randomly selecting which player goes
        first, and alternating turns from then onward.
        """
        depth = 2
        player = random.choice([0, 1])
        inner = -1
        if player == 0:
            inner = self.first_turn()
            self.first == True
            player = 1
        while self.winner == None:
            if player == 0:
                inner = self.take_turn(inner, depth)
                player = 1
            elif player == 1:
                inner = self.op_move(inner)
                player = 0


def main():
    ttp = TictacPlayer()
    ttp.start_game()


main()
