import serial
import random
import numpy as np
import math 

from common import stitch, exec_hpgl 
from polygons_r_circles import circle, circle_points

CHAR_WIDTH = 100

def random_nonoverlap_circle(outer_bounds, inner_bounds):
    """Returns hpgl intructions for random circle within the given bounds"""
    (low_left_x, low_left_y, up_right_x, up_right_y) = outer_bounds
    (inner_low_x, inner_low_y, inner_high_x, inner_high_y) = inner_bounds
    instructions = dot_bound(*outer_bounds)
    instructions = dot_bound(*inner_bounds)

    radius = random.randint(100, 400)

    #if circle will overlap with text, shift right
    cx = random.randint(low_left_x + radius, up_right_x - radius)
    cy = random.randint(low_left_y + radius, up_right_y - radius)
    while inner_low_x - radius < cx < inner_high_x + radius and \
          inner_low_y - radius < cy < inner_high_y + radius:
        cx = random.randint(low_left_x + radius, up_right_x - radius)
        cy = random.randint(low_left_y + radius, up_right_y - radius)

    steps = 360.0 / random.randint(3,13)
    return circle(cx, cy, radius, arc = steps)

def text(label, posx, posy):
    """Returns list of commands to draw text at (posx, posy)"""
    return ["PU;",
            "PA{},{}".format(posx, posy),
            "LB{}\3;".format(label)]

def centered_text(label, low_x, high_x, pos_y):
    """Centers given string at pos_y on the page between low_x and high_x"""
    text_width = len(label) * CHAR_WIDTH
    area_center = low_x + ((high_x - low_x) / 2)
    start_x = area_center - (text_width / 2)
    return text(label, int(start_x), pos_y)

def dot_bound(low_left_x, low_left_y, up_right_x, up_right_y):
    """Places dots at the corners of the speficied rectangle"""
    coords = [(low_left_x, low_left_y),
              (up_right_x, low_left_y),
              (low_left_x, up_right_y),
              (up_right_x, up_right_y)]
    instructions = []
    for (x, y) in coords:
        instructions.extend(["PU{},{};PD;".format(x,y)])
    instructions.append("PU;")
    return instructions

if __name__ == "__main__":
    cmds = []
    mess = "Happy Birthday!"
    card_bounds = (500, 500, 5500, 7500)
    #demarcate edges of card
    cmds.extend(dot_bound(*card_bounds))
    #start writing text in a different color
    cmds.extend(["SP2;"])
    cmds.extend(centered_text(mess, 500, 5500, 6000))
    cmds.extend(centered_text("People", 500, 5500, 6000 - 2*CHAR_WIDTH))
    #Just bad magic numbers I figured out once that worked
    text_bounds = (2150 - CHAR_WIDTH, 
                  6000 - 3*CHAR_WIDTH, 
                  2150 + (CHAR_WIDTH * (len(mess) + 4)), 
                  6000 + (2 * CHAR_WIDTH) )
    #useful debugging of text bounds
    #cmds.extend(dot_bound(*text_bounds))
    cmds.extend(["SP1;"])

    for i in range(50):
        current_circle = random_nonoverlap_circle(card_bounds, text_bounds)
        print(current_circle)
        cmds.extend(current_circle)

    exec_hpgl(cmds)
