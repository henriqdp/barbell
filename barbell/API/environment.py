import sys

from Box2D import b2World
from Box2D.b2 import (polygonShape)

from .utils import load_default_values, fill_in_with_default


class Environment(b2World):
    name = "ENVIRONMENT"
    floor_name = "FLOOR"
    joint_name = "JOINT"

    keys = [
        'gravity',
        'do_sleep',
        'floor',
        'objects_color',
    ]

    joint_keys = [
        'anchor_a',
        'anchor_b',
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

    def create_joint(self, part_a, part_b, joint):
        default_joint = load_default_values(self.joint_name)
        fill_in_with_default(joint, default_joint, self.joint_keys)
        if joint["type"] == "distance":
            self.CreateDistanceJoint(
                bodyA=part_a.body,
                bodyB=part_b.body,
                anchorA=part_a.body.position,
                anchorB=part_b.body.position
            )
        elif joint["type"] == "revolute":
            self.CreateRevoluteJoint(
                bodyA=part_a.body,
                bodyB=part_b.body,
                localAnchorA=joint["anchor_a"],
                localAnchorB=joint["anchor_b"]
            )
        elif joint["type"] == "prismatic":
            self.CreatePrismaticJoint(
                bodyA=part_a.body,
                bodyB=part_b.body,
                anchor=(0, 5),
                axis=(3, 0),
                maxMotorForce=1000,
                enableMotor=True,
                lowerTranslation=-100,
                upperTranslation=100,
                enableLimit=True
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
