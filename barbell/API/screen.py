from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)


class Screen(object):
    def __init__(self, screen_structure, pygame):
        width = 640
        height = 480
        self.pygame = pygame
        self.screen = self.pygame.display.set_mode((width, height), 0, 32)
        self.pygame.display.set_caption('henrique')

    def check_events(self):
        events = []
        for event in self.pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # The user closed the window or pressed escape
                events.append('exit')
        return events

    def fill(self):
        self.screen.fill((0, 0, 0, 0))
