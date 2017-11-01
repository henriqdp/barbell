from .bodypart import BodyPart
from .screen import Screen
from .world import World


class Barbell(object):
    def __init__(self, structure):
        # load SCREEN into Barbell
        if "SCREEN" in structure:
            self.initialize_screen(structure["SCREEN"])
        else:
            self.initialize_screen({})
            print("[WARNING] section 'SCREEN' not declared, loading default values")

        # load WORLD into Barbell
        if "WORLD" in structure:
            self.create_world(structure["WORLD"])
        else:
            self.create_world({})
            print("[WARNING] section 'WORLD' not declared, loading default values")

        # load PARTS into Barbell
        self.parts = {}
        if "PARTS" in structure:
            self.create_parts(structure["PARTS"])
        else:
            print("[WARNING] section 'PARTS' not declared, your agent simply does not exist. Is that what you wanted to achieve?")

        self.running = True
        self.events = []

        if "JOINTS" in structure:
            self.create_joints(structure["JOINTS"])
        else:
            print("[WARNING] no joints declared")

    def initialize_screen(self, screen_structure):
        self.screen = Screen(screen_structure)

    def create_world(self, world_structure):
        self.world = World(world_structure, self.screen)

    def create_parts(self, parts_structure):
        for part_structure in parts_structure:
            for part_name in part_structure:
                new_part = BodyPart(self.world, part_name, part_structure[part_name])
                if new_part.name in self.parts:
                    print("[WARNING] '%s' is being redefined, which may lead to unpredictable behavior" % new_part.name)
                self.parts[new_part.name] = new_part

    def create_joints(self, joints_structure):
        for joint in joints_structure:
            self.world.create_joint(self.parts, joint)

    def reset(self):
            for part in self.parts:
                self.parts[part].reset(self.world)

    def step(self):
        events = self.screen.check_events()
        if 'exit' in events:
            self.running = False
        self.events = events
        self.screen.update(self.world, self.parts)

    def get_events(self):
        return self.screen.check_events()
