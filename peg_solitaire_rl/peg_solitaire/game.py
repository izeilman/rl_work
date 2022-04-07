import random
import numpy as np
from .teacher import possible_actions

class Game:
    def __init__(self, agent, teacher=None):
        self.agent = agent
        self.teacher = teacher
        self.board = [['O' for _ in range(i+1)] for i in range(6)]
        self.board[0][0] = '-'

    def playerMove(self):
        printBoard(self.board)
        while True:
            move = input("Your move! Please select a column and row (format \"col,row\"): ")
            print('\n')
            try:
                row, col = int(move[0])-1, int(move[2])-1
                if self.board[row][col] != '-': raise ValueError
                self.board[row][col] = 'O'
            except ValueError:
                print("INVALID INPUT!")
                continue
            break

    def agentMove(self, action):
        self.board[action[0][0]][action[0][1]] = 'O'
        self.board[action[1][0]][action[1][1]] = '-'
        self.board[action[2][0]][action[2][1]] = '-'

    def checkForEnd(self):
        if len(possible_actions(self.board)) == 0:
            return True
        c = 0
        for i in self.board:
            for j in i:
                if j == 'O':
                    if c: return False
                    else: c += 1
        return True


    def playGame(self, player):
        # Initialize the agent's state and action
        if player:
            while True:
                self.playerMove()
        else:
            prev_state = getStateKey(self.board)
            prev_action = self.agent.get_action(prev_state, self.board)
            # iterate until game is over
            while True:
                # execute oldAction, observe reward and state
                self.agentMove(prev_action)
                if self.checkForEnd():
                    reward = 1
                    printBoard(self.board)
                    break
                else:
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
                printBoard(self.board)

            # Game over. Perform final update
            self.agent.update(prev_state, None, prev_action, None, reward, self.board)

    def start(self):
        if self.teacher is not None:
            self.playGame(player=False)
        else:
            while True:
                # response = input("Would you like to play a game? [y/n]: ")
                response = 'n'
                response = response.lower()
                print('')
                if response == 'n' or response == 'no':
                    self.playGame(player=False)
                    break
                elif response == 'y' or response == 'yes':
                    self.playGame(player=True)
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
