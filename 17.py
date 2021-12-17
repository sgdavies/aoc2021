#!/usr/bin/python
XMIN = 253
XMAX = 280
YMIN = -73
YMAX = -46

# By symmetry, v_y as we reach y=0 is the initial velocity (but downward)
# On next step, it's that +1.  We'll miss the target box if that is greater than YMIN,
# so no point searching further after that.

# vx_min is the lowest triangle number that reaches XMIN
# vx_max is XMAX - hit the far side of the target box in one step

s = 1
while True:
    if s*(s+1)//2 > XMIN:
        vx_min = s
        break
    s += 1

y_max = 1-YMIN
hits = 0
for vx in range(vx_min, XMAX+1):
    for vy in range(YMIN, y_max):
        x=0;y=0
        step = 1
        skip = False
        while not skip:
            #
            step += 1
