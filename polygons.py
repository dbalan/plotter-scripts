import math
import random
from collections import namedtuple

import numpy as np

from common import write_hpgl

Point = namedtuple("Point", ("x", "y"))
PI = math.pi


def circle_points(center, radius, rotation=0, arc=5):
    """Generates 360/arc points on the circumference of a circle"""
    steps = int(360.0 / arc) + 1
    for deg in np.linspace(0 + rotation, 360 + rotation, steps):
        yield Point(int(center.x + radius * math.cos(deg * 2 * PI / 360)),
                    int(center.y + radius * math.sin(deg * 2 * PI / 360)))


def circle(center, radius, rotation=0, arc=5):
    current = circle_points(center, radius, rotation=rotation, arc=arc)
    instructions = []

    first = next(current)
    instructions.append("PA{},{};".format(first.x, first.y))

    for (x, y) in current:
        instructions.append("PD{},{};".format(x, y))

    instructions.append("PD{},{};".format(first.x, first.y))
    instructions.append("PU;")
    return instructions


def square(center, size, rotation=45):
    """Draws square centered at (cx, cy) with side length size"""
    return circle(center, size / math.sqrt(2), rotation=rotation, arc=90)


def random_circle(bound_x, bound_y):
    """Returns hpgl instructions for random circle within the given bounds"""
    radius = random.randint(100, 1000)
    x = random.randint(500 + radius, bound_x - radius)
    y = random.randint(500 + radius, bound_y - radius)
    center = Point(x, y)
    steps = 360.0 / random.randint(3, 12)
    return circle(center, radius, arc=steps)


if __name__ == "__main__":
    port = "/dev/ttyUSB0"
    speed = 9600

    instructions = []
    for i in range(50):
        instructions.extend(random_circle(10000, 7200))

    write_hpgl(instructions, "images/polygons.hpgl")
