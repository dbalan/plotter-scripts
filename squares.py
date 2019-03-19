# draws random squares, using PEN1
import time
import random
import serial

def rect(start_x, start_y, length, breadth):
    coords = [(start_x+length, start_y),
              (start_x+length, start_y+breadth),
              (start_x, start_y+breadth),
              (start_x, start_y)]

    instructions = []
    instructions.append("PA{},{};".format(start_x, start_y))
    for (x, y) in coords:
        instructions.append("PD{},{};".format(x,y))
    instructions.append("PU;")
    return instructions

def square(x, y, size):
    return rect(x, y, size, size)

def random_square():
    bound_x = 10000
    bound_y = 7000
    size = random.randint(200,1000)
    x = random.randint(100, bound_x - (size + 2) )
    y = random.randint(200, bound_y - (size + 2) )
    return square(x, y, size)

def execute(body):
    start = ["IN;PU;", "SP1;"]
    end = ["SP0;"]
    return start + body + end


port = "/dev/cuaU0"
speed = 9600

with serial.Serial(port, speed, timeout=None) as plt:
    plt.write("IN;PU;SP1;")
    for i in range(100):
        body = random_square()
        for line in body:
            # TODO: we can sent more commands at one, to be exact, bufferlen
            # size (Esc-B) returns bufferlen
            plt.write(line)
            # For every line sent, end with OA, which reports back current
            # position on the pen
            plt.write("OA;")
            c = ""
            data = ""
            while c != '\r':
                c = plt.read()
                data += c
                print("read: {}".format(map(ord, c)))
            print("OA return: {}".format(data))
            # We got data, mean OA got executed, so the instruction buffer
            # is all consumed, ready to sent more.
    plt.write("SP0;")
