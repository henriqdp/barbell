import sys

from .screen import Screen
from .environment import Environment
from .agent import Agent


class Barbell(object):
    def __init__(self, structure, render=True):
        self.running = True
        self.events = []
        self.render = render

        # load SCREEN into Barbell
        if "DOMAIN" in structure:
            self.initialize_screen(structure["DOMAIN"])
        else:
            self.initialize_screen({})
            print("[WARNING] section 'SCREEN' not declared, loading default values")

        # load ENVIRONMENT into Barbell
        if "ENVIRONMENT" in structure:
            self.initialize_environment(structure["ENVIRONMENT"])
        else:
            self.create_environment({})
            print("[WARNING] section 'ENVIRONMENT' not declared, loading default values")

        # initialize agent
        if "AGENT" in structure:
            self.create_agent(structure["AGENT"])
        else:
            sys.exit("[ERROR] No agent declared")

        self.current_iteration = 0
        self.last_reward = None

        self.reward_function = None
        self.action_function = None
        self.reset_function = None
        self.no_reward_function_warning = False
        self.no_action_function_warning = False
        self.no_reset_function_warning = False

    def set_reward_function(self, reward_function):
        self.reward_function = reward_function

    def set_reset_function(self, reset_function):
        self.reset_function = reset_function

    def set_action_function(self, action_function):
        self.action_function = action_function

    def initialize_screen(self, screen_structure):
        self.screen = Screen(screen_structure, self.render)

    def initialize_environment(self, environment_structure):
        self.environment = Environment(environment_structure, self.screen)

    def create_agent(self, agent_structure):
        self.agent = Agent(self.environment, agent_structure)

    def apply_force(force, vector_type=None, vector=None):
        pass

    def reset(self):
        if self.reward_function:
            reward = self.reward_function(self.get_state())
            self.last_reward = reward
        else:
            if not self.no_reward_function_warning:
                print("[WARNING] No reward function was defined. No reward will be computed")
                self.no_reward_function_warning = True

        self.current_iteration = 0
        self.agent.reset(self.environment)

    def step(self):
        state = self.get_state()
        self.current_iteration += 1

        if not self.action_function:
            if not self.no_action_function_warning:
                print("[WARNING] No action function have been provided")
                print("Set an action function by calling the set_action_function() method")
                self.no_action_function_warning = True
        else:
            self.action_function(self, state)

        if not self.reset_function:
            if not self.no_reset_function_warning:
                print("[WARNING] No reset function have been provided. Environment resetting will have to be by calling barbell.reset()")
                print("Set a reset function by calling the set_reset_function() method")
                self.no_reset_function_warning = True
        else:
            if self.reset_function(state):
                self.reset()

        self.events = self.screen.check_events()
        if 'exit' in self.events:
            self.running = False

        # updates environment
        self.environment.step(self.screen.values["target_fps"])
        if self.render:
            self.screen.update(self.environment, self.agent)
        return state

    def get_events(self):
        if self.render:
            return self.screen.check_events()
        else:
            return []

    def get_state(self):
        state = {
            'current_iteration': self.current_iteration,
            'agent': self.agent.get_state()
        }
        return state
