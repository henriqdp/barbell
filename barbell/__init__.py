import sys

import Box2D  # NOQA
import pygame  # NOQA
import yaml

from .API import Barbell


def from_file(filename=None):
    if filename:
        with open(filename, 'r') as raw_data:
            data = yaml.load(raw_data)
            barbell = Barbell(data)
            return barbell
    else:
        sys.exit('[ERROR] a filename must be informed')
