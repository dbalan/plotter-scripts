import time
import numpy as np
import random
import serial
import math

def circle_points(cx, cy, radius, rotation=0, arc=5):
    """Generates 360/arc points on the circumference of a circle"""
    steps = int(360.0 / arc) + 1
    for deg in np.linspace(0 + rotation, 360 + rotation, steps):
        yield (int(cx + radius * math.cos(deg * 2 * math.pi / 360)),
               int(cy + radius * math.sin(deg * 2 * math.pi / 360)))

def circle(cx, cy, radius, rotation=0, arc=5):
    current = circle_points(cx, cy, radius, rotation=rotation, arc=arc)
    instructions = []

    (first_x, first_y) = next(current)
    instructions.append("PA{},{};".format(first_x, first_y))
    for (x, y) in current:
        instructions.append("PD{},{};".format(x, y))

    instructions.append("PD{},{};".format(first_x, first_y))
    instructions.append("PU;")
    return instructions

def square(cx, cy, radius, rotation=45):
    """Draws square centered at (cx, cy) with side length sqrt(2)* radius"""
    return circle(cx, cy, radius, rotation=rotation, arc=90)

def hallway(cx, cy, radius, disp_x, disp_y, end_rad, end_rot = 45, steps=15):
    """Draws steps number of squares interpolated between start and end"""
    instructions = []
    x_series = np.geomspace(cx, cx + disp_x, steps)
    y_series = np.geomspace(cy, cy + disp_y, steps)
    rad_series = np.geomspace(radius, end_rad, steps)
    rot_series = np.linspace(45, end_rot, steps)

    for (x, y, rad, rot) in zip(x_series, y_series, rad_series, rot_series):
        instructions.extend(square(x, y, rad, rotation=rot))

    return instructions

port = "/dev/ttyUSB0"
speed = 9600

with serial.Serial(port, speed, timeout=None) as plt:
#with open("hallway.hpgl", "w")  as plt:
    #send initialization instructions
    plt.write("IN;PU;SP1;")

    deviation = (-300, -100, 0, 100, 300)
    rotation = (0, 29, 45, 78, 120)
    spacing = 1500
    for x, dev in enumerate(deviation):
        for y, rot in enumerate(rotation):
            figure = hallway(750 + y * spacing, 750 + x * spacing, 1000, 
                             -dev, dev, 250,
                             end_rot = rot)
            for line in figure:
                plt.write(line)
                
                #send a blocking isnstruction, to know when pen has stopped
                plt.write("OA;")
                c = ""
                while c != "\r":
                    c = plt.read()

    #Finally, put back the pen
    plt.write("SP0;")
