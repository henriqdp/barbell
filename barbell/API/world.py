from Box2D import b2World
from Box2D.b2 import (polygonShape)

from .utils import load_default_values, fill_in_with_default


class World(b2World):
    name = "WORLD"
    floor_name = "FLOOR"

    keys = [
        'gravity',
        'do_sleep',
    ]

    def __init__(self, world_structure, screen):
        default_values = load_default_values(self.name)
        world_structure = fill_in_with_default(world_structure, default_values, self.keys)
        self.values = world_structure
        super().__init__(gravity=self.values["gravity"], doSleep=self.values["do_sleep"])

        # creates default floor
        if "floor" in self.values:
            if self.values["floor"] == "default":
                floor_values = load_default_values(self.floor_name)
                floor_size = [screen.values["width"], 2]
                floor_body = self.CreateStaticBody(position=floor_values["position"],
                                                   shapes=polygonShape(box=floor_size,))

                self.floor = floor_body
                self.values["floor_color"] = floor_values["color"]
            else:
                pass  # TODO: create floor dynamically

    def step(self, delta):
        super().Step(delta, 10, 10)
