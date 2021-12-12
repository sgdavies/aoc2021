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

def explore(node, visited):
    if node == "end": return 1

    my_visited = visited.copy()
    routes = 0
    if node in smalls: my_visited.add(node)
    for other in filter(lambda x: x not in my_visited, cave[node]):
        routes += explore(other, my_visited)

    return routes

def explore_two(node, visited):
    if node == "end":
        return 1

    my_visited = visited.copy()
    routes = 0
    if node in smalls:
        my_visited[node] += 1
        if my_visited[node] > 2: return 0
    for other in sorted(cave[node]):
        if not other in my_visited:
            routes += explore_two(other, my_visited)
        elif other != "start" and len(list(filter(lambda x: x==2, my_visited.values()))) <= 1:
            routes += explore_two(other, my_visited)

    return routes

print(explore("start", set()))
print(explore_two("start", dict.fromkeys(smalls, 0)))
