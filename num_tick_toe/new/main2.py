from game import TicTacToe
import collections
import numpy as np
import random
import pickle
import time
from matplotlib import pyplot as plt
import os
os.chdir('\\'.join(str(__file__).split("\\")[:-1]))


def Q_state(state):
    return ('-'.join(str(e) for e in state)).replace('nan','x')

def valid_actions(state):

    valid_Actions = []

    valid_Actions = [i for i in env.action_space(state)[0]] ###### -------please call your environment as env
    return valid_Actions

# Defining a function which will add new Q-values to the Q-dictionary.

def add_to_dict(state):
    state1 = Q_state(state)

    valid_act = valid_actions(state)
    if state1 not in Q_dict.keys():
        for action in valid_act:
            Q_dict[state1][action] = 0

def epsilon_greedy(state, time):
#     epsilon = - 1/ (1 + np.exp((-time+7500000)/1700000)) + 1
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-0.000001*time)
    z = np.random.random()
    if z > epsilon:
        # ===> Q value fetch max value
        state1 = Q_state(state)
        action = max(Q_dict[state1],key=Q_dict[state1].get)
    else:
        # ===> random action generation
        agent_actions, env_actions = env.action_space(state)
        action = random.choice(list(agent_actions))
    return action

def initialise_tracking_states():
    sample_q_values = [('x-x-x-x-x-x-x-x-x',(6,5)),('x-x-x-x-x-x-x-x-x',(1,9)),
                       ('x-3-x-x-1-x-x-x-x',(7,5)),('x-5-x-x-x-x-5-7-x',(8,2))]
    for q_value in sample_q_values:
        state = q_value[0]
        action = q_value[1]
        state1 = Q_state(state)
        States_track[state1][action] = []




#Defining a function to save the Q-dictionary as a pickle file

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def save_tracking_states():
    for state in States_track.keys():
        for action in States_track[state].keys():
            if state in Q_dict and action in Q_dict[state]:
                States_track[state][action].append(Q_dict[state][action])


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
    episode = 0
    while not isTerminated:
        curr_action = epsilon_greedy(curr_state, episode)
        next_state, reward, isTerminated = env.step(curr_state, curr_action)
        curr_state = next_state
        total_reward += reward


class user:
    def __init__(self):
        self.state = [np.nan for i in range(9)]
    def action(self, move, value):
        move -= 1
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


def play_with_ml():
    env = TicTacToe()
    total_reward = 0
    episode = 0
    while episode < 20:
        isTerminated = False
        player = user()
        player.print_board_demo()

        if episode % 2 == 0:
            moves = [i for i in range(9) if i % 2 == 1]
        else:
            moves = [i for i in range(9) if i % 2 == 0]

        while not isTerminated:
            if episode % 2 == 0:
                print(f"Player's move | values remaining {moves}")
                move = int(input("\nposition: "))
                value = int(input("value: "))
                moves.remove(value)
                player.move = (move - 1, value)
                next_state, reward, isTerminated = env.step(player.state, player.move)
                move = epsilon_greedy(player.state, episode)
                # player.move = (move[0], move[1])
                # next_state, reward, isTerminated = env.step(player.state, player.move)
            else:
                move = epsilon_greedy(player.state, episode)
                player.move = (move[0], move[1])
                next_state, reward, isTerminated = env.step(player.state, player.move)
                print(f"Player's move | values remaining {moves}")
                move = int(input("\nposition: "))
                value = int(input("value: "))
                player.move = (move - 1, value)
                moves.remove(value)
                next_state, reward, isTerminated = env.step(player.state, player.move)
            curr_state = next_state
            total_reward += reward
            player.print_board()
        episode += 1


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
initialise_tracking_states()

# env = TicTacToe()
# train(env)
States_track = pickle.load(open("States_tracked.pkl", "rb"))
Q_dict = pickle.load(open("Policy.pkl", "rb"))
print(States_track)
for i in list(Q_dict)[0:5]:
    print(i, Q_dict[i])

# board = np.array([7, 8, 9, 2, 5, np.nan, 3, 6, 4])
# board = np.array([np.nan, 8, np.nan, 2, np.nan, np.nan, 3, np.nan, 5])
# play_with_arbitrary_board(board)

# play_with_ml()
