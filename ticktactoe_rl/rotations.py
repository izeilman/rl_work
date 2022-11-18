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



# distinctBoards = list(validBoards())
# dump(distinctBoards, open("distinctBoards.pkl", 'wb'))
# distinctBoards = load(open("distinctBoards.pkl", 'rb'))

from pickle import load, dump
import os
os.chdir(os.path.dirname(__file__))

def rot90(Q):
    z = [7,4,1,
         8,5,2,
         9,6,3]
    new = {}
    keys = list(Q.keys())
    values = list(Q.values())
    for i, v in enumerate(z):
        new[keys[i]] = values[v-1]
    return new





from math import isclose
def main():
    name = "5M"
    x = load(open(f"q_{name}.pkl", "rb"))

    x.Q = rot90(x.Q) # 90
    if not os.path.exists(f"{name}-r90.pkl"):
        dump(x, open(f"{name}-r90.pkl", "wb"))

    x.Q = rot90(x.Q) # 180
    if not os.path.exists(f"{name}-r180.pkl"):
        dump(x, open(f"{name}-r180.pkl", "wb"))

    x.Q = rot90(x.Q) # 270
    if not os.path.exists(f"{name}-r270.pkl"):
        dump(x, open(f"{name}-r270.pkl", "wb"))

    x.Q = rot90(x.Q) # 360
    if not os.path.exists(f"{name}-r360.pkl"):
        dump(x, open(f"{name}-r360.pkl", "wb"))


    x1 = load(open(f"{name}-r90.pkl", "rb"))
    x2 = load(open(f"{name}-r180.pkl", "rb"))
    x3 = load(open(f"{name}-r270.pkl", "rb"))
    x4 = load(open(f"{name}-r360.pkl", "rb"))

    for b, Q in ({"90":x1.Q, "180":x2.Q, "270":x3.Q, "360":x4.Q}).items():
        print("Rotated by", b)
        for i in list(list(x.Q.items())):
            symmetry = 0
            count = 0
            move_option, rewards = i # unpack
            for board, value in rewards.items():
                count += 1
                # if the reward value for the space of the Q tables are similar within an absolute total
                # Increment/Decrement symmetry value
                if isclose(Q[move_option][board], value, abs_tol = .6): symmetry += 1
                else: symmetry -= 1
            print(f"  {move_option} %{(symmetry/count)*100:.2f} similar")

if __name__ == "__main__":
    main()
