from os import walk
import sys
from collections import deque, namedtuple

BLOCK = "#"
WALKPATH = "."

START = "S"
END = "E"

UP = "^"
RIGHT = ">"
DOWN = "v"
LEFT = "<"

WALK_WAYS = {
    "S": list("^>v<"),
    "<": list("<^v"),
    "^": list("^<>"),
    ">": list(">^v"),
    "v": list("v<>"),
    " ": list("^>v<"),
}


TURN_STYLES = {
    ("S", "^"),
    ("^", ">"),
    ("^", "<"),
    (">", "^"),
    (">", "v"),
    ("v", ">"),
    ("v", "<"),
    ("<", "^"),
    ("<", "v"),
}

TURN_COST = 1_000
World = list[list[str]]
Point = namedtuple("Point", "x y")


def get_world():
    return [list(line.rstrip()) for line in sys.stdin.readlines()]


def start_and_end(world: World) -> tuple[Point, Point]:
    for y, row in enumerate(world):
        for x, c in enumerate(row):
            if c == START:
                start = Point(x, y)
            elif c == END:
                end = Point(x, y)
    return start, end


def next_move(p: Point, w: str, width: int, height: int) -> Point | None:
    x, y = p
    if w == UP:
        x, y = p.x, p.y - 1
    elif w == RIGHT:
        x, y = p.x + 1, p.y
    elif w == DOWN:
        x, y = p.x, p.y + 1
    elif w == LEFT:
        x, y = p.x - 1, p.y
    if x >= 0 and x < width and y >= 0 and y < height:
        return Point(x, y)
    return None


def world_dimension(world) -> tuple[int, int]:
    return len(world[0]), len(world)


def reveal_the_world(world):
    for r in world:
        for c in r:
            print(c, end="")
        print()


def show_travel_path_with_cost(world, travel_path, travel_cost):
    show_travel_path(travel_path, world)
    print("cost: ", travel_cost)


def path_cost(travel_path: list[str]) -> int:
    total_cost = 0
    for p, q in zip(travel_path[:-1], travel_path[1:]):
        if (p, q) in TURN_STYLES:
            total_cost += TURN_COST
    total_cost += len(travel_path[1:] if travel_path[0] == START else travel_path)
    return total_cost


def show_travel_path(travel_path: list[str], world: World):
    width, height = world_dimension(world)
    start, end = start_and_end(world)

    traveled_world = [[c for c in r] for r in world]
    traveled_world[start.y][start.x] = START
    traveled_world[end.y][end.x] = END

    p = start
    ww = START
    for w in travel_path:
        traveled_world[p.y][p.x] = ww
        q = next_move(p, w, width, height)
        if not q:
            continue
        p = q
        ww = w

    reveal_the_world(traveled_world)


def main():
    solve_part1()


def solve_part1():
    world = get_world()
    width, height = world_dimension(world)
    start, end = start_and_end(world)

    reveal_the_world(world)

    fringe = deque()
    fringe.append((start, "S"))

    path_costs = [[float("inf") for _ in range(width)] for _ in range(height)]

    travel_paths: list[list[str]] = []
    # travel_path: list[str] | None = None
    travel_cost = float("inf")

    while fringe:
        s = fringe.popleft()
        loc, journal = s

        cost = path_cost(journal)

        print(f"{loc.x},{loc.y}", "path: ", journal, "cost: ", cost, "path_costs:", path_costs[loc.y][loc.x])

        if cost  >= path_costs[loc.y][loc.x]:
            continue
        
        path_costs[loc.y][loc.x] = cost

        if world[loc.y][loc.x] == END:
            print(f"{loc.x},{loc.y}", "path: ", journal, "cost: ", cost, "travel_cost", travel_cost)
            if cost < travel_cost:
                travel_paths.clear()
            travel_paths.append(journal)
            travel_cost = cost
            continue

        ways = journal[-1]
        for w in WALK_WAYS[ways]:
            if (m := next_move(loc, w, width, height)) and world[m.y][m.x] != BLOCK:
                fringe.append((m, journal + w))

    if not travel_paths:
        raise SystemExit("No travel paths found for this world")

    print("Best path(s): ", len(travel_paths))
    for tp in travel_paths:
        show_travel_path_with_cost(world, tp, travel_cost)

    sit_paths = best_sit_paths(travel_paths, world)
    show_best_sit_paths(sit_paths, world)
    print(f"There are {len(sit_paths)} best sit path(s) in this world")


def best_sit_paths(travel_paths: list[list[str]], world: World) -> set[Point]:
    start, _ = start_and_end(world)
    width, height = world_dimension(world)

    result = set()
    for tp in travel_paths:
        p = start
        result.add(p)
        for w in tp:
            q = next_move(p, w, width, height)
            if not q:
                continue
            p = q
            result.add(p)
    return result


def show_best_sit_paths(sit_paths: set[Point], world: World) -> None:
    for y, r in enumerate(world):
        for x, c in enumerate(r):
            if (x, y) in sit_paths:
                print("O", end="")
            else:
                print(c, end="")
        print()


def show_best_sit_Paths(sit_paths: set[Point], world: World) -> None:
    pass


if __name__ == "__main__":
    main()
