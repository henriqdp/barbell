import sys

from .bodypart import BodyPart
from .utils import check_mandatory_keys


class Agent(object):
    name = "AGENT"
    parts_name = "PARTS"
    joints_name = "JOINTS"

    part_mandatory_keys = []

    joint_mandatory_keys = [
        'connects',
        'type'
    ]

    def __init__(self, environment, agent_structure):
        self.parts = {}

        if "PARTS" in agent_structure:
            self.initialize_parts(environment, agent_structure["PARTS"])
        else:
            sys.exit("[ERROR] No parts declared for the agent")

        if "JOINTS" in agent_structure:
            self.initialize_joints(environment, agent_structure["JOINTS"])
            self.joints_structure = agent_structure["JOINTS"]
        else:
            print("[WARNING] No joints declared for the agent")

    def initialize_parts(self, environment, parts):
        for part in parts:
            for part_name in part:
                if part_name in self.parts:
                    sys.exit("[ERROR] Part '%s' is being redefined, which may lead to unpredictable behavior" % part_name)
                self.parts[part_name] = BodyPart(environment, part_name, part[part_name])

    def initialize_joints(self, environment, joints):
        for i in range(0, len(joints)):
            check_mandatory_keys(self.joint_mandatory_keys, joints[i], "Joint #%d" % i)
            try:
                # check if agent has part_a
                if joints[i]["connects"][0] in self.parts:
                    body_a = self.parts[joints[i]["connects"][0]].body
                else:
                    body_a = environment.objects[joints[i]["connects"][0]]

                # check if agent has part_b
                if joints[i]["connects"][1] in self.parts:
                    body_b = self.parts[joints[i]["connects"][1]].body
                else:
                    body_b = environment.objects[joints[i]["connects"][1]]

            except KeyError:
                sys.exit("[ERROR] Joint #%d is trying to connect nonexistant parts" % i)

            environment.create_joint(body_a, body_b, joints[i])

    def reset(self, environment):
        for part in self.parts:
            self.parts[part].reset(environment)
        self.initialize_joints(environment, self.joints_structure)
