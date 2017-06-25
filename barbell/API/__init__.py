import pyglet
from .. import Barbell


class API:
    def __init__(self, verbose=False, mode="graphic"):
        self.app = pyglet.app
        self. instance = Barbell()

    def run(self):
        self.app.run()
