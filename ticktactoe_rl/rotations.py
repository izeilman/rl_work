axes = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6),(0,3,6),(2,4,7),(2,5,8)]

def isWin(board):
    return any("".join(board[p] for p in axis) in ["XXX","OOO"] for axis in axes)

def validBoards(board="-"*9,player=None):
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
        if isWin(played): continue                # stop game upon winning
        for nextBoard in validBoards(played,opponent):
            print(nextBoard)
            yield nextBoard # return boards for subsequent moves


def print_statistics():
    distinctBoards = list(validBoards())  # only look at distinct board states

    allStates = len(distinctBoards)
    print(f"distinctBoards: {allStates}")  # 8533 counting all intermediate states

    winningStates = sum(isWin(b) for b in  distinctBoards)
    print(f"winningStates: {winningStates}") # 1884  (so 942 for a specific starting player)

    filledStates  = sum(("." not in b) for b in distinctBoards)
    print(f"filledStates: {filledStates}") #  156 states where all cells are filled

    finalStates  = sum(isWin(b) or ("." not in b) for b in distinctBoards)
    print(f"finalStates: {finalStates}") #  1916 end of game states (win or draw)

    earlyWins = sum(isWin(b) and ("." in b) for b in distinctBoards)
    print(f"earlyWins: {earlyWins}") # 1760 wins before filling the board

    draws  = finalStates - winningStates
    print(f"draws: {draws}") #  32 ways to end up in a draw

    lastWins = filledStates-draws
    print(f"lastWins: {lastWins}") # 124 wins on the 9th move (i.e filling the board)

    fastWins = sum( isWin(b) and b.count(".") == 4 for b in distinctBoards)
    print(f"fastWins: {fastWins}") # 240 fastest wins by 1st player (in 3 moves)

    fastCounters = sum( isWin(b) and b.count(".") == 3 for b in distinctBoards)
    print(f"fastCounters: {fastCounters}") # 296 fastest wins by 2nd player (in 3 moves)


from pickle import dump, load
import os
os.chdir('\\'.join(str(__file__).split("\\")[:-1]))

def rot90(a):
    z = [7,4,1,
         8,5,2,
         9,6,3]
    finished = []
    for state in a:
        new = ''
        for i in z:
             new += state[i-1]
        finished.append(new)
    return finished

def flip_horiz(a):
    z = [7,8,9,
         4,5,6,
         1,2,3]
    finished = []
    for state in a:
        new = ''
        for i in z:
             new += state[i-1]
        finished.append(new)
    return finished

def flip_virt(a):
    z = [3,2,1,
         6,5,4,
         9,8,7]
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
    boards_rot90 = rot90(distinctBoards)
    boards_rot180 = rot90(boards_rot90)
    boards_rot270 = rot90(boards_rot180)
    boards_flip_horiz = flip_horiz(distinctBoards)
    boards_flip_virt = flip_virt(distinctBoards)

# rotations()
print_statistics()
