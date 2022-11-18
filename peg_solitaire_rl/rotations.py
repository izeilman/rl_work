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

def rot(Q):
    z = [15,
         16, 10,
         17, 11, 6,
         18, 12, 7, 3,
         19, 13, 8, 4, 1,
         20, 14, 9, 5, 2, 0]
    new = {}
    keys = list(Q.keys())
    values = list(Q.values())
    for i, v in enumerate(z):
        new[keys[i]] = values[v]
    return new


# def flip_virt(Q):
#     z = [0,
#          2, 1,
#          5, 4, 3,
#          9, 8, 7, 6,
#          14, 13, 12, 11, 10,
#          20, 19, 18, 17, 16, 15]
#     new = {}
#     keys = list(Q.keys())
#     values = list(Q.values())
#     for i, v in enumerate(z):
#         new[keys[i]] = values[v-1]
#     return new
import os
os.chdir('\\'.join(str(__file__).split("\\")[:-1]))
from math import isclose
from pickle import dump, load
def main():
    name = "10k"
    x = load(open(f"{name}.pkl", "rb"))

    x.Q = rot(x.Q) # r1
    if not os.path.exists(f"{name}-r1.pkl"):
        dump(x, open(f"{name}-r1.pkl", "wb"))

    x.Q = rot(x.Q) # r2
    if not os.path.exists(f"{name}-r2.pkl"):
        dump(x, open(f"{name}-r2.pkl", "wb"))

    x.Q = rot(x.Q) # r3
    if not os.path.exists(f"{name}-r3.pkl"):
        dump(x, open(f"{name}-r3.pkl", "wb"))



    x1 = load(open(f"{name}-r1.pkl", "rb"))
    x2 = load(open(f"{name}-r2.pkl", "rb"))
    x3 = load(open(f"{name}-r3.pkl", "rb"))

    for b, Q in ({"r1":x1.Q, "r2":x2.Q, "r3":x3.Q}).items():
        print("Rotation", b)
        for i in list(list(x.Q.items())):
            symmetry = 0
            count = 0
            move_option, rewards = i # unpack
            for board, value in rewards.items():
                count += 1
                # if the reward value for the space of the Q tables are similar within an absolute total
                # Increment/Decrement symmetry value
                if isclose(Q[move_option][board], value, abs_tol = .05): symmetry += 1
                else: symmetry -= 1
            print(f"  {move_option} %{(symmetry/count)*100:.2f} similar")

if __name__ == "__main__":
    main()
