import gym
import yaml

class Barbell:
    def __init__(self, env_name):
        if ".yaml" in env_name:
            print("LOL YAML file")
        else:
            self.env = gym.make(env_name)
            self.action_space = self.env.action_space
            self.env.reset()

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        self.env.reset()
