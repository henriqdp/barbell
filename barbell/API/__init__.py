import pygame
import Box2D  # NOQA

from .bodypart import BodyPart
from .screen import Screen


class Barbell(object):
    def __init__(self, structure):
        try:
            self.parts = []
            for part in structure["PARTS"]:
                self.parts.append(BodyPart(part))
        except KeyError:
            print("[WARNING] section 'PARTS' was not declared")
        self.structure = structure
        self.screen = Screen(structure, pygame)
        self.running = True

    def step(self):
        events = self.screen.check_events()
        if 'exit' in events:
            self.running = False
        self.screen.fill()
