import itertools, sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

    g1, g2 = {}, {}
    for line in lines:
        a,b,c,d = [int(x) for x in line.replace(" -> ", ",").split(",")]
        steph = 1 if c>=a else -1
        stepv = 1 if d>=b else -1
        for x,y in itertools.zip_longest(range(a,c+steph, steph), range(b,d+stepv,stepv)):
            if x is None: x = a
            if y is None: y = b
            if a==c or b==d: g1[(x,y)] = 1 if (x,y) in g1 else 0
            g2[(x,y)] = 1 if (x,y) in g2 else 0

print(sum(g1.values()))
print(sum(g2.values()))
