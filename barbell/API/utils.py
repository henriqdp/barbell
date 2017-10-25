import yaml
import os


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
            values[key] = default_values[key]
    return values


def coord_box2d_to_pygame(body, screen, shape):
    vertices = [(body.transform * v) * screen.values["ppm"] for v in shape.vertices]
    vertices = [(v[0], screen.values["height"] - v[1]) for v in vertices]
    return vertices


def get_circle_coordinates(body, screen, shape):
    ppm = screen.values["ppm"]
    circle_coords = body.transform * shape.pos * ppm
    circle_coords = (circle_coords[0],
                     screen.values["height"] - circle_coords[1],
                     shape.radius * ppm)

    return circle_coords
