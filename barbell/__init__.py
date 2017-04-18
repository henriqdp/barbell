import gym
import yaml

class Barbell:
    def new(self, env_name):
        if ".yaml" in env_name:
            print("LOL YAML file")
        else:
            self.env = gym.make(env_name)
            self.action_space = self.env.action_space
