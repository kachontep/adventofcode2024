from enum import unique
import sys
from collections import defaultdict, namedtuple
from typing import Iterator


MAP_BLANK_STATE = "."
MAP_ANTINODE_STATE = "#"


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
        if c != MAP_BLANK_STATE and c != MAP_ANTINODE_STATE:
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


def compute_antinodes_part2(src: Pos, tgt: Pos, max_pos: Pos) -> list[Pos]:
    def repeat_in_bound(p: Pos, dist_vec: Pos) -> list[Pos]:
        result = [p]
        done = False
        q = p
        while not done:
            q = Pos(q.x + dist_vec.x, q.y + dist_vec.y)
            if not is_bounded(q, max_pos):
                done = True
            else:
                result.append(q)
        return result

    dist_vec = Pos(tgt.x - src.x, tgt.y - src.y)
    src_antinodes = repeat_in_bound(src, Pos(dist_vec.x * -1, dist_vec.y * -1))
    tgt_antinodes = repeat_in_bound(tgt, dist_vec)
    return src_antinodes + tgt_antinodes


def is_bounded(p: Pos, max_xy: Pos) -> bool:
    return 0 <= p.x <= max_xy.x and 0 <= p.y <= max_xy.y


def solve_part2():
    max_pos, attena_groups = read_map_state()
    total_antinodes = []
    for _, poss in attena_groups.items():
        for src, tgt in generate_combination(poss):
            pair_antinodes = compute_antinodes_part2(src, tgt, max_pos)
            total_antinodes.extend(pair_antinodes)
    unique_antinodes = len(set(total_antinodes))
    print(unique_antinodes)


def main():
    # solve_part1()
    solve_part2()


if __name__ == "__main__":
    main()
