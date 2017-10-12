from Box2D.b2 import (world, polygonShape)

from .utils import load_default_values, fill_in_with_default


class World(object):
    name = "WORLD"
    floor_name = "FLOOR"

    keys = [
        'gravity',
        'do_sleep'
    ]

    def __init__(self, world_structure):
        default_values = load_default_values(self.name)
        world_structure = fill_in_with_default(world_structure, default_values, self.keys)
        self.values = world_structure
        self.world = world(gravity=self.values["gravity"], doSleep=self.values["do_sleep"])

        # creates default floor
        if "floor" in self.values:
            if self.values["floor"] == "default":
                floor_values = load_default_values(self.floor_name)

                floor_body = self.world.CreateStaticBody(position=floor_values["position"],
                                                         shapes=polygonShape(box=floor_values["box"],))

                self.floor = floor_body
                self.values["floor_color"] = floor_values["color"]
            else:
                pass  # TODO: create floor dynamically
