#!/usr/bin/python
import re, sys

rel = re.compile(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")

with open(sys.argv[1]) as f:
    lines = list(map(lambda l: l.strip(), f.readlines()))

def lim_range(lo, hi):
    MAX = 50
    if hi< -MAX or lo>MAX: return []
    return range(max(-MAX, lo), min(MAX, hi)+1) # +1 at top end - range is inclusive

def simple_part_one(lines):
    voxels = {}
    for line in lines:
        m = rel.match(line)
        for x in lim_range(int(m.group(2)), int(m.group(3))):
            for y in lim_range(int(m.group(4)), int(m.group(5))):
                for z in lim_range(int(m.group(6)), int(m.group(7))):
                    voxels[(x,y,z)] = 1 if m.group(1) == "on" else 0
    print(sum(voxels.values()))

simple_part_one(lines)

def vox_vol(xw,yw,zw):
    return (xw+1)*(yw+1)*(zw+1) # Include both ends of range

def overlap(al,ah, bl,bh):
    # Returns the overlap (inclusive) or zero
    if ah<bl: return 0
    if al>bh: return 0
    if al<=bl and ah>=bh: return bh-bl+1
    if bl<=al and bh>=ah: return ah-al+1
    if al<=bl and ah<=bh: return ah-bl+1
    if bl<=al and bh<=ah: return bh-al+1
    print(al,ah, bl,bh)
    assert(False)

from typing import NamedTuple
class Box(NamedTuple):
    xl: int
    xh: int
    yl: int
    yh: int
    zl: int
    zh: int
    on: bool

    def vol(self):
        return (1+self.xh-self.xl)*(1+self.yh-self.yl)*(1+self.zh-self.zl) 

    def split_around(self, other):
        # Return list of smaller boxes that don't overlap with `other`
        # Assumes there is some overlap
        if self.xl>=other.xl and self.xh<=other.xh and \
           self.yl>=other.yl and self.yh<=other.yh and \
           self.zl>=other.zl and self.zh<=other.zh:
            # self is totally contained within other
            return []
        smalls = []
        remnant = self
        if remnant.xl < other.xl:
            smalls.append(Box(remnant.xl, other.xl-1, remnant.yl, remnant.yh, remnant.zl, remnant.zh, True))
            remnant = Box(other.xl, remnant.xh, remnant.yl, remnant.yh, remnant.zl, remnant.zh, True)
        if other.xh < remnant.xh:
            smalls.append(Box(other.xh+1, remnant.xh, remnant.yl, remnant.yh, remnant.zl, remnant.zh, True))
            remnant = Box(remnant.xl, other.xh, remnant.yl, remnant.yh, remnant.zl, remnant.zh, True)

        if remnant.yl < other.yl:
            smalls.append(Box(remnant.xl, remnant.xh, remnant.yl, other.yl-1, remnant.zl, remnant.zh, True))
            remnant = Box(remnant.xl, remnant.xh, other.yl, remnant.yh, remnant.zl, remnant.zh, True)
        if other.yh < remnant.yh:
            smalls.append(Box(remnant.xl, remnant.xh, other.yh+1, remnant.yh, remnant.zl, remnant.zh, True))
            remnant = Box(remnant.xl, remnant.xh, remnant.yl, other.yh, remnant.zl, remnant.zh, True)

        if remnant.zl < other.zl:
            smalls.append(Box(remnant.xl, remnant.xh, remnant.yl, remnant.yh, remnant.zl, other.zl-1, True))
            remnant = Box(remnant.xl, remnant.xh, remnant.yl, remnant.yh, other.zl, remnant.zh, True)
        if other.zh < remnant.zh:
            smalls.append(Box(remnant.xl, remnant.xh, remnant.yl, remnant.yh, other.zh+1, remnant.zh, True))
            remnant = Box(remnant.xl, remnant.xh, remnant.yl, remnant.yh, remnant.zl, other.zh, True)
        # By this point remnant == other

        return smalls

boxen = []

for line in lines:
    m = rel.match(line)
    new_box = Box(int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)), int(m.group(7)), m.group(1) == "on")

    new_boxen = []
    for box in boxen:
        if overlap(new_box.xl, new_box.xh, box.xl, box.xh) and \
           overlap(new_box.yl, new_box.yh, box.yl, box.yh) and \
           overlap(new_box.zl, new_box.zh, box.zl, box.zh):
            # There's some overlap.
            # Split existing box to leave a hole where the new box goes.
            # We'll then either add the new box later if it's on (filling in the gap)
            # or not if the new box is off (leaving the hole).
            new_boxen += box.split_around(new_box)
        else:
            new_boxen.append(box)

    if new_box.on:
        new_boxen.append(new_box)

    boxen = new_boxen

print(sum([box.vol() for box in boxen]))
