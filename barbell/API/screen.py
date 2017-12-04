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
        default_values = load_default_values("DOMAIN")
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

    #  TODO: definir se é realmente necessário
    def draw_floor(self, world):
        if world.floor is not None:
            for fixture in world.floor.fixtures:
                shape = fixture.shape
                vertices = vertices_box2d_to_pygame(world.floor, self, shape)
                self.pygame.draw.polygon(self.screen, world.values["floor_color"], vertices)

    def draw_polygon(self, body, color, shape):
        vertices = vertices_box2d_to_pygame(body, self, shape)
        self.pygame.draw.polygon(self.screen, color, vertices)

    def draw_circle(self, body, color, shape):
        circle_coords = get_circle_coordinates(body, self, shape)
        self.pygame.draw.circle(self.screen, color, [int(x) for x in circle_coords[0:2]],
                                int(circle_coords[2]))

    def draw_environment(self, environment):
        for env_object in environment.objects:
            for fixture in environment.objects[env_object]:
                self.draw_polygon(environment.objects[env_object], environment.color, fixture.shape)

    def draw_agent(self, agent):
        for part in agent.parts:
            self.draw_part(agent.parts[part])

    def draw_part(self, part):
        for fixture in part.body.fixtures:
            shape = fixture.shape
            if part.type == 'box':
                self.draw_polygon(part.body, part.color, fixture.shape)
            elif part.type == 'circle':
                self.draw_circle(part.body, part.color, shape)
                # circle_coords = get_circle_coordinates(part.body, self, shape)
                # self.pygame.draw.circle(self.screen, part.color,
                #                         [int(x) for x in circle_coords[0:2]],
                #                         int(circle_coords[2]))
            elif part.type == 'polygon':
                self.draw_polygon(part.body, part.color, fixture.shape)
                pass  # TODO: desenhar polígono

    # TODO: ver se vou usar isso mesmo
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

    def step(self, target_fps):
        self.clock.tick(target_fps)

    def update(self, environment, agent):
        self.fill()
        self.draw_agent(agent)
        self.draw_environment(environment)
        environment.step(self.values["target_fps"])
        self.step(self.values["target_fps"])
        self.flip()
