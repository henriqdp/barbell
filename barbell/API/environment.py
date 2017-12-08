import sys, random

from Box2D import b2World
from Box2D.b2 import (polygonShape)

from .utils import load_default_values, fill_in_with_default, deg_to_rad


class Environment(b2World):
    name = "ENVIRONMENT"
    floor_name = "FLOOR"
    distance_joint_name = "DISTANCE_JOINT"
    revolute_joint_name = "REVOLUTE_JOINT"
    prismatic_joint_name = "PRISMATIC_JOINT"
    object_name = "OBJECT"

    keys = [
        'gravity',
        'do_sleep',
        'floor',
        'objects_color',
    ]

    joint_keys = [
        'anchor_a',
        'anchor_b',
        'anchor_a_offset',
        'anchor_b_offset',
    ]

    distance_joint_keys = [
        'anchor_a_offset',
        'anchor_b_offset',
    ]

    revolute_joint_keys = [
        'anchor_a',
        'anchor_b',
    ]

    prismatic_joint_keys = [
        'anchor',
        'axis',
        'max_motor_force',
        'enable_motor',
        'motor_speed',
        'lower_translation',
        'upper_translation',
        'enable_limit',
    ]

    object_keys = [
        'type',
        'initial_position',
        'angle',
        'static',
        'density',
        'friction'

    ]

    def __init__(self, world_structure, screen):
        default_values = load_default_values(self.name)
        world_structure = fill_in_with_default(world_structure, default_values, self.keys)
        self.values = world_structure
        self.color = world_structure["objects_color"]
        self.objects = {}
        super().__init__(gravity=self.values["gravity"], doSleep=self.values["do_sleep"])

        # creates default floor
        if "floor" in self.values:
            if self.values["floor"] == "default":
                floor_values = load_default_values(self.floor_name)
                floor_size = [screen.values["width"], 2]
                floor_body = self.CreateStaticBody(position=floor_values["position"],
                                                   shapes=polygonShape(box=floor_size,))

                self.objects["floor"] = floor_body
                self.floor = floor_body
            elif self.values["floor"] == "none":
                self.floor = None

        if "OBJECTS" in self.values:
            object_values = load_default_values(self.object_name)   # NOQA
            for world_object in self.values["OBJECTS"]:
                for object_name in world_object:
                    object_structure = fill_in_with_default(world_object[object_name], object_values, self.object_keys)
                    if object_name in self.objects:
                        sys.exit("[ERROR] Object %s is being redefined" % object_name)
                    self.objects[object_name] = self.create_object(object_structure)

    def create_object(self, object_values):
        if object_values["angle"] == 'random':
            angle = deg_to_rad(random.randint(0, 360))
        elif object_values["angle"] != 0:
            angle = deg_to_rad(object_values["angle"])
        else:
            angle = 0

        if object_values["initial_position"] == "random":
            if 'x_range' not in object_values or 'y_range' not in object_values:
                sys.exit("[ERROR] x_range and y_range must be defined when the initial position of a part/object is set to random")
            elif type(object_values['x_range']) != list or type(object_values['y_range']) != list:
                sys.exit("[ERROR] x_range and y_range must be lists")
            elif len(object_values['x_range']) != 2 or len(object_values['y_range']) != 2:
                sys.exit("[ERROR] x_range and y_range must be 2 in length")
            else:
                x = random.uniform(object_values['x_range'][0], object_values['x_range'][1])
                y = random.uniform(object_values['y_range'][0], object_values['y_range'][1])
                initial_position = (round(x, 2), round(y, 2))
        else:
            initial_position = object_values["initial_position"]

        if object_values["static"] is True:
            body = self.CreateStaticBody(position=initial_position,
                                         angle=angle)
        else:
            body = self.CreateDynamicBody(position=initial_position,
                                          angle=angle)

        if object_values["type"] == 'box':
            body.CreatePolygonFixture(box=object_values["box_size"],
                                      density=object_values["density"],
                                      friction=object_values["friction"])
        elif object_values["type"] == 'circle':
            body.CreateCircleFixture(radius=object_values["radius"],
                                     density=object_values["density"],
                                     friction=object_values["friction"])
        elif object_values["type"] == 'polygon':
            if type(object_values["vertices"]) == list:
                for v in object_values["vertices"]:
                    if type(v) != list or len(v) != 2:
                        print("[ERROR] Vertices list of a part must be a list of pairs")
                        sys.exit()
            else:
                print("[ERROR] Vertices list of a part must be a list of pairs")
                sys.exit()
            body.CreatePolygonFixture(vertices=object_values["vertices"],
                                      density=object_values["density"],
                                      friction=object_values["friction"])
        return body

    def create_joint(self, body_a, body_b, joint):
        if joint["type"] == "distance":
            distance_joint = load_default_values(self.distance_joint_name)
            fill_in_with_default(joint, distance_joint, self.distance_joint_keys)
            self.CreateDistanceJoint(
                bodyA=body_a,
                bodyB=body_b,
                anchorA=body_a.position + joint["anchor_a_offset"],
                anchorB=body_b.position + joint["anchor_b_offset"],
            )
        elif joint["type"] == "revolute":
            revolute_joint = load_default_values(self.revolute_joint_name)
            fill_in_with_default(joint, revolute_joint, self.revolute_joint_keys)
            self.CreateRevoluteJoint(
                bodyA=body_a,
                bodyB=body_b,
                localAnchorA=joint["anchor_a"],
                localAnchorB=joint["anchor_b"]
            )
        elif joint["type"] == "prismatic":
            prismatic_joint = load_default_values(self.prismatic_joint_name)
            fill_in_with_default(joint, prismatic_joint, self.prismatic_joint_keys)
            self.CreatePrismaticJoint(
                bodyA=body_a,
                bodyB=body_b,
                anchor=joint["anchor"],
                axis=joint["axis"],
                maxMotorForce=joint["max_motor_force"],
                enableMotor=joint["enable_motor"],
                motorSpeed=joint["motor_speed"],
                lowerTranslation=joint["lower_translation"],
                upperTranslation=joint["upper_translation"],
                enableLimit=joint["enable_limit"]
            )

        else:
            sys.exit("[ERROR] Unknown joint type: %s" % joint["type"])

        # if 'type' not in joint or 'connects' not in joint:
        #     sys.exit("[ERROR] Keys 'type' and 'connects' is mandatory for joint")
        # try:
        #     partA = parts[joint['connects'][0]]
        #     partB = parts[joint['connects'][1]]
        #
        #     if joint['type'] == 'distance':
        #         self.CreateDistanceJoint(
        #             bodyA=partA.body,
        #             bodyB=partB.body,
        #             anchorA=partA.body.position,
        #             anchorB=partB.body.position,
        #         )
        #     elif joint['type'] == 'revolute':
        #         if 'anchor_a' in joint:
        #             anchorA = joint['anchor_a']
        #         else:
        #             anchorA = (0, 0)
        #         if 'anchor_b' in joint:
        #             anchorB = joint['anchor_b']
        #         else:
        #             anchorB = (0, 0)
        #
        #         self.CreateRevoluteJoint(
        #             bodyA=partA.body,
        #             bodyB=partB.body,
        #             localAnchorA=anchorA,
        #             localAnchorB=anchorB
        #         )
        #
        #     elif joint['type'] == 'prismatic':
        #         self.CreatePrismaticJoint(
        #             bodyA=partA.body,
        #             bodyB=partB.body,
        #             anchor=(0, 5),
        #             axis=(3, 0),
        #             maxMotorForce=1000,
        #             enableMotor=True,
        #             lowerTranslation=-100,
        #             upperTranslation=100,
        #             enableLimit=True
        #         )
        #
        #     else:
        #         print("[WARNING] Unknown joint type '%s' - skipping" % joint['type'])
        #
        # except KeyError:
        #     sys.exit("[ERROR] joint (%s, %s) tries to connect parts that do not exist" % (partA, partB,))

    def step(self, target_fps):
        super().Step(1 / target_fps, 10, 10)
