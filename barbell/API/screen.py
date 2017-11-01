import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)
from .utils import (load_default_values, fill_in_with_default,
                    vertices_box2d_to_pygame, get_circle_coordinates,
                    coord_box2d_to_pygame)


class Screen(object):
    keys = [
        'width',
        'height',
        'target_fps',
        'caption',
        'background_color',
        'draw_joints',
        'joint_color',
        'joint_width',
        'ppm'
    ]

    def __init__(self, screen_structure):
        default_values = load_default_values("SCREEN")
        screen_values = fill_in_with_default(screen_structure, default_values, self.keys)
        self.values = screen_values
        self.pygame = pygame

        screensize = self.get_pygame_screensize()
        self.screen = self.pygame.display.set_mode(screensize, 0, 32)
        self.pygame.display.set_caption(self.values["caption"])
        self.clock = self.pygame.time.Clock()

    def check_events(self):
        events = []
        for event in self.pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # The user closed the window or pressed escape
                events.append('exit')
            elif event.type == KEYDOWN:
                events.append(event.key)
        return events

    def fill(self):
        self.screen.fill(self.values["background_color"])

    def get_pygame_screensize(self):
        screensize = (int(self.values["width"] * self.values["ppm"]),
                      int(self.values["height"] * self.values["ppm"]))
        return screensize

    def draw_floor(self, world):
        if world.floor is not None:
            for fixture in world.floor.fixtures:
                shape = fixture.shape
                vertices = vertices_box2d_to_pygame(world.floor, self, shape)
                self.pygame.draw.polygon(self.screen, world.values["floor_color"], vertices)

    def draw_parts(self, parts):
        for part in parts:
            for fixture in parts[part].body.fixtures:
                shape = fixture.shape
                if parts[part].type == 'box':
                    vertices = vertices_box2d_to_pygame(parts[part].body, self, shape)
                    self.pygame.draw.polygon(self.screen, parts[part].color, vertices)
                elif parts[part].type == 'circle':
                    circle_coords = get_circle_coordinates(parts[part].body, self, shape)
                    self.pygame.draw.circle(self.screen, parts[part].color, [int(
                        x) for x in circle_coords[0:2]], int(circle_coords[2]))

    def draw_joints(self, world):
        for joint in world.joints:
            start = coord_box2d_to_pygame(joint.anchorA, self)
            end = coord_box2d_to_pygame(joint.anchorB, self)
            self.pygame.draw.line(self.screen,
                                  self.values["joint_color"],
                                  start,
                                  end,
                                  self.values["joint_width"])

    def flip(self):
        self.pygame.display.flip()

    def update(self, world, parts):
        self.fill()
        self.draw_floor(world)
        self.draw_parts(parts)
        if self.values["draw_joints"]:
            print(self.draw_joints)
            self.draw_joints(world)
        world.step(1 / self.values["target_fps"])
        self.clock.tick(self.values["target_fps"])
        self.flip()
