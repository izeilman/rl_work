# import pickle
# import os
# os.chdir('\\'.join(str(__file__).split("\\")[:-1]))
#
#
# x = pickle.load(open("10k.pkl", "rb"))
# print(x.Q)
board = [['O' for _ in range(i+1)] for i in range(6)]
z = []
for row in board:
    for i in row:
        if i == 'O':
            z.append(i)

print(len(z))
