import random
import numpy as np
from scipy.signal import convolve2d

class Game:
    def __init__(self, agent, teacher=None):
        self.agent = agent
        self.teacher = teacher
        # initialize the game board
        self.board = [['-' for _ in range(i+1)] for i in range(6)]

    def playerMove(self):
        if self.teacher is not None:
            action = self.teacher.makeMove(self.board)
            self.board[action[0]][action[1]] = 'X'
        else:
            printBoard(self.board)
            while True:
                move = input("Your move! Please select a column and row (format \"col,row\"): ")
                print('\n')
                try:
                    row, col = int(move[0])-1, int(move[2])-1
                    self.board[row][col] = 'X'
                except ValueError:
                    print("INVALID INPUT! Please use the correct format.")
                    continue
                break

    def agentMove(self, action):
        self.board[action[0]][action[1]] = 'O'

    def checkForWin(self, key):
        c = 0
        for i in self.board:
            for j in i:
                if j == '-':
                    if c: return False
                    else: c += 1
        return True

    # def checkForDraw(self):
    #     draw = True
    #     for row in self.board:
    #         for elt in row:
    #             if elt == '-':
    #                 draw = False
    #     return draw

    def checkForEnd(self, key):
        if self.checkForWin(key):
            if self.teacher is None:
                printBoard(self.board)
                if key == 'X':
                    print("Player wins!")
                else:
                    print("RL agent wins!")
            return 1
        # elif self.checkForDraw():
        #     if self.teacher is None:
        #         printBoard(self.board)
        #         print("It's a draw!")
        #     return 0
        return -1

    def playGame(self, player_first):
        # Initialize the agent's state and action
        if player_first:
            self.playerMove()
        prev_state = getStateKey(self.board)
        prev_action = self.agent.get_action(prev_state, self.board)
        # iterate until game is over
        while True:
            # execute oldAction, observe reward and state
            self.agentMove(prev_action)
            check = self.checkForEnd('O')
            if not check == -1:
                # game is over. +1 reward if win, 0 if draw
                reward = check
                break
            self.playerMove()
            check = self.checkForEnd('X')
            if not check == -1:
                # game is over. -1 reward if lose, 0 if draw
                reward = -1*check
                break
            else:
                # game continues. 0 reward
                reward = 0
            new_state = getStateKey(self.board)

            # determine new action (epsilon-greedy)
            new_action = self.agent.get_action(new_state, self.board)
            # update Q-values
            self.agent.update(prev_state, new_state, prev_action, new_action, reward, self.board)
            # reset "previous" values
            prev_state = new_state
            prev_action = new_action
            # append reward

        # Game over. Perform final update
        self.agent.update(prev_state, None, prev_action, None, reward, self.board)

    def start(self):
        if self.teacher is not None:
            # During teaching, chose who goes first randomly with equal probability
            if random.random() < 0.5:
                self.playGame(player_first=False)
            else:
                self.playGame(player_first=True)
        else:
            while True:
                # response = input("Would you like to go first? [y/n]: ")
                response = 'y'
                print('')
                if response == 'n' or response == 'no':
                    self.playGame(player_first=False)
                    break
                elif response == 'y' or response == 'yes':
                    self.playGame(player_first=True)
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

def printBoard(board):
    print('    1   2   3   4   5   6 \n')
    for i, row in enumerate(board):
        print(end = f' {i+1}  {"  "*(5-i)}')
        for elt in row:
            print(f'{elt}   ', end='')
        print('\n')

def getStateKey(board):
    key = ''
    for row in board:
        for elt in row:
            key += elt
    return key
