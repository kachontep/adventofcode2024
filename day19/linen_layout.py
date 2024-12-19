from functools import lru_cache
from itertools import groupby
import sys

patterns = list(map(lambda s: s.strip(), sys.stdin.readline().rstrip().split(",")))
sys.stdin.readline()
designs = list(map(lambda s: s.rstrip(), sys.stdin.readlines()))

PATTERNS = {
    k: list(v)
    for k, v in groupby(sorted(patterns, key=lambda s: s[0]), key=lambda s: s[0])
}

# print("patterns:", f"{patterns!r}")
# print("designs:", f"{designs!r}")


def check_valid(design: str, patterns: dict[str, list[str]]) -> bool:
    if not design:
        return True
    matches = patterns.get(design[0], [])
    for m in matches:
        if design.startswith(m) and check_valid(design[len(m):], patterns):
            return True
    return False

# def count_valid(design: str, patterns: dict[str, list[str]]) -> int:
@lru_cache(maxsize=None)
def count_valid(design: str) -> int:
    global PATTERNS
    if not design:
        return 1
    matches = PATTERNS.get(design[0], [])
    count = 0
    for m in matches:
        if design.startswith(m):
            count += count_valid(design[len(m):])
    return count

def sovle_part1():
    total = 0
    count = 0
    for d in designs:
        if check_valid(d, PATTERNS): # type: ignore
            count += 1
        total += 1
    print(count, "/", total)

def solve_part2():
    count = 0
    for d in designs:
        count += count_valid(d) # type: ignore
    print(count)

# sovle_part1()
solve_part2()
