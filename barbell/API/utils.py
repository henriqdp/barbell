import os
import sys
import math
import yaml


def check_mandatory_keys(keys, structure, structure_name):
    for key in keys:
        if key not in structure:
            sys.exit("[ERROR] Missing key '%s' in structure '%s'" % (key, structure_name,))


def load_default_values(section=None):
    cwd = os.path.dirname(__file__)
    with open(os.path.join(cwd, 'assets/default_values.yaml'), 'r') as default_values:
            if section is None:
                return yaml.load(default_values)
            else:
                return yaml.load(default_values)[section]


def fill_in_with_default(values, default_values, keys):
    for key in keys:
        if key not in values:
            if key not in default_values and key not in values:
                sys.exit("Missing key: %s" % key)
            else:
                values[key] = default_values[key]
    return values


def deg_to_rad(degrees):
    return (degrees * math.pi) / 180


def vertices_box2d_to_pygame(body, screen, shape):
    vertices = [(body.transform * v) * screen.values["ppm"] for v in shape.vertices]
    vertices = [(v[0], screen.get_pygame_screensize()[1] - v[1]) for v in vertices]
    return vertices


def coord_box2d_to_pygame(coord, screen):
    coords = (coord[0] * screen.values["ppm"],
              screen.get_pygame_screensize()[1] - coord[1] * screen.values["ppm"])
    return coords


def get_circle_coordinates(body, screen, shape):
    ppm = screen.values["ppm"]
    circle_coords = body.transform * shape.pos * ppm
    circle_coords = (circle_coords[0],
                     screen.get_pygame_screensize()[1] - circle_coords[1],
                     shape.radius * ppm)

    return circle_coords
