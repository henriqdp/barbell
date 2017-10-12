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
