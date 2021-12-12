#!/usr/bin/python
import sys

with open(sys.argv[1], "r") as f:
    lines = f.readlines()

octopodes = {}
for y, line in enumerate(lines):
    for x, c in enumerate(line.strip()):
        octopodes[(x,y)] = int(c)

steps = int(sys.argv[2])
flashes = 0
step = 1
while True:
    new_flashes = 0
    flashed = set()
    to_flash = set()
    for k,v in octopodes.items():
        v += 1
        if v>9: to_flash.add(k)
        octopodes[k] = v

    while to_flash:
        o = to_flash.pop()
        flashed.add(o)
        new_flashes += 1
        surrounding = [ (o[0]-1, o[1]-1),
                        (o[0]-1, o[1])  ,
                        (o[0]-1, o[1]+1),
                        (o[0]  , o[1]-1),
                        (o[0]  , o[1]+1),
                        (o[0]+1, o[1]-1),
                        (o[0]+1, o[1])  ,
                        (o[0]+1, o[1]+1) ]
        for no in surrounding:
            if no in octopodes:  # ignore outside the edge!
                if no not in flashed:
                    octopodes[no] += 1
                    if octopodes[no] > 9: to_flash.add(no)  # noop if already there

    for o in flashed:
        octopodes[o] = 0

    if new_flashes == len(octopodes):
        print(step)
        exit(0)

    flashes += new_flashes
    if step == steps:
        print(flashes)

    step += 1
