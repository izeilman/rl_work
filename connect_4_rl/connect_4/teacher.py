import random
import numpy as np
from scipy.signal import convolve2d

class Teacher:
    """
    A class to implement a teacher that knows the optimal playing strategy.
    Teacher returns the best move at any time given the current state of the game.
    Note: things are a bit more hard-coded here, as this was not the main focus of
    the exercise so I did not spend as much time on design/style. Everything works
    properly when tested.

    Parameters
    ----------
    level : float
        teacher ability level. This is a value between 0-1 that indicates the
        probability of making the optimal move at any given time.
    """

    def __init__(self, level=0.9):
        """
        Ability level determines the probability that the teacher will follow
        the optimal strategy as opposed to choosing a random available move.
        """
        self.ability_level = level

    def win(self, b, key='X'):
        """ If we have two in a row and the 3rd is available, take it. """
        # Check for diagonal wins
        board = np.zeros(shape=(6,7))
        for i in range(6):
            for j in range(7):
                board[i][j] = int(b[i][j] == key)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        horizontal_kernel = np.array([[ 1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
        for kernel in detection_kernels:
            if (convolve2d(board, kernel, mode="valid") == 4).any():
                return True


        # a = [board[0][0], board[1][1], board[2][2]]
        # b = [board[0][2], board[1][1], board[2][0]]
        # if a.count('-') == 1 and a.count(key) == 2:
        #     ind = a.index('-')
        #     return ind, ind
        # elif b.count('-') == 1 and b.count(key) == 2:
        #     ind = b.index('-')
        #     if ind == 0:
        #         return 0, 2
        #     elif ind == 1:
        #         return 1, 1
        #     else:
        #         return 2, 0
        # # Now check for 2 in a row/column + empty 3rd
        # for i in range(3):
        #     c = [board[0][i], board[1][i], board[2][i]]
        #     d = [board[i][0], board[i][1], board[i][2]]
        #     if c.count('-') == 1 and c.count(key) == 2:
        #         ind = c.index('-')
        #         return ind, i
        #     elif d.count('-') == 1 and d.count(key) == 2:
        #         ind = d.index('-')
        #         return i, ind
        # return None

    def blockWin(self, board):
        """ Block the opponent if she has a win available. """
        return self.win(board, key='O')

    # def fork(self, board):
    #     """ Create a fork opportunity such that we have 2 threats to win. """
    #     # Check all adjacent side middles
    #     if board[1][0] == 'X' and board[0][1] == 'X':
    #         if board[0][0] == '-' and board[2][0] == '-' and board[0][2] == '-':
    #             return 0, 0
    #         elif board[1][1] == '-' and board[2][1] == '-' and board[1][2] == '-':
    #             return 1, 1
    #     elif board[1][0] == 'X' and board[2][1] == 'X':
    #         if board[2][0] == '-' and board[0][0] == '-' and board[2][2] == '-':
    #             return 2, 0
    #         elif board[1][1] == '-' and board[0][1] == '-' and board[1][2] == '-':
    #             return 1, 1
    #     elif board[2][1] == 'X' and board[1][2] == 'X':
    #         if board[2][2] == '-' and board[2][0] == '-' and board[0][2] == '-':
    #             return 2, 2
    #         elif board[1][1] == '-' and board[1][0] == '-' and board[0][1] == '-':
    #             return 1, 1
    #     elif board[1][2] == 'X' and board[0][1] == 'X':
    #         if board[0][2] == '-' and board[0][0] == '-' and board[2][2] == '-':
    #             return 0, 2
    #         elif board[1][1] == '-' and board[1][0] == '-' and board[2][1] == '-':
    #             return 1, 1
    #     # Check all cross corners
    #     elif board[0][0] == 'X' and board[2][2] == 'X':
    #         if board[1][0] == '-' and board[2][1] == '-' and board[2][0] == '-':
    #             return 2, 0
    #         elif board[0][1] == '-' and board[1][2] == '-' and board[0][2] == '-':
    #             return 0, 2
    #     elif board[2][0] == 'X' and board[0][2] == 'X':
    #         if board[2][1] == '-' and board[1][2] == '-' and board[2][2] == '-':
    #             return 2, 2
    #         elif board[1][0] == '-' and board[0][1] == '-' and board[0][0] == '-':
    #             return 0, 0
    #     return None

    # def blockFork(self, board):
    #     """ Block the opponents fork if she has one available. """
    #     corners = [board[0][0], board[2][0], board[0][2], board[2][2]]
    #     # Check all adjacent side middles
    #     if board[1][0] == 'O' and board[0][1] == 'O':
    #         if board[0][0] == '-' and board[2][0] == '-' and board[0][2] == '-':
    #             return 0, 0
    #         elif board[1][1] == '-' and board[2][1] == '-' and board[1][2] == '-':
    #             return 1, 1
    #     elif board[1][0] == 'O' and board[2][1] == 'O':
    #         if board[2][0] == '-' and board[0][0] == '-' and board[2][2] == '-':
    #             return 2, 0
    #         elif board[1][1] == '-' and board[0][1] == '-' and board[1][2] == '-':
    #             return 1, 1
    #     elif board[2][1] == 'O' and board[1][2] == 'O':
    #         if board[2][2] == '-' and board[2][0] == '-' and board[0][2] == '-':
    #             return 2, 2
    #         elif board[1][1] == '-' and board[1][0] == '-' and board[0][1] == '-':
    #             return 1, 1
    #     elif board[1][2] == 'O' and board[0][1] == 'O':
    #         if board[0][2] == '-' and board[0][0] == '-' and board[2][2] == '-':
    #             return 0, 2
    #         elif board[1][1] == '-' and board[1][0] == '-' and board[2][1] == '-':
    #             return 1, 1
    #     # Check all cross corners (first check for double fork opp using the corners array)
    #     elif corners.count('-') == 1 and corners.count('O') == 2:
    #         return 1, 2
    #     elif board[0][0] == 'O' and board[2][2] == 'O':
    #         if board[1][0] == '-' and board[2][1] == '-' and board[2][0] == '-':
    #             return 2, 0
    #         elif board[0][1] == '-' and board[1][2] == '-' and board[0][2] == '-':
    #             return 0, 2
    #     elif board[2][0] == 'O' and board[0][2] == 'O':
    #         if board[2][1] == '-' and board[1][2] == '-' and board[2][2] == '-':
    #             return 2, 2
    #         elif board[1][0] == '-' and board[0][1] == '-' and board[0][0] == '-':
    #             return 0, 0
    #     return None
    #
    # def center(self, board):
    #     """ Pick the center if it is available. """
    #     if board[1][1] == '-':
    #         return 1, 1
    #     return None
    #
    # def corner(self, board):
    #     """ Pick a corner move. """
    #     # Pick opposite corner of opponent if available
    #     if board[0][0] == 'O' and board[2][2] == '-':
    #         return 2, 2
    #     elif board[2][0] == 'O' and board[0][2] == '-':
    #         return 0, 2
    #     elif board[0][2] == 'O' and board[2][0] == '-':
    #         return 2, 0
    #     elif board[2][2] == 'O' and board[0][0] == '-':
    #         return 0, 0
    #     # Pick any corner if no opposites are available
    #     elif board[0][0] == '-':
    #         return 0, 0
    #     elif board[2][0] == '-':
    #         return 2, 0
    #     elif board[0][2] == '-':
    #         return 0, 2
    #     elif board[2][2] == '-':
    #         return 2, 2
    #     return None
    #
    # def sideEmpty(self, board):
    #     """ Pick an empty side. """
    #     if board[1][0] == '-':
    #         return 1, 0
    #     elif board[2][1] == '-':
    #         return 2, 1
    #     elif board[1][2] == '-':
    #         return 1, 2
    #     elif board[0][1] == '-':
    #         return 0, 1
    #     return None

    def randomMove(self, board):
        """ Chose a random move from the available options. """
        possible_actions = []
        for j in range(6):
            for i in range(5):
                if board[5-i][6-j] == '-':
                    possible_actions.append((5-i,6-j))
                    break
        # print(possible_actions)
        return random.choice(possible_actions)

    def makeMove(self, board):
        """
        Trainer goes through a hierarchy of moves, making the best move that
        is currently available each time. A touple is returned that represents
        (row, col).
        """
        # Chose randomly with some probability so that the teacher does not always win
        if random.random() > self.ability_level:
            return self.randomMove(board)
        # Follow optimal strategy
        # TODO: add more stratagy
        for a in [self.win(board),
                  self.blockWin(board),
                  # self.fork(board),
                  # self.blockFork(board),
                  # self.center(board),
                  # self.corner(board),
                  # self.sideEmpty(board)
                  ]:
            if a is not None:
                return a
        return self.randomMove(board)
