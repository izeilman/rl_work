from pickle import load
import os
os.chdir('\\'.join(str(__file__).split("\\")[:-1]))

df = load(open("10k.pkl", 'rb'))

def f(x):
    for i in x.Q:
        if len(x.Q[i]) > 0:
            print(f"{i}\n{len(x.Q[i])}\n")
        else:
            print(f"{i}\n{x.Q[i]}\n")

print(df.Q[(0,0)])
