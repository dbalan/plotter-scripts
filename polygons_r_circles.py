import time
import numpy as np
import random
import serial
import math

MARGIN = 100

def circle_points(cx, cy, radius, arc=5):
    """Generates 360/arc points on the circumference of a circle"""
    steps = int(360.0 / arc) + 1
    for deg in np.linspace(0, 360, steps):
        yield (int(cx + radius * math.cos(deg * 2 * math.pi / 360)),
               int(cy + radius * math.sin(deg * 2 * math.pi / 360)))

def circle(cx, cy, radius, arc=5):
    current = circle_points(cx, cy, radius, arc=arc)

    instructions = []

    (first_x, first_y) = next(current)
    instructions.append("PA{},{};".format(first_x, first_y))

    for (x, y) in current:
        instructions.append("PD{},{};".format(x, y))

    instructions.append("PD{},{};".format(first_x, first_y))
    instructions.append("PU;")
    return instructions

def random_circle(bound_x, bound_y):
    """Returns hpgl intructions for random circle within the given bounds"""
    radius = random.randint(100,1000)
    cx = random.randint(MARGIN, bound_x - radius)
    cy = random.randint(MARGIN, bound_y - radius)
    steps = 360.0 / random.randint(3,12)
    return circle(cx, cy, radius, arc = steps)

if __name__ == "__main__":
    port = "/dev/ttyUSB0"
    speed = 9600

    with serial.Serial(port, speed, timeout=None) as plt:
        #send initialization instructions
        plt.write("IN;PU;SP1;")

        for i in range(50):
            figure = random_circle(10000, 7200)
            for line in figure:
                plt.write(line)
                
                #send a blocking isnstruction, to know when pen has stopped
                plt.write("OA;")
                c = ""
                while c != "\r":
                    c = plt.read()

        #Finally, put back the pen
        plt.write("SP0;")
