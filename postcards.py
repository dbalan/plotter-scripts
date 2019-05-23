import math
import random
from collections import namedtuple

import numpy as np

import common
from corridors import hallygon
from polygons import circle

Point = namedtuple("Point", ("x", "y"))


def dist(p1, p2):
    """Finds distance between two Points"""
    return math.sqrt((p1.x - p2.x) ** 2
                     + (p1.y - p2.y) ** 2)


def overlap(prev_list, center, radius):
    """Compares center and radius and determines if there is overlap
    with any center and radius in prev_list"""
    for prev_center, prev_radius in prev_list:
        if dist(prev_center, center) < prev_radius + radius:
            return True
    return False


if __name__ == "__main__":
    port = "/dev/ttyUSB0"
    speed = 9600

    hallways = []
    DEFAULT_SIZE = 1000 / math.sqrt(2)
    DEV = 200
    size = DEFAULT_SIZE
    spacing = size * math.sqrt(2)
    margin = size + DEV

    deviation_x = np.linspace(-DEV, DEV, 5)
    deviation_y = np.linspace(-DEV, DEV, 3)
    for x, dev_x in enumerate(deviation_x):
        for y, dev_y in enumerate(deviation_y):
            cx = margin + x * spacing
            cy = margin + y * spacing

            hallways.extend(hallygon(cx, cy, size, 4,
                                     dev_x, dev_y, 100,
                                     random.randint(0, 90), steps=10))

    polygons = []
    previous = []
    low_left = Point(DEV + 207, 3800)
    up_right = Point(5400, 7300)
    while len(previous) < 200:
        rad = random.randint(50, 250)
        center = Point(random.randint(low_left.x + rad, up_right.x - rad),
                       random.randint(low_left.y + rad, up_right.y - rad))
        if not overlap(previous, center, rad):
            sides = random.randint(3, 9)
            rot = random.randint(0, 360)
            previous.append((center, rad))
            polygons.extend(circle(center, rad,
                                   rotation=rot,
                                   arc=360.0 / sides))

    common.exec_hpgl(hallways + polygons, port=port, speed=speed)
