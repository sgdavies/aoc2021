#!/usr/bin/python
descr = """pn-TY
rp-ka
az-aw
al-IV
pn-co
end-rp
aw-TY
rp-pn
al-rp
end-al
IV-co
end-TM
co-TY
TY-ka
aw-pn
aw-IV
pn-IV
IV-ka
TM-rp
aw-PD
start-IV
start-co
start-pn"""

cave = {}
smalls = set()

for line in descr.split("\n"):
    line.strip()
    a,b = line.split("-")
    if a not in cave:
        cave[a] = []
    if b not in cave:
        cave[b] = []
    cave[a].append(b)
    cave[b].append(a)

    for node in [a,b]:
        if all([c.islower() for c in node]):
            smalls.add(node)

def explore(node, visited, special):
    if node == "end": return 1

    my_visited = visited.copy()
    routes = 0
    if node in smalls: my_visited.add(node)

    for other in cave[node]:
        if not other in my_visited:
            routes += explore(other, my_visited, special)
        elif special is not None and not special and other != "start" and other in smalls:
            routes += explore(other, my_visited, True)

    return routes

def run():
    print(explore("start", set(), None))
    print(explore("start", set(), False))

#import cProfile
#cProfile.run('run()')
run()
