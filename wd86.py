import numpy as np
import math
import random
from collections import namedtuple
from common import exec_hpgl, write_hpgl
from bday import text

Point = namedtuple("Point", ("x", "y"))
PI = math.pi

def line(center, length, rotation=0):
    """Returns hpgl instructions for line centered at center with given
    length and rotation in degrees"""
    unit = np.array([math.cos(rotation * 2*PI / 360), 
                     math.sin(rotation * 2*PI / 360)])
    end = center + unit * length / 2
    start = center - unit * length / 2    
    return ["PA{},{};".format(*[int(coord) for coord in start]),
            "PD{},{};".format(*[int(coord) for coord in end]),
            "PU;"]

def random_line(bound_x, bound_y, length):
    """Returns hpgl intructions for random line within bounds"""
    x = random.randint(200 + length, bound_x - length)
    y = random.randint(200 + length, bound_y - length)
    center = np.array([x, y])
    rotation = random.randint(0, 360)
    return line(center, length, rotation=rotation)

if __name__ == "__main__":
    port = "/dev/ttyUSB0"
    speed = 9600
    
    instructions = ["SP2;"]
    instructions.extend(text("Wall Drawing #86", 200, 200))
    instructions.append("SP1;")
    for i in range(1000):
        instructions.extend(random_line(10100, 7600, 250))

    write_hpgl(instructions, "images/wd86.hpgl")
    #exec_hpgl(instructions) 
