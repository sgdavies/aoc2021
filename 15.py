#!/usr/bin/python
import sys
with open(sys.argv[1]) as f:
    mapp = f.readlines()

width = len(mapp[0].strip())
depth = len(mapp)

def solve(tiles):
    TILES = tiles 
    costs = { (0,0): 0 }
    active = set([(0,0)])

    while active:
        nx,ny = active.pop()
        linked_nodes = [(nx-1,ny),(nx+1,ny),(nx,ny-1),(nx,ny+1)]
        for node in linked_nodes:
            x,y = node
            if x<0 or x>=TILES*width or y<0 or y>=TILES*depth: continue

            map_x = x%width
            wrap_x = x//width
            map_y = y%depth
            wrap_y = y//depth
            enter_cost = int(mapp[map_y][map_x]) + wrap_x + wrap_y
            if enter_cost > 9: enter_cost -= 9
            new_cost = costs[(nx,ny)] + enter_cost
            #old_cost = costs.get((x,y))  ## slower that `x not in d or d[x]`
            if (x,y) not in costs or new_cost < costs[(x,y)]:
                costs[(x,y)] = new_cost
                active.add((x,y))

    return costs[(TILES*width-1, TILES*depth-1)]

print(solve(1))

if len(sys.argv) > 2 and sys.argv[2] == "--profile":
    import cProfile
    cProfile.run("print(part_two())")
else:
    print(solve(5))
