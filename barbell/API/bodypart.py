import sys
import random

from Box2D import b2Vec2

from .utils import (load_default_values, fill_in_with_default, deg_to_rad,
                    check_mandatory_keys, rad_to_deg)


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
        if part_values["angle"] == 'random':
            angle = deg_to_rad(random.randint(0, 360))
        elif part_values["angle"] != 0:
            angle = deg_to_rad(part_values["angle"])
        else:
            angle = 0

        if part_values["initial_position"] == "random":
            if 'x_range' not in part_values or 'y_range' not in part_values:
                sys.exit("[ERROR] x_range and y_range must be defined when the initial position of a part/object is set to random")
            elif type(part_values['x_range']) != list or type(part_values['y_range']) != list:
                sys.exit("[ERROR] x_range and y_range must be lists")
            elif len(part_values['x_range']) != 2 or len(part_values['y_range']) != 2:
                sys.exit("[ERROR] x_range and y_range must be 2 in length")
            else:
                x = random.uniform(part_values['x_range'][0], part_values['x_range'][1])
                y = random.uniform(part_values['y_range'][0], part_values['y_range'][1])
                initial_position = (round(x, 2), round(y, 2))
        else:
            initial_position = part_values["initial_position"]
        if part_values["static"] is True:
            body = environment.CreateStaticBody(position=initial_position,
                                                angle=angle)
        else:
            body = environment.CreateDynamicBody(position=initial_position,
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

    def apply_force(self, force_type, anchor, force_vector):
        if force_type == 'rotate':
            self.body.ApplyTorque(force_vector, True)
            return

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
            'angle': rad_to_deg(self.body.angle),
            'linearVelocity': (self.body.linearVelocity[0], self.body.linearVelocity[1]),
        }
        # print(self.body)
        return state
