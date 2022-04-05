import pickle
import os
os.chdir('\\'.join(str(__file__).split("\\")[:-1]))
Q_dict = pickle.load(open("q_5000000.pkl", "rb"))
print(Q_dict.Q.keys())
print()
print(Q_dict.Q[(0,2)])

it = iter(Q_dict.Q.values())
# for i in range(9):
#     print((i // 3, i % 3))
# d = {}
# for i in reversed(range(9)):
#     # print((i//3, (i%3)))
#     d[(i//3, (i%3))] = next(it)

print(type(Q_dict.Q))
Q_dict.Q = d
d.sort()
print(d.keys())
Q_dict.save("q_5M_reversed.pkl")
