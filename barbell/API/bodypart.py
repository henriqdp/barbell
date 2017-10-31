import sys

from .utils import load_default_values, fill_in_with_default


class BodyPart(object):
    keys = [
        'density',
        'friction',
        'initial_position',
        'angle',
        'color',
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

        # create part's body
        dynamic_body = world.CreateDynamicBody(position=part_values["initial_position"],
                                               angle=part_values["angle"])

        if self.type == 'box':
            dynamic_body.CreatePolygonFixture(box=part_values["box_size"],
                                              density=part_values["density"],
                                              friction=part_values["friction"])
        elif self.type == 'circle':
            dynamic_body.CreateCircleFixture(radius=part_values["radius"],
                                             density=part_values["density"],
                                             friction=part_values["friction"])

        self.body = dynamic_body

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
