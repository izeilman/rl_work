# spaces = []
# for i in range(6):
#     for j in range(i+1):
#         spaces.append((i,j))

# from itertools import permutations

# empty = '-'*21
# boards = []
# for i in range(20):
#     boards.append("X"*(i+1) + empty[:-(i+1)])



# 0
# 1  2
# 3  4  5
# 6  7  8 9
# 10 11 12 13 14
# 15 16 17 18 19 20

def rot90(a):
    z = [15,
         16, 10,
         17, 11, 6,
         18, 12, 7, 3,
         19, 13, 8, 4, 1,
         20, 14, 9, 5, 2, 0]
    finished = []
    for state in a:
        new = ''
        for i in z:
             new += state[i-1]
        finished.append(new)
    return finished


def flip_virt(a):
    z = [0,
         2, 1,
         5, 4, 3,
         9, 8, 7, 6,
         14, 13, 12, 11, 10,
         20, 19, 18, 17, 16, 15]
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
    boards_rot_90 = rot90(distinctBoards)
    boards_rot_180 = rot90(boards_rot_90)
    boards_flip_virt = flip_virt(distinctBoards)
