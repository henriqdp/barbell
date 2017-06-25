import pyglet
from pyglet.window import Window
import pymunk
import random


class Barbell(Window):
    def __init__(self, mode="graphic"):
        self.space = pymunk.Space()
        self.epoch = 0

        if mode == "graphic":
            super().__init__(width=800, height=800)

        pyglet.clock.schedule(self.update)

    def on_draw(self):
        print(random.randint(0, 10))

    def update(self, dt):
        pass
