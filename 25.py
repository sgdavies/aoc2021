#!/usr/bin/python
import sys
with open(sys.argv[1]) as f:
    lines = f.readlines()

grid = {}
MAX_X = len(lines[0].strip())
MAX_Y = len(lines)

DOWN = 'v'
LEFT = '>'

for y, line in enumerate(lines):
    for x, c in enumerate(line.strip()):
        if c != '.': grid[(x,y)] = c

def show_grid(g):
    for y in range(MAX_Y):
        s=""
        for x in range(MAX_X):
            if (x,y) in g: s+= g[(x,y)]
            else: s += "."
        print(s)
    print()

steps = 0
while True:
    #show_grid(grid)
    moved = False
    new_grid = {}
    for k,v in grid.items():
        if v==LEFT:
            x,y = k
            nx = (x+1)%MAX_X
            if (nx,y) not in grid:
                new_grid[(nx,y)] = v
                moved = True
            else:
                new_grid[(x,y)] = v
        elif v==DOWN:
            new_grid[k] = v
        else:
            assert(False)
    grid = new_grid
    new_grid = {}
    for k,v in grid.items():
        if v==DOWN:
            x,y = k
            ny = (y+1)%MAX_Y
            if (x,ny) not in grid:
                new_grid[(x,ny)] = v
                moved = True
            else:
                new_grid[(x,y)] = v
        elif v==LEFT:
            new_grid[k] = v
        else:
            assert(False)

    grid = new_grid
    steps += 1
    if not moved: break

print(steps)
