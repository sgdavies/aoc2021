#!/usr/bin/python
import sys
with open(sys.argv[1]) as f:
    lines = f.readlines()

steps = int(sys.argv[2])

template = lines.pop(0).strip()
lines.pop(0)
recipes = {}
pairs = {}
counts = {}
for line in lines:
    k,v = line.strip().split(" -> ")
    recipes[k] = v
    pairs[k] = 0
    counts[k[0]] = 0
    counts[k[1]] = 0

for i in range(1, len(template)):
    pairs[ template[i-1]+template[i] ] += 1

for _ in range(steps):
    new_pairs = dict.copy(pairs)
    for pair, num in pairs.items():
        new_pairs[pair] -= num
        new_ingredient = recipes[pair]
        new_pairs[pair[0]+new_ingredient] += num
        new_pairs[new_ingredient+pair[1]] += num
    pairs = new_pairs

for pair, num in pairs.items():
    counts[pair[0]] += num
    counts[pair[1]] += num

# Each element in a pair is counted twice except the start and end
if steps < 5:
    print(template)
    print(recipes)
    print(pairs)
    print(counts)
counts[template[0]] += 1
counts[template[-1]] += 1
sort_counts = sorted(counts.values())
print((sort_counts[-1] - sort_counts[0])//2)
