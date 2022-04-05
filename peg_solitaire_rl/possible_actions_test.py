board = [['O' for j in range(i+1)] for i in range(6)]
# board[3][2] = '-'
board[0][0] = '-'
spaces = []
for i in range(6):
    for j in range(i+1):
        spaces.append((i,j))


def get_adj(space):
    directions = {"R"  : (space[0], space[1] + 1),
                  "L"  : (space[0], space[1] - 1),
                  "TL" : (space[0] - 1, space[1] - 1),
                  "TR" : (space[0] - 1, space[1]),
                  "BL" : (space[0] + 1, space[1]),
                  "BR" : (space[0] + 1, space[1] + 1)}
    return directions

empty_spaces = []
for i, row in enumerate(board):
    for j, col in enumerate(row):
        if col == '-':
            empty_spaces.append((i,j))

possible_actions = []
for space in empty_spaces:
    adj = get_adj(space)
    for z in adj:
        if adj[z] in spaces and board[adj[z][0]][adj[z][1]] == 'O':
            move = get_adj(adj[z])[z]
            if move in spaces and board[move[0]][move[1]] == 'O':
                possible_actions.append((space, adj[z], move))

print(f'board: {board}')
print(f'empty_spaces: {empty_spaces}')
print(f'possible_actions: {possible_actions}')

def printBoard(board):
    print('    1   2   3   4   5   6 \n')
    for i, row in enumerate(board):
        print(end = f' {i+1}  {"  "*(5-i)}')
        for elt in row:
            print(f'{elt}   ', end='')
        print('\n')

printBoard(board)
