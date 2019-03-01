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

port = "/dev/cuaU0"
speed = 9600

with serial.Serial(port, speed, timeout=1) as plt:
    plt.write("IN;PU;SP1;")
    for i in range(100):
        body = random_square()
        for line in body:
            plt.write(line)
            print(plt.readlines())
            time.sleep(.5)
    plt.write("SP0;")

