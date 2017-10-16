from .utils import load_default_values, fill_in_with_default


class BodyPart(object):
    keys = [
        'density',
        'friction',
        'initial_position',
        'name',
        'angle',
        'color'
    ]

    mandatory_keys = [
        'initial_position',
        'name'
    ]

    def __init__(self, world, part_values):
        self.check_mandatory_values(part_values)

        default_values = load_default_values("PART")
        part_values = fill_in_with_default(part_values, default_values, self.keys)

        dynamic_body = world.CreateDynamicBody(position=part_values["initial_position"], angle=part_values["angle"])
        dynamic_body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)
        self.body = dynamic_body
        self.color = part_values["color"]

    def check_mandatory_values(self, part_values):
        # TODO
        return True
