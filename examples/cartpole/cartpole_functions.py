import os
import numpy as np


class CartpoleIntelligence(object):
    features = [
        'cart_x',
        'cart_speed',
        'pole_angle',
        'pole_angular_velocity',
    ]

    def __init__(self, initialize_weights=True, max_iterations=1000, weights=[]):
        if initialize_weights:
            open(os.path.join(os.path.dirname(__file__), 'weights.txt'), 'w+')
            self.weights = np.random.rand(len(self.features)) * 2 - 1
        else:
            self.weights = weights
        self.max_iterations = max_iterations
        self.best_reward = 0
        self.last_reward = 0
        self.best_weights = []
        self.counter = 0

        self.noise_scaling = 0.1
        self.mode = 'hill_climbing'

    def reset_function(self, state):
            pole_angle = state["agent"]["pole"]["angle"]
            current_iteration = state["current_iteration"]
            if pole_angle > 90 or  \
               pole_angle < -90 or \
               current_iteration > self.max_iterations:
                return True
            else:
                return False

    def reward_function(self, state):
        reward = state["current_iteration"]
        # print("Epoch ended with reward of %d" % reward)

        if reward > self.best_reward:
            self.best_weights = self.weights
            self.best_reward = reward
            print("Weights are being updated")
            self.save_weights()

        if self.mode == 'hill_climbing':
            if reward > self.last_reward:
                self.weights += (np.random.rand(len(self.features)) * 2 - 1) * self.noise_scaling
            else:
                self.mode = 'random_search'
        elif self.mode == 'random_search':
            self.weights = np.random.randn(len(self.features))
            self.mode = 'hill_climbing'

        if self.counter % 100 == 0:
            print("Best reward so far: %d" % self.best_reward)
        self.counter += 1

        self.last_reward = reward
        return reward

    def fake_reward(self, state):
        return 0

    def compute_features(self, state):
        # print(state["agent"]["pole"]["angle"])
        features = [
            state["agent"]["cart"]["position"][0],
            state["agent"]["cart"]["linearVelocity"][0],
            state["agent"]["pole"]["angle"],
            state["agent"]["pole"]["angularVelocity"],
        ]
        # print(features / np.linalg.norm(features))
        return features / np.linalg.norm(features)

    def action_function(self, barbell, state):
        # self.weights = np.random.rand(len(self.features)) * 2 - 1
        action = np.dot(self.weights, self.compute_features(state))
        if action < 0:
            barbell.agent.push_cart((-10, 0))
        else:
            barbell.agent.push_cart((10, 0))

    def save_weights(self):
        f = open(os.path.join(os.path.dirname(__file__), 'weights.txt'), 'w+')
        for weight in self.weights:
            f.write("%f\n" % weight)
