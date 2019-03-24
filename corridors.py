import time
import numpy as np
import random
import serial
import math

import common
from bday import text
from polygons_r_circles import circle_points, circle

def hallygon(cx, cy, radius, sides, disp_x, disp_y, end_rad, end_rot, steps = 15):
    """Draws steps number of squares interpolated between start and end"""
    instructions = []
    x_series = np.geomspace(cx, cx + disp_x, steps)
    y_series = np.geomspace(cy, cy + disp_y, steps)
    rad_series = np.geomspace(radius, end_rad, steps)
    rot_series = np.linspace(45, end_rot, steps)

    for (x, y, rad, rot) in zip(x_series, y_series, rad_series, rot_series):
        instructions.extend(circle(x, y, rad, rotation=rot, arc = 360/sides))

    return instructions

def is_prime(num):
    """Tests if num is prime"""
    if num == 0 or num == 1:
        return False
    bound = int(math.sqrt(num)) + 1

    for i in range(2, num + 1):
        for j in range(2, bound):
            if i * j == num:
                return False
    return True

if __name__ == "__main__":
    port = "/dev/ttyUSB0"
    speed = 9600
    instructions = []

    DEFAULT_SIZE = 575
    DEV = 250
    size = DEFAULT_SIZE
    spacing = size/(math.sqrt(2))
    margin = size + DEV
    instructions.extend(text("hallygons", size - 200, size - 200))
    deviation_x = np.linspace(-DEV, DEV, 23)
    deviation_y = np.linspace(-DEV, DEV, 14)
    for x, dev_x in enumerate(deviation_x):
        for y, dev_y in enumerate(deviation_y):
            cx = margin + x * spacing
            cy = margin + y * spacing

            if is_prime(x + 1) and is_prime(y + 1):
                sides = max([x + 1, y + 1])
                instructions.append("SP2;")
                size = size / math.sqrt(2)
                rot = (360 / (sides / math.pi))
            else:
                sides = 4
                instructions.append("SP1;")
                size = DEFAULT_SIZE
                rot = 157.5

            instructions.extend(hallygon(cx, cy, size, sides,
                                         dev_x, dev_y, 60,
                                         end_rot = rot, steps = 4))

    common.exec_hpgl(instructions, port=port, speed=speed)
    #common.write_hpgl(instructions, "hallway.hpgl")
