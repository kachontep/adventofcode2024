from sqlite3 import connect
import sys
from collections import defaultdict
from pprint import pprint


def accept_inputs() -> list[list[str]]:
    return [line.rstrip().split("-") for line in sys.stdin.readlines()]


def find_computers(inputs: list[list[str]]) -> list[str]:
    return sorted(list(set([cc for c in inputs for cc in c])))


def find_connections(
    inputs: list[list[str]], self_include: bool = False
) -> dict[str, list[str]]:
    # Connections
    connections: dict[str, list[str]] = defaultdict(list)
    for a, b in inputs:
        connections[a].append(b)
        connections[b].append(a)
    if self_include:
        for k in connections.keys():
            connections[k].append(k)
    return connections


def solve_part_1():
    inputs = accept_inputs()
    computers = find_computers(inputs)
    connections = find_connections(inputs)

    # pprint(connections)
    result: set[tuple[str, str, str]] = set()
    for c in computers:
        c_cons = set(connections[c])
        if len(c_cons) > 1:
            for cc in c_cons:
                cc_cons = set(connections[cc]) & c_cons
                if len(cc_cons) >= 1:
                    for ccc in cc_cons:
                        result.add(tuple(sorted([c, cc, ccc])))  # type: ignore
    answer = 0
    for r in result:
        for t in r:
            if t.startswith("t"):
                answer += 1
                break

    print(answer)

def is_complete(computers: set[str], connections: dict[str, set[str]]) -> bool:
    connected_set = set(computers)
    for c in computers:
        connected_set &= connections[c]
    return connected_set == computers

def solve_part_2():
    inputs = accept_inputs()

    connections = {k: set(v) for k,v in find_connections(inputs, self_include=True).items()}
    largest_conns = set()
    for c in connections:
        g_complete = set()
        for cc in connections[c]:
            if is_complete(g_complete | {cc}, connections):
                g_complete.add(cc)
        if len(g_complete) > len(largest_conns):
            largest_conns = g_complete

    answer = ",".join(sorted(largest_conns))
    print(answer)
        

def main():
    # solve_part_1()
    solve_part_2()


if __name__ == "__main__":
    main()
