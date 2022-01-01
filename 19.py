#!/usr/bin/python
import sys
from functools import reduce
try:
    from tqdm import tqdm
except:
    print("Install the tqdm module to get a progress bar!")
    def tqdm(x):
        return x

PREAMBLE = "--- scanner "
MUST_MATCH = 12 # 12

class Scanner:
    def __init__(self, id: int):
        self.id = id
        self.location = None
        self.beacons = set()

    def add_beacon(self, x, y, z):
        self.beacons.add((x,y,z))

    def orientation_funcs():
        return [ # Rotations if facing +x
                 lambda p: p,
                 lambda p: (p[0], -p[2], p[1]),
                 lambda p: (p[0], -p[1], -p[2]),
                 lambda p: (p[0], p[2], -p[1]),
                 # Rotations if facing +y
                 lambda p: (-p[1], p[0], p[2]),
                 lambda p: (-p[2], p[0], -p[1]),
                 lambda p: (p[1], p[0], -p[2]),
                 lambda p: (p[2], p[0], p[1]),
                 # Rotations if facing +z
                 lambda p: (-p[2], p[1], p[0]),
                 lambda p: (-p[1], -p[2], p[0]),
                 lambda p: (p[2], -p[1], p[0]),
                 lambda p: (p[1], p[2], p[0]),
                 # Rotations if facing -x
                 lambda p: (-p[0], p[1], -p[2]),
                 lambda p: (-p[0], p[2], p[1]),
                 lambda p: (-p[0], -p[1], p[2]),
                 lambda p: (-p[0], -p[2], -p[1]),
                 # Rotations if facing -y
                 lambda p: (p[1], -p[0], p[2]),
                 lambda p: (-p[2], -p[0], p[1]),
                 lambda p: (-p[1], -p[0], -p[2]),
                 lambda p: (p[2], -p[0], -p[1]),
                 # Rotations if facing -z
                 lambda p: (p[2], p[1], -p[0]),
                 lambda p: (p[1], -p[2], -p[0]),
                 lambda p: (-p[2], -p[1], -p[0]),
                 lambda p: (-p[1], p[2], -p[0]),
                ]

with open(sys.argv[1]) as f:
    lines = f.readlines()

scanners = []

for line in lines:
    line = line.strip()
    if line.startswith(PREAMBLE):
        scanner = Scanner(int(line[len(PREAMBLE):].split(" ")[0]))
    elif line == "":
        scanners.append(scanner)
    else:
        x,y,z = [int(w) for w in line.split(',')]
        scanner.add_beacon(x,y,z)
scanners.append(scanner) # close out the last one

scanners[0].location = (0,0,0)
scanners_to_process = { scanners[0] }

print(len(scanners))
for _ in tqdm(scanners):
    # It's a hack - but the bulk of the work here happens at most once per located scanner, 
    # and we expect to do that work for each scanner (except the last one, and others if we're lucky)
    if not scanners_to_process:
        # We've solved them all
        break

    scanner_a = scanners_to_process.pop()
    assert scanner_a.location is not None # otherwise it shouldn't be in the process list
    # Attempt to fix all scanners which overlap with this solved one.
    for scanner_b in scanners:
        if scanner_b == scanner_a or scanner_b.location is not None:
            continue

        # We have a solved scanner A, and another, B, which may or may not overlap.
        for f in Scanner.orientation_funcs():
            solved = False
            b_beacons = set(map(f, scanner_b.beacons))
            for beac_a in scanner_a.beacons: ## Could stop 12 before end?
                for beac_b in b_beacons:
                    # Assume beac_a is the same as beac_b and use that to fix the x,y,z offsets for B
                    # Then iterate over the others and see how many match up with A's beacons
                    (x,y,z) = (beac_a[0]-beac_b[0], beac_a[1]-beac_b[1], beac_a[2]-beac_b[2])
                    moved_beacons = set(map(lambda p: (p[0]+x,p[1]+y,p[2]+z), b_beacons))
                        
                    if len(scanner_a.beacons.intersection(moved_beacons)) >= MUST_MATCH:
                        solved = True

                    if solved: break # we found the beac_b that corresponds to beac_a
                if solved: break # we found a beac_a that matches a beacon in scanner_b
            if solved: break # we found an orientation func which gets 12+ matches between the two scanners

        # We've tried up to all beacon-beacon combos at all orientations (or quit early with a solution)
        if solved:
            #print("Solved", scanner_a.id, scanner_b.id, "(",x,y,z,")")
            scanner_b.beacons = moved_beacons
            scanner_b.location = (x,y,z)
            scanners_to_process.add(scanner_b)

print("Scanners:", len(scanners))
print(len(reduce(lambda acc, scanner: acc.union(scanner.beacons), scanners, set())))
from itertools import combinations
max_manhattan = 0
for (a,b) in combinations(scanners, 2):
    manhattan = sum([abs(a.location[i]-b.location[i]) for i in range(3)]) 
    if manhattan > max_manhattan:
        max_manhattan = manhattan
        pair = (a.id, b.id)

print(pair, max_manhattan)
