from encodings import normalize_encoding
from os import path
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


def start_and_end_in_maze(maze: Maze) -> tuple[Coord, Coord]:
    for y, r in enumerate(maze):
        for x, c in enumerate(r):
            if c == "S":
                start = (x, y)
            if c == "E":
                end = (x, y)
    return start, end


def maze_dimension(maze: Maze):
    return len(maze[0]), len(maze)


def run(
    start: Coord,
    end: Coord,
    maze: Maze,
    cheat_dist: int = 2,
) -> tuple[int, list[tuple[Coord, Coord, int]]]:
    W, H = maze_dimension(maze)

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

    def runner(start: Coord) -> int:
        history: set[Coord] = set()
        fringe: list = [(start, [])]
        goal: tuple[Coord, list[Coord]] | None = None

        while fringe:
            p = fringe.pop()

            if p[0] in history:
                continue
            history.add(p[0])

            if p[0] == end:
                goal = p
                break

            for new_coord in next_coords(p[0]):
                if not is_blocked(new_coord):
                    fringe.append((new_coord, p[1] + [p[0]]))

        assert goal is not None, "Goal not found"

        for i, q in enumerate(goal[1]):
            path_costs[q] = len(goal[1]) - i
        path_costs[goal[0]] = 0

        return path_costs[start]

    normal_cost = runner(start)

    cheat_costs: list[tuple[Coord, Coord, int]] = []
    path_coords = list(path_costs.keys())

    for i, c in enumerate(path_coords):
        for w in path_coords[i+cheat_dist:]:
            dist = abs(c[0] - w[0]) + abs(c[1] - w[1])
            if dist > cheat_dist:
                continue
            cost_reduced = path_costs[c] - (path_costs[w] + dist)
            if cost_reduced > 0:
                cheat_costs.append((c, w, cost_reduced))
                
    return normal_cost, cheat_costs


def solve_part1():
    start, end = start_and_end_in_maze(maze)

    normal_cost, cheat_costs = run(start, end, maze)

    print("Normal cost:", normal_cost)

    cheats_reduce_over_100 = sum(1 for p, d, c in cheat_costs if c >= 100)
    print(f"Total cheats: {cheats_reduce_over_100}")


def solve_part2():
    start, end = start_and_end_in_maze(maze)

    normal_cost, cheat_costs = run(start, end, maze, cheat_dist=20)

    print("Normal cost:", normal_cost)

    cheats_reduce_over_100 = sum(1 for p, d, c in cheat_costs if c >= 100)
    print(f"Total cheats: {cheats_reduce_over_100}")

def main():
    # solve_part1()
    solve_part2()


if __name__ == "__main__":
    main()
