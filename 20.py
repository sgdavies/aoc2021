#!/usr/bin/python
import functools, sys
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

if len(sys.argv) > 2:
    steps = int(sys.argv[2])
else:
    steps = 2

key = [0 if c=='.' else 1 for c in lines.pop(0).strip()]
lines.pop(0) # Blank line

minx = 0
miny = 0
maxx = len(lines[0].strip())
maxy = len(lines)

grid = {}

for y,line in enumerate(lines):
    for x,c in enumerate(line.strip()):
        grid[(x,y)] = 0 if c=='.' else 1 if c=='#' else exit(1)

print(sum(grid.values()))

for i in range(steps):
    new_grid = {}
    for x in range(minx-1, maxx+1):
        for y in range(miny-1, maxy+1):
            if key[0]: g = i%2
            else: g = 0
            
            bits = [g,g,g,g,g,g,g,g,g]
            if (x-1,y-1) in grid: bits[8] = grid[(x-1,y-1)]
            if (x  ,y-1) in grid: bits[7] = grid[(x  ,y-1)]
            if (x+1,y-1) in grid: bits[6] = grid[(x+1,y-1)]
            if (x-1,y  ) in grid: bits[5] = grid[(x-1,y  )]
            if (x  ,y  ) in grid: bits[4] = grid[(x  ,y  )]
            if (x+1,y  ) in grid: bits[3] = grid[(x+1,y  )]
            if (x-1,y+1) in grid: bits[2] = grid[(x-1,y+1)]
            if (x  ,y+1) in grid: bits[1] = grid[(x  ,y+1)]
            if (x+1,y+1) in grid: bits[0] = grid[(x+1,y+1)]

            val = functools.reduce(lambda acc, iv: acc + iv[1]*(2**iv[0]), enumerate(bits), 0)
            val = key[val]

            new_grid[(x,y)] = val

    minx -=1
    maxx +=1
    miny -=1
    maxy +=1

    grid = new_grid
    if False: # print grid
        print()
        print("x(%d,%d) y(%d,%d) g %d" %(minx+1,maxx-1,miny+1,maxy-1,g))
        for y in range(miny-1, maxy+1):
            print("".join([ 'O' if (x,y)==(0,0) and grid[(0,0)] else 'o' if (x,y)==(0,0) else '.' if (x,y) not in grid else '#' if grid[(x,y)] else '.' for x in range(minx-1,maxx+1) ]))

print(sum(grid.values()))
