import dill

with open('trained_player.pkl', 'rb') as f:
    trained_player = dill.load(f)
trained_player.set_params(epsilon=0) # Full exploitation, no random moves

no_episodes = 1000
rewards = pd.Series(np.zeros(no_episodes))
for ep_idx in tqdm(range(no_episodes)):
    while not tictactoe.is_endstate():
        tictactoe = trained_player.make_move(tictactoe)
        tictactoe = trained_player.make_computer_move(tictactoe)

    rewards[ep_idx] = tictactoe.get_reward(1)
    tictactoe.reset_board()
print(rewards.value_counts())
