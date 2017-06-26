import pyglet
from pyglet.window import Window
# from pyglet.text import Label
import pymunk
# import random


class Barbell(Window):
    def __init__(self, mode="graphic"):
        # Basic initial definitions: physics space and epoch
        self.space = pymunk.Space()
        self.epoch = 0

        if mode == "graphic":
            super().__init__(width=800, height=800)

        # Objects vector. Objects are added through API calls
        self.objects = []

        pyglet.clock.schedule(self.update)

    def on_draw(self):
        # pyglet.gl.glClearColor(1, 1, 1, 1)
        self.label.draw()

    def update(self, dt):
        self.clear()
