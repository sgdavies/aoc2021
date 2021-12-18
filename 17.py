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
    if s*(s+1)//2 >= XMIN:
        vx_min = s
        break
    s += 1

vy_max = 1-YMIN
hits = 0
max_vy = 0
for ovx in range(vx_min, XMAX+1):
    for ovy in range(YMIN, vy_max):
        x=0;y=0
        vx=ovx;vy=ovy
        step = 1
        while True:
            x += vx
            y += vy
            if x>XMAX or y<YMIN:
                break
            if vx>0: vx -= 1
            vy -= 1
            if x>= XMIN and y <= YMAX:
                hits += 1
                if ovy>max_vy: max_vy = ovy
                break
            step += 1

print(max_vy*(max_vy+1)//2, hits)
