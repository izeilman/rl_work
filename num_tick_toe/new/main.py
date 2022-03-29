class game:
    def __init__(self):
        self.state = [np.nan for i in range(9)]
        self.game_playing = True
    def action(self, move, value):
        self.move = (move, value)
        self.state[move] = value
    def print_board(self):
        tmp = []
        for i in range(9):
            val = self.state[i]
            if np.isnan(val):
                tmp.append(" ")
            else:
                tmp.append(val)
        i = iter(tmp)
        print(f"""┌───┬───┬───┐\n│ {next(i)} │ {next(i)} │ {next(i)} │\n├───┼───┼───┤\n│ {next(i)} │ {next(i)} │ {next(i)} │\n├───┼───┼───┤\n│ {next(i)} │ {next(i)} │ {next(i)} │\n└───┴───┴───┘""")
    def print_board_demo(self):
        i = iter(range(9))
        print(f"""┌───┬───┬───┐\n│ {next(i) + 1} │ {next(i) + 1} │ {next(i) + 1} │\n├───┼───┼───┤\n│ {next(i) + 1} │ {next(i) + 1} │ {next(i) + 1} │\n├───┼───┼───┤\n│ {next(i) + 1} │ {next(i) + 1} │ {next(i) + 1} │\n└───┴───┴───┘""")


def train():
    pass

# if the Q-val of a board-state is reward,
# choose a board-state - get its reward
# for all the next states possible, get their rewards
# verify that the game does the action that will
# result in the board-state with the highest Q-val
def play():
    env = game()
    pvp = False
    pve = False
    eve = True
    Q_state = {}
    States_Tracked = {}
    while env.game_playing:
        if pvp:
            env.action(input("Move: "))
            env.action(input("Move: "))
        if pve:
            env.action(input("Move: "))
            env.state
            env.action()
        if eve:
            pass
