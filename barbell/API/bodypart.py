import sys

from Box2D import b2Vec2

from .utils import load_default_values, fill_in_with_default, deg_to_rad


class BodyPart(object):
    keys = [
        'density',
        'friction',
        'angle',
        'color',
        'static'
    ]

    mandatory_keys = [
        'initial_position',
        'type',
    ]

    box_mandatory_keys = [
        'box_size'
    ]

    circle_mandatory_keys = [
        'radius'
    ]

    def __init__(self, world, part_name, part_values):
        self.name = part_name

        # check for mandatory keys in world definition
        self.check_mandatory_values(part_values)

        # fill uninformed bodypart values with defaults
        default_values = load_default_values("PART")
        part_values = fill_in_with_default(part_values, default_values, self.keys)

        self.type = part_values["type"]
        self.color = part_values["color"]

        self.create_body(world, part_values)

        self.values = part_values

    def reset(self, world):
        world.DestroyBody(self.body)
        self.create_body(world, self.values)

    def create_body(self, world, part_values):
        # create part's body

        if part_values["angle"] != 0:
            part_values["angle"] = deg_to_rad(part_values["angle"])

        if part_values["static"] is True:
            body = world.CreateStaticBody(position=part_values["initial_position"],
                                          angle=part_values["angle"])
        else:
            body = world.CreateDynamicBody(position=part_values["initial_position"],
                                           angle=part_values["angle"])

        if self.type == 'box':
            body.CreatePolygonFixture(box=part_values["box_size"],
                                      density=part_values["density"],
                                      friction=part_values["friction"])
        elif self.type == 'circle':
            body.CreateCircleFixture(radius=part_values["radius"],
                                     density=part_values["density"],
                                     friction=part_values["friction"])

        self.body = body

    def check_mandatory_values(self, part_values):
        for key in self.mandatory_keys:
            if key not in part_values:
                sys.exit("Missing key in part %s: %s" % (self.name, key,))

        if part_values["type"] == 'box':
            for key in self.box_mandatory_keys:
                if key not in part_values:
                    sys.exit("Missing key for box %s: %s" % (self.name, key,))

        elif part_values["type"] == 'circle':
            for key in self.circle_mandatory_keys:
                if key not in part_values:
                    sys.exit("Missing key for circle %s: %s" % (self.name, key,))

    def apply_force(self, force_type, force_vector):
        if force_type == "local":
            force_vector = self.body.GetWorldVector(localVector=force_vector)
        elif force_type == "global":
            force_vector = b2Vec2(force_vector[0], force_vector[1])
        else:
            print("[WARNING] %s is not a valid force type." % force_type)
            return
        point = self.body.GetWorldPoint(localPoint=(0.0, 0.0))
        self.body.ApplyForce(force_vector, point, True)
