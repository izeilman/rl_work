from abc import ABC, abstractmethod
import os
import pickle
import collections
import numpy as np
import random
from .teacher import possible_actions
os.chdir('\\'.join(str(__file__).split("\\")[:-1]))


class Learner(ABC):
    """
    Parent class for Q-learning and SARSA agents.

    Parameters
    ----------
    alpha : float
        learning rate
    gamma : float
        temporal discounting rate
    eps : float
        probability of random action vs. greedy action
    eps_decay : float
        epsilon decay rate. Larger value = more decay
    """
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        # Agent parameters
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.eps_decay = eps_decay
        # Possible actions correspond to the set of all x,y coordinate pairs
        self.actions = []
        for i in range(6):
            for j in range(i+1):
                self.actions.append((i,j))
        # Initialize Q values to 0 for all state-action pairs.
        # Access value for action a, state s via Q[a][s]
        self.Q = {}
        # Keep a list of reward received at each episode
        self.rewards = []

    def get_action(self, s, board):

        # Only consider the allowed actions (empty board spaces)

        if random.random() < self.eps:
            # Random choose.
            actions = possible_actions(board)
            print(len(actions), flush = True)
            print(actions, flush = True)
            selection = random.choice(actions)
        else:
            # Greedy choose.
            actions = possible_actions(board)
            for a in actions:
                if a not in self.Q:
                    self.Q[a] = collections.defaultdict(int)
            values = np.array([self.Q[a][s] for a in actions])
            # Find location of max
            if len(values) == 0:
                selection = random.choice(actions)
            else:
                ix_max = np.where(values == np.max(values))[0]
                if len(ix_max) > 1:
                    # If multiple actions were max, then sample from them
                    ix_select = np.random.choice(ix_max, 1)[0]
                else:
                    # If unique max action, select that one
                    ix_select = ix_max[0]
                selection = actions[ix_select]

        # update epsilon; geometric decay
        self.eps *= (1.-self.eps_decay)

        return selection

    def save(self, path):
        """ Pickle the agent object instance to save the agent's state. """
        if os.path.isfile(path):
            os.remove(path)
        f = open(path, 'wb')
        pickle.dump(self, f)
        f.close()

    @abstractmethod
    def update(self, s, s_, a, a_, r):
        pass


class Qlearner(Learner):
    """
    A class to implement the Q-learning agent.
    """
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

    def update(self, s, s_, a, a_, r, board):
        """
        Perform the Q-Learning update of Q values.

        Parameters
        ----------
        s : string
            previous state
        s_ : string
            new state
        a : (i,j) tuple
            previous action
        a_ : (i,j) tuple
            new action. NOT used by Q-learner!
        r : int
            reward received after executing action "a" in state "s"
        """
        # Update Q(s,a)
        if s_ is not None:
            # hold list of Q values for all a_,s_ pairs. We will access the max later
            actions = possible_actions(board)
            for a in actions:
                if a not in self.Q:
                    self.Q[a] = collections.defaultdict(int)
            Q_options = [self.Q[action][s_] for action in actions]
            # update
            self.Q[a][s] += self.alpha*(r + self.gamma*max(Q_options) - self.Q[a][s])
        else:
            # terminal state update
            self.Q[a][s] += self.alpha*(r - self.Q[a][s])

        # add r to rewards list
        self.rewards.append(r)


class SARSAlearner(Learner):
    """
    A class to implement the SARSA agent.
    """
    def __init__(self, alpha, gamma, eps, eps_decay=0.):
        super().__init__(alpha, gamma, eps, eps_decay)

    def update(self, s, s_, a, a_, r):
        """
        Perform the SARSA update of Q values.

        Parameters
        ----------
        s : string
            previous state
        s_ : string
            new state
        a : (i,j) tuple
            previous action
        a_ : (i,j) tuple
            new action
        r : int
            reward received after executing action "a" in state "s"
        """
        # Update Q(s,a)
        if s_ is not None:
            self.Q[a][s] += self.alpha*(r + self.gamma*self.Q[a_][s_] - self.Q[a][s])
        else:
            # terminal state update
            self.Q[a][s] += self.alpha*(r - self.Q[a][s])

        # add r to rewards list
        self.rewards.append(r)
