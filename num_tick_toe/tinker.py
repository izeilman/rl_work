def train(env):
    start_time = time.time()

    for episode in range(EPISODES):
        env = TicTacToe()
        curr_state = env.state
        isTerminated = False
        add_to_dict(curr_state)
        total_reward = 0

        while not isTerminated:
            current_state_ele = Q_state(curr_state)
            curr_action = epsilon_greedy(curr_state, episode)
            next_state, reward, isTerminated = env.step(curr_state, curr_action)

            next_state_ele = Q_state(next_state)
            add_to_dict(next_state)

            if isTerminated:
                print(curr_action)
                Q_dict[current_state_ele][curr_action] += LR * (
                    (reward - Q_dict[current_state_ele][curr_action]))
            else:
                max_next = max(Q_dict[next_state_ele],
                               key=Q_dict[next_state_ele].get)
                Q_dict[current_state_ele][curr_action] += LR * (
                    (reward + (GAMMA * (Q_dict[next_state_ele][max_next]))) -
                    Q_dict[current_state_ele][curr_action])

            curr_state = next_state
            total_reward += reward

        # Tracking the Q-Values here

        if (episode == threshold-1):        #at the 1999th episode
            initialise_tracking_states()

        if ((episode+1) % threshold) == 0:   #every 2000th episode
            save_tracking_states()
            # save_obj(States_track, 'States_tracked')
            print((episode/15000000)*100)

        # Saving the Policy here

        # if ((episode+1) % policy_threshold ) == 0:  #every 30000th episodes, the Q-dict will be saved
            # save_obj(Q_dict, 'Policy')



    elapsed_time = time.time() - start_time
    # save_obj(States_track, 'States_tracked')
    # save_obj(Q_dict, 'Policy')
    print(elapsed_time)

def play_with_arbitrary_board(curr_state):
    env = TicTacToe()
    isTerminated = False
    total_reward = 0
    episode = 1500

    while not isTerminated:
        curr_action = epsilon_greedy(curr_state, episode)
        next_state, reward, isTerminated = env.step(curr_state, curr_action)
        curr_state = next_state
        total_reward += reward

EPISODES = 15000000
# EPISODES = 20000

LR = 0.01   # learning rate
GAMMA = 0.91

max_epsilon = 1.0
min_epsilon = 0.001

threshold = 2000
policy_threshold = 30000
Q_dict = collections.defaultdict(dict)
States_track = collections.defaultdict(dict)
rewards_tracked =  {(2,1):0, (5,5):0, (8,3): 0, (9,7):0}
initialise_tracking_states()

env = TicTacToe()
# train(env)
States_track = pickle.load(open("States_tracked.pkl", "rb"))
Q_dict = pickle.load(open("Policy.pkl", "rb"))

# board = np.array([7, 8, 9, 2, 5, np.nan, 3, 6, 4])
board = np.array([np.nan, 8, np.nan, 2, np.nan, np.nan, 3, np.nan, 5])
play_with_arbitrary_board(board)
