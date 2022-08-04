import numpy as np
from scipy.signal import convolve2d

def isWin(a, key):
    board = np.zeros(shape=(6,7))
    for i in range(6):
        for j in range(7):
            board[i][j] = int(a[i+j] == key)
    diag1_kernel = np.eye(4, dtype=np.uint8)
    diag2_kernel = np.fliplr(diag1_kernel)
    horizontal_kernel = np.array([[1, 1, 1, 1]])
    vertical_kernel = np.transpose(horizontal_kernel)
    detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
    for kernel in detection_kernels:
        check = convolve2d(board, kernel, mode="valid")
        if (check == 4).any():
            # if (check == 4) for more than 2
            return True

from itertools import permutations
from pickle import load, dump
import os
os.chdir('\\'.join(str(__file__).split("\\")[:-1]))

count = 0

def validBoards(board="-"*21,player=None):
    global count
    count += 1
    if player == None:
        yield board  # count the empty board
        for b in validBoards(board,player="X"): yield b # X goes 1st
        for b in validBoards(board,player="O"): yield b # O goes 1st
        return
    opponent = "XO"[player=="X"]
    for pos,cell in enumerate(board):
        if cell != "-": continue
        played = board[:pos]+player+board[pos+1:] # simulate move
        yield played                              # return the new state
        if count % 1000000 == 0: print(count)
        if isWin(played, player): continue                # stop game upon winning
        for nextBoard in validBoards(played,opponent):
            yield nextBoard # return boards for subsequent moves

distinctBoards = list(validBoards())  # only look at distinct board states
with open("merpk.pkl", "wb") as f:
    dump(distinctBoards, f)
allStates = len(distinctBoards)
print(f"distinctBoards: {allStates}")
# empty = '-'*42
# boards = []
# for i in range(21):
#     boards.append("XO"*(i+1) + empty[:-2*(i+1)])
#     if i != 20:
#         boards.append("XO"*(i+1) + 'X' + empty[:(-2*(i+1)) - 1])
#         boards.append("XO"*(i+1) + 'O' + empty[:(-2*(i+1)) - 1])
# print(boards[0], flush = True)
# new = list(permutations(boards[0]))
# print(new, flush = True)
# invalid = False
# pass_one = []
# for board in boards:
#     new = set(permutations(board))
#     print(new, flush = True)
#     for perm in new:
#         for val, space in enumerate(perm):
#             if space != '-':
#                 c = 0
#                 invalid = False
#                 while val + 7*c < 41:
#                     if perm[val + 7*c] == '-':
#                         invalid = True
#                         break
#                     c += 1
#                 if invalid:
#                     break
#                 else:
#                     pass_one.append(perm)

# empty = '-'*7
# boards = []
# for i in range(3):
#     boards.append("XO"*(i+1) + empty[:-2*(i+1)])
#     if i != 3:
#         boards.append("XO"*(i+1) + 'X' + empty[:(-2*(i+1)) - 1])
#         boards.append("XO"*(i+1) + 'O' + empty[:(-2*(i+1)) - 1])
# print(set(list(permutations(boards[0]))))
from pickle import dump, load
import os
os.chdir('\\'.join(str(__file__).split("\\")[:-1]))

def flip_virt(a):
    z = [6,5,4,3,2,1,0,
         13,12,11,10,9,8,7,
         20,19,18,17,16,15,14,
         27,26,25,24,23,22,21,
         34,33,32,31,30,29,28,
         41,40,39,38,37,36,35]
    finished = []
    for state in a:
        new = ''
        for i in z:
             new += state[i-1]
        finished.append(new)
    return finished

def rotations():
    # distinctBoards = list(validBoards())
    # dump(distinctBoards, open("distinctBoards.pkl", 'wb'))
    distinctBoards = load(open("distinctBoards.pkl", 'rb'))
    boards_flip_virt = flip_virt(distinctBoards)
