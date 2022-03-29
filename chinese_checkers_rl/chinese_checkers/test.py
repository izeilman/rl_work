board = [['-' for j in range(i+1)] for i in range(6)]
possible_actions = []
for i, row in enumerate(board):
    for j, col in enumerate(row):
        if col == '-':
            possible_actions.append((i,j))
print(possible_actions)
