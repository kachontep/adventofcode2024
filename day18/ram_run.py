import sys
import heapq
from collections import namedtuple


Ram = list[list[str]]
Coord = namedtuple("Coord", "x y")
WalkState = namedtuple("WalkStep", "cost x y paths direction")
WalkPath = list[WalkState]
WalkHistory = namedtuple("WalkHistory", "x y direction")


def get_fallen_bytes() -> list[Coord]:
    return [
        Coord(x, y)
        for r in sys.stdin.readlines()
        for x, y in [tuple(map(int, r.split(",")))]
    ]


WALKABLE = "."
BLOCKED = "#"


def main():
    # solve_part1(is_test=False)
    solve_part2(is_test=False)


def solve_part1(is_test: bool = True):
    if is_test:
        MAX_ROWS = 7
        MAX_COLS = 7
        MAX_FALL = 12
    else:
        MAX_ROWS = 71
        MAX_COLS = 71
        MAX_FALL = 1024

    start = Coord(0, 0)
    end = Coord(MAX_COLS - 1, MAX_ROWS - 1)

    ram: Ram = [[WALKABLE for c in range(MAX_COLS)] for r in range(MAX_ROWS)]
    fallens = get_fallen_bytes()

    for f in fallens[:MAX_FALL]:
        simulate(ram, f)

    walk_paths = walk(ram, start, end, MAX_ROWS, MAX_COLS)
    if walk_paths:
        print("answer:", walk_paths[0].cost)
    else:
        print("no answer")


def solve_part2(is_test: bool = True) -> None:
    if is_test:
        MAX_ROWS = 7
        MAX_COLS = 7
        LAST_FALL = 12
    else:
        MAX_ROWS = 71
        MAX_COLS = 71
        LAST_FALL = 1024

    start = Coord(0, 0)
    end = Coord(MAX_COLS - 1, MAX_ROWS - 1)

    ram: Ram = [[WALKABLE for c in range(MAX_COLS)] for r in range(MAX_ROWS)]
    fallens = get_fallen_bytes()

    last_byte_index = LAST_FALL

    for f in fallens[:last_byte_index]:
        simulate(ram, f)

    max_fallens = len(fallens)
    while last_byte_index < max_fallens:
        last_byte_index += 1
        simulate(ram, fallens[last_byte_index])
        walk_paths = simple_walk(ram, start, end, MAX_ROWS, MAX_COLS):
        if not walk_paths:
            break

    print(last_byte_index, len(fallens))
    if last_byte_index == max_fallens:
        print("no answer")
    else:
        answer = fallens[last_byte_index]
        print("answer:", f"({answer.x},{answer.y})")


PATH_CHARS = ["", "^", ">", "v", "<"]
FW_STEPS = [Coord(0, 0), Coord(0, -1), Coord(1, 0), Coord(0, 1), Coord(-1, 0)]
BW_STEPS = [Coord(0, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1), Coord(1, 0)]


def simple_walk(ram: Ram, start: Coord, end: Coord, max_rows: int, max_cols: int) -> WalkPath:
    return walk(ram, start, end, max_rows, max_cols, short_circuit=True)

def walk(ram: Ram, start: Coord, end: Coord, max_rows: int, max_cols: int, short_circuit: bool = False) -> WalkPath:
    result = []
    fringe = []
    heapq.heappush(fringe, WalkState(0, start.x, start.y, "", 0))
    min_cost = float("inf")
    histories: set[tuple[int, int, int]] = set()

    while fringe:
        s = heapq.heappop(fringe)

        # print("s:", s)
        # print("fringe:", fringe)

        if (s.x, s.y, s.direction) in histories:
            continue
        histories.add((s.x, s.y, s.direction))

        if result and s.cost > min_cost:
            continue

        if s.x == end.x and s.y == end.y and s.cost <= min_cost:
            if s.cost < min_cost:
                result.clear()
            result.append(s)
            min_cost = s.cost
            if short_circuit:
                return result
            continue

        next_states = [
            WalkState(
                s.cost + 1, s.x + di.x, s.y + di.y, s.paths + PATH_CHARS[s.direction], i
            )
            for i, di in enumerate(FW_STEPS)
            if i != 0 and di != BW_STEPS[s.direction]
        ]  # type: ignore
        for ns in next_states:
            if (
                ns.x < 0
                or ns.x >= max_cols
                or ns.y < 0
                or ns.y >= max_rows
                or ram[ns.y][ns.x] == BLOCKED
            ):
                continue
            heapq.heappush(fringe, ns)

    return result


def simulate(ram: Ram, f: Coord, c: str = BLOCKED) -> None:
    ram[f.y][f.x] = c


def print_ram(ram: Ram) -> None:
    for y, r in enumerate(ram):
        for x, c in enumerate(r):
            print(c, end="")
        print()


if __name__ == "__main__":
    main()
