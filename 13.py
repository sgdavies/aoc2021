#!/usr/bin/python
with open("13.dat", "r") as f:
    lines = f.readlines()

dots = set()
folds = []

while (line := lines.pop()) != "\n":
    plane, val = line.strip().split(" ")[2].split("=")
    folds = [(plane, int(val))] + folds

for line in lines:
    x,y = line.strip().split(",")
    dots.add((int(x),int(y)))

first = True
for fold in folds:
    if fold[0] == "x":
        x = fold[1]
        folded = set(filter(lambda dot: dot[0] > x, dots))
        dots -= folded
        folded = set(map(lambda dot: (2*x - dot[0], dot[1]), folded))
        dots.update(folded)
    elif fold[0] == "y":
        y = fold[1]
        folded = set(filter(lambda dot: dot[1] > y, dots))
        dots -= folded
        folded = set(map(lambda dot: (dot[0], 2*y - dot[1]), folded))
        dots.update(folded)
    else:
        print("Bad val", fold[0], fold[1])
        exit()

    if first:
        print(len(dots))
        first = False

img = [ ["."]*(x+1) for _ in range(y+1) ]
for dot in dots:
    img[dot[1]][dot[0]] = '#'

print("\n".join(["".join(row) for row in img]))
