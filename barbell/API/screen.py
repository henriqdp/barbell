import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)
from .utils import load_default_values, fill_in_with_default, coord_box2d_to_pygame


class Screen(object):
    keys = [
        'width',
        'height',
        'target_fps',
        'caption',
        'background_color',
        'ppm'
    ]

    def __init__(self, screen_structure):
        default_values = load_default_values("SCREEN")
        screen_values = fill_in_with_default(screen_structure, default_values, self.keys)
        self.values = screen_values
        self.pygame = pygame
        self.screen = self.pygame.display.set_mode((self.values["width"], self.values["height"]), 0, 32)
        self.pygame.display.set_caption(self.values["caption"])
        self.clock = self.pygame.time.Clock()

    def check_events(self):
        events = []
        for event in self.pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # The user closed the window or pressed escape
                events.append('exit')
        return events

    def fill(self):
        self.screen.fill(self.values["background_color"])

    def draw_floor(self, world):
        if isinstance(world.floor, list):
            pass  # TODO: draw floor dynamically etc
        else:
            for fixture in world.floor.fixtures:
                # TODO: arrumar esse código porco
                shape = fixture.shape
                vertices = [(world.floor.transform * v) * self.values["ppm"] for v in shape.vertices]
                vertices = [(v[0], self.values["height"] - v[1]) for v in vertices]
                self.pygame.draw.polygon(self.screen, world.values["floor_color"], vertices)

    def draw_parts(self, parts):
        for part in parts:
            for fixture in part.body.fixtures:
                shape = fixture.shape
                vertices = [(part.body.transform * v) * self.values["ppm"] for v in shape.vertices]
                vertices = [(v[0], self.values["height"] - v[1]) for v in vertices]
                self.pygame.draw.polygon(self.screen, part.color, vertices)

    def flip(self):
        self.pygame.display.flip()

    def update(self, world, parts):
        self.fill()
        self.draw_floor(world)
        self.draw_parts(parts)
        world.step(1 / self.values["target_fps"])
        self.clock.tick(self.values["target_fps"])
        self.flip()
