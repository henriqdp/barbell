import sys

from .screen import Screen
from .environment import Environment
from .agent import Agent


class Barbell(object):
    def __init__(self, structure, render=True):
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

        self.running = True
        self.events = []
        self.render = render

    def initialize_screen(self, screen_structure):
        self.screen = Screen(screen_structure)

    def initialize_environment(self, environment_structure):
        self.environment = Environment(environment_structure, self.screen)

    def create_agent(self, agent_structure):
        self.agent = Agent(self.environment, agent_structure)

    def apply_force(force, vector_type=None, vector=None):
        pass

    def reset(self):
        self.agent.reset(self.environment)

    def step(self):
        self.events = self.screen.check_events()
        if 'exit' in self.events:
            self.running = False
        if self.render:
            self.screen.update(self.environment, self.agent)

    def get_events(self):
        return self.screen.check_events()
