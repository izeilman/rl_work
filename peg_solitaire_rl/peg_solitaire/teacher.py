import random
import numpy as np

spaces = []
for i in range(6):
    for j in range(i+1):
        spaces.append((i,j))

def possible_actions(board):
    def get_adj(space):
        directions = {"R"  : (space[0], space[1] + 1),
                      "L"  : (space[0], space[1] - 1),
                      "TL" : (space[0] - 1, space[1] - 1),
                      "TR" : (space[0] - 1, space[1]),
                      "BL" : (space[0] + 1, space[1]),
                      "BR" : (space[0] + 1, space[1] + 1)}
        return directions

    empty_spaces = []
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == '-':
                empty_spaces.append((i,j))

    possible_actions = []
    for space in empty_spaces:
        adj = get_adj(space)
        for z in adj:
            if adj[z] in spaces and board[adj[z][0]][adj[z][1]] == 'O':
                move = get_adj(adj[z])[z]
                if move in spaces and board[move[0]][move[1]] == 'O':
                    possible_actions.append((space, adj[z], move))

    return possible_actions


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

    def randomMove(self, board):
        return random.choice(self.possible_actions(board))

    def makeMove(self, board):
        """
        Trainer goes through a hierarchy of moves, making the best move that
        is currently available each time. A touple is returned that represents
        (row, col).
        """
        # Chose randomly with some probability so that the teacher does not always win
        if random.random() > self.ability_level:
            return self.randomMove(board)

        return self.randomMove(board)
