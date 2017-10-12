import pygame
import Box2D  # NOQA

from .bodypart import BodyPart
from .screen import Screen
from .world import World


class Barbell(object):
    def __init__(self, structure):
        # load SCREEN into Barbell
        if "SCREEN" in structure:
            self.initialize_screen(structure["SCREEN"])
        else:
            self.initialize_screen({})
            print("[WARNING] section 'SCREEN' not declared, loading default values")

        # load WORLD into Barbell
        if "WORLD" in structure:
            self.create_world(structure["WORLD"])
        else:
            self.create_world({})
            print("[WARNING] section 'WORLD' not declared, loading default values")

        # load PARTS into Barbell
        self.parts = []
        if "PARTS" in structure:
            self.create_parts(structure["PARTS"])
        else:
            print("[WARNING] section 'PARTS' not declared, your agent simply does not exist. Is that what you wanted to achieve?")

        self.running = True

    def initialize_screen(self, screen_structure):
        self.screen = Screen(screen_structure, pygame)

    def create_world(self, world_structure):
        self.world = World(world_structure)

    def create_parts(self, parts_structure):
        for part in parts_structure:
            self.parts.append(BodyPart(part))

    def step(self):
        events = self.screen.check_events()
        if 'exit' in events:
            self.running = False
        self.screen.update(self.world)
