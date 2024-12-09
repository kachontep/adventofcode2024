from enum import unique
import sys
from collections import defaultdict, namedtuple
from typing import Iterator

MAP_BLANK_STATE = "."


class Pos(namedtuple("_Pos", "x y")):
    pass


MaxXYPos = Pos  # width, height
AttenaGroups = dict[str, list[Pos]]  # letter and list of pos


def traverse_map_states() -> Iterator[tuple[Pos, str]]:
    for y, line in enumerate(sys.stdin.readlines()):
        for x, c in enumerate(line.rstrip()):
            yield Pos(x, y), c


def read_map_state() -> tuple[MaxXYPos, AttenaGroups]:
    attena_groups = defaultdict(list)
    max_x, max_y = -1, -1
    for pos, c in traverse_map_states():
        if c != MAP_BLANK_STATE:
            attena_groups[c].append(pos)
        if max_x < pos.x:
            max_x = pos.x
        if max_y < pos.y:
            max_y = pos.y
    return Pos(max_x, max_y), attena_groups


def generate_combination(poss: list[Pos]) -> Iterator[tuple[Pos, Pos]]:
    poss_len = len(poss)
    for i in range(poss_len - 1):
        for j in range(i + 1, poss_len):
            yield poss[i], poss[j]


def compute_antinodes(src: Pos, tgt: Pos) -> tuple[Pos, Pos]:
    dist_vec = Pos(tgt.x - src.x, tgt.y - src.y)
    antinode_src = Pos(src.x - dist_vec.x, src.y - dist_vec.y)
    antinode_tgt = Pos(tgt.x + dist_vec.x, tgt.y + dist_vec.y)
    return antinode_src, antinode_tgt


def is_in_map(p: Pos, max_x: int, max_y: int) -> bool:
    return 0 <= p.x <= max_x and 0 <= p.y <= max_y


def main():
    max_pos, attena_groups = read_map_state()
    total_antinodes = []
    for _, poss in attena_groups.items():
        for src, tgt in generate_combination(poss):
            pair_antinodes = compute_antinodes(src, tgt)
            bounded_antinodes = [
                n for n in pair_antinodes if is_in_map(n, max_pos.x, max_pos.y)
            ]
            total_antinodes.extend(bounded_antinodes)
    unique_antinodes = len(set(total_antinodes))
    print(unique_antinodes)


if __name__ == "__main__":
    main()
