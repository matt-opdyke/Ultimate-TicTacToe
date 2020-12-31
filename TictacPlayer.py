import random


class TictacPlayer:
    board = [[0] * 9] * 9
    markers = ['X', 'O']

    def __init__(self):
        """ Initializes the TictacPlayer object with either 'X' or 'O' randomly
        """
        self.my_marker = random.choice(self.markers)
        self.op_marker = self.markers[0] if self.my_marker == self.markers[1] else self.markers[1]

    def heuristic(self, state):
        """ A function to calculate the current game heuristic value of the given state
        """
        pass

    def succ(self, state):
        """ A function used to find all successor states of the current state
        """
        pass

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

    def board_validation(self, state):
        """ Checks to see if the current state is terminal
        """
        pass
