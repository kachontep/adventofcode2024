import sys
from collections import defaultdict
from pprint import pprint

inputs: list[list[str]] = [line.rstrip().split("-") for line in sys.stdin.readlines()]

# Computers
computers = sorted(list(set([cc for c in inputs for cc in c])))

# Connections
connections: dict[str, list[str]] = defaultdict(list)
for a,b in inputs:
    connections[a].append(b)
    connections[b].append(a)

# pprint(connections)
result: set[tuple[str, str, str]] = set()
for c in computers:
    c_cons = set(connections[c])
    if len(c_cons) > 1:
        for cc in c_cons:
            cc_cons = set(connections[cc]) & c_cons
            if len(cc_cons) >= 1:
                for ccc in cc_cons:
                    result.add(tuple(sorted([c, cc, ccc]))) # type: ignore

answer = 0
for r in result:
    for t in r:
        if t.startswith("t"):
            answer += 1
            break

print(answer)