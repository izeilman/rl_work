import pickle
import os
os.chdir('\\'.join(str(__file__).split("\\")[:-1]))


x = pickle.load(open("10k.pkl", "rb"))
print(x.Q)
