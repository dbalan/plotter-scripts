import serial

# combine command together with maxlen buflen and expose as an iterator
def stitch(body, buflen=40):
    start = ["IN;PU;", "SP1;"]
    end = ["SP0;"]
    final = start + body + end

    ## read in 20 bytes at a time or boundary
    count = 0
    buf = []
    for ins in final:
        if count + len(ins) >= buflen:
            yield "".join(buf)
            buf = []
            count = len(ins)
        else:
            count += len(ins)
        buf.append(ins)

    # send rest of the code
    yield "".join(buf)

# cmds is a list with semicolon attached to the command
def exec_hpgl(cmds):
    port = "/dev/cuaU0"
    speed = 9600

    body = stitch(cmds)
    with serial.Serial(port, speed, timeout=None) as plt:
        for ins in body:
            # TODO: we can sent more commands at one, to be exact, bufferlen
            # size (Esc-B) returns bufferlen
            plt.write(ins)
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

