import sys
from typing import Counter

Maze = list[list[str]]
Coord = tuple[int, int]

maze: Maze = [list(line.rstrip()) for line in sys.stdin.readlines()]


def show_maze(maze: Maze) -> None:
    for r in maze:
        for c in r:
            print(c, end="")
        print()


show_maze(maze)


def maze_dimension(maze: Maze):
    return len(maze[0]), len(maze)


def run(
    start: Coord, end: Coord, maze: Maze
) -> tuple[int, list[tuple[Coord, Coord, Coord, int]]]:
    W, H = maze_dimension(maze)

    history: set[Coord] = set()
    path_costs: dict[Coord, int] = {}

    def valid_coord(pos: Coord) -> bool:
        return 0 <= pos[0] < W and 0 <= pos[1] < H

    def next_coords(pos: Coord) -> list[Coord]:
        return [
            (pos[0] + m[0], pos[1] + m[1])
            for m in [(0, -1), (1, 0), (0, 1), (-1, 0)]
            if valid_coord((pos[0] + m[0], pos[1] + m[1]))
        ]

    def is_blocked(pos: Coord) -> bool:
        return maze[pos[1]][pos[0]] == "#"

    def use_cheat(pos: Coord, block: Coord) -> Coord | None:
        w = pos[0] + 2 * (block[0] - pos[0]), pos[1] + 2 * (block[1] - pos[1])

        return w if valid_coord(w) and not is_blocked(w) else None

    def runner(pos: Coord, cost: int = 0) -> int:
        history.add(pos)

        if pos == end:
            path_costs[pos] = 0
            return cost

        new_coords = []
        for new_coord in next_coords(pos):
            if not is_blocked(new_coord) and new_coord not in history:
                new_coords.append(new_coord)

        final_cost = min(runner(c, cost + 1) for c in new_coords)
        path_costs[pos] = final_cost - cost
        return final_cost

    normal_cost = runner(start)

    cheat_costs: list[tuple[Coord, Coord, Coord, int]] = []
    for c in path_costs.keys():
        blocks = [b for b in next_coords(c) if is_blocked(b)]
        for b in blocks:
            w = use_cheat(c, b)
            if not w:
                continue
            cost_reduced = path_costs[c] - path_costs[w]
            if cost_reduced > 0:
                cheat_costs.append((c, b, w, path_costs[c] - (path_costs[w] + 2)))

    return normal_cost, cheat_costs


def solve_part1():
    start, end = start_and_end_in_maze(maze)

    normal_cost, cheat_costs = run(start, end, maze)

    print("Normal cost:", normal_cost)

    counter = Counter(c for p, b, w, c in cheat_costs)
    for reduced_picos, num_cheat in counter.items():
        if reduced_picos < 100:
            continue
        if num_cheat > 1:
            print(f"There are {num_cheat} cheat(s) that save {reduced_picos} picoseconds.")
        else:
            print(f"There is one cheat that saves {reduced_picos} picoseconds")


def start_and_end_in_maze(maze: Maze) -> tuple[Coord, Coord]:
    for y, r in enumerate(maze):
        for x, c in enumerate(r):
            if c == "S":
                start = (x, y)
            if c == "E":
                end = (x, y)
    return start, end


def main():
    solve_part1()


if __name__ == "__main__":
    main()
