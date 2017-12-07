import sys

from Box2D import b2Vec2

from .utils import (load_default_values, fill_in_with_default, deg_to_rad,
                    check_mandatory_keys)


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

    polygon_mandatory_keys = [
        'vertices'
    ]

    def __init__(self, environment, part_name, part_values):
        self.name = part_name

        # check for mandatory keys in part definition
        self.check_mandatory_values(part_values)

        # fill uninformed bodypart values with defaults
        default_values = load_default_values("PART")
        part_values = fill_in_with_default(part_values, default_values, self.keys)

        self.type = part_values["type"]
        self.color = part_values["color"]

        self.create_body(environment, part_values)

        self.values = part_values

    def reset(self, environment):
        environment.DestroyBody(self.body)
        self.create_body(environment, self.values)

    def create_body(self, environment, part_values):
        # create part's body

        if part_values["angle"] != 0:
            angle = deg_to_rad(part_values["angle"])
        else:
            angle = 0

        if part_values["static"] is True:
            body = environment.CreateStaticBody(position=part_values["initial_position"],
                                                angle=angle)
        else:
            body = environment.CreateDynamicBody(position=part_values["initial_position"],
                                                 angle=angle)

        if self.type == 'box':
            body.CreatePolygonFixture(box=part_values["box_size"],
                                      density=part_values["density"],
                                      friction=part_values["friction"])
        elif self.type == 'circle':
            body.CreateCircleFixture(radius=part_values["radius"],
                                     density=part_values["density"],
                                     friction=part_values["friction"])
        elif self.type == 'polygon':
            if type(part_values["vertices"]) == list:
                for v in part_values["vertices"]:
                    if type(v) != list or len(v) != 2:
                        print("[ERROR] Vertices list of a part must be a list of pairs")
                        sys.exit()
            else:
                print("[ERROR] Vertices list of a part must be a list of pairs")
                sys.exit()
            body.CreatePolygonFixture(vertices=part_values["vertices"],
                                      density=part_values["density"],
                                      friction=part_values["friction"])

        self.body = body

    def check_mandatory_values(self, part_values):
        check_mandatory_keys(self.mandatory_keys, part_values, self.name)

        if part_values["type"] == 'box':
            check_mandatory_keys(self.box_mandatory_keys, part_values, self.name)

        elif part_values["type"] == 'circle':
            check_mandatory_keys(self.circle_mandatory_keys, part_values, self.name)

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

    def read_state(self):
        state = {
            'position': self.body.position,
            'angularVelocity': self.body.angularVelocity,
            'angle': self.body.angle,
            'linearVelocity': (self.body.linearVelocity[0], self.body.linearVelocity[1]),
        }
        # print(self.body)
        return state
