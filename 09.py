def solve(fname):
    with open(fname,'r') as f:
        lines = f.readlines()

    grid = [ [int(c) for c in line.strip()] for line in lines]
    sum_risk = 0

    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            if (x==0 or row[x-1] > v) and \
               (x==len(row)-1 or row[x+1] > v) and \
               (y==0 or grid[y-1][x] > v) and \
               (y==len(grid)-1 or grid[y+1][x] > v):
                   #print(x,y,v)
                   sum_risk += v + 1

    print(sum_risk)
    
    visited = set()
    basins = []
    sizex = len(grid[0])
    sizey = len(grid)
    for x in range(sizex):
        for y in range(sizey):
            if (x,y) not in visited:
                basins.append( visit(x,y, visited, grid) )

    basins.sort()
    print(basins[-1] * basins[-2] * basins[-3])

def visit(x,y, visited, grid):
    if (x,y) in visited:
        return 0
    visited.add((x,y))
    if grid[y][x] == 9: return 0

    basin_size = 1 # this square
    if x>0:
        basin_size += visit(x-1, y, visited, grid)
    if x<len(grid[y])-1:
        basin_size += visit(x+1, y, visited, grid)
    if y>0:
        basin_size += visit(x, y-1, visited, grid)
    if y<len(grid)-1:
        basin_size += visit(x, y+1, visited, grid)

    return basin_size


solve("09.test")
solve("09.dat")
