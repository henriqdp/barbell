import pyglet
from .. import Barbell
from API.object import Object


class API:
    def __init__(self, verbose=False, mode="graphic"):
        self.verbose = verbose
        self.mode = mode

    def initializeBarbell(self):
        self.app = pyglet.app
        self.instance = Barbell()

    def add_object(self):
        new_object = Object(self.instance.space)
        self.instance.objects.append(new_object)

    def add_circle(self):
        pass

    def add_rectangle(self):
        pass

    def run(self):
        self.app.run()
