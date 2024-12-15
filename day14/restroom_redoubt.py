import re
import sys
from functools import reduce
from dataclasses import dataclass


@dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int

    def move(self, n, width, height) -> "Robot":
        px = (self.px + n * (self.vx + width)) % width
        py = (self.py + n * (self.vy + height)) % height
        return Robot(px, py, self.vx, self.vy)

    def axis(self, x_axis, y_axis) -> tuple[int, int]:
        return self.px - x_axis, self.py - y_axis


ROBOT_PATTERN = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")


def map_dimension(test: bool = True):
    if test:
        map_width = 11
        map_height = 7
    else:
        map_width = 101
        map_height = 103
    return map_width, map_height

def get_robots():
    return [
        Robot(*list(map(int, m.groups())))
        for m in [ROBOT_PATTERN.match(line.rstrip()) for line in sys.stdin.readlines()]
        if m
    ]


def show_robots(robots: list[Robot], width: int, height: int, trial: int | None = None):
    if trial:
        print("===", trial, "=" * (width - len(str(trial)) - 5))

    counts = [[0 for _ in range(height)] for _ in range(width)]
    for r in robots:
        counts[r.px][r.py] += 1

    for y in range(height):
        for x in range(width):
            if counts[x][y] == 0:
                print(".", end="")
            else:
                print(f"{counts[x][y]}", end="")
        print()


def qurants_count(moved_robots, mid_px, mid_py):
    quarants = [0 for _ in range(4)]
    for r in moved_robots:
        ax, ay = r.axis(mid_px, mid_py)
        if ax == 0 or ay == 0:
            continue
        quarant_pos = (ay > 0 and 1 or 0) * 2 + (ax > 0 and 1 or 0)
        quarants[quarant_pos] += 1
    return quarants


def map_midpoint(map_width, map_height):
    return map_width // 2, map_height // 2


def solve_part1(test: bool = False):
    robots = get_robots()
    map_width, map_height = map_dimension(test)

    n_times = 100
    
    moved_robots = [r.move(n_times, map_width, map_height) for r in robots]
    mid_px, mid_py = map_midpoint(map_width, map_height)

    quarants = qurants_count(moved_robots, mid_px, mid_py)

    answer = reduce(lambda a, b: a * b, quarants, 1)
    print(answer)


def solve_part2(test: bool):
    robots = get_robots()
    map_width, map_height = map_dimension(test)
    mid_x, mid_y = map_midpoint(map_width, map_height)
    max_r = min(map_width // 2, map_height // 2)
    r_square_threshold = (max_r / 2) ** 2
    total_robots = len(robots)

    seconds = 1
    while True:
        moved_robots = [r.move(seconds, map_width, map_height) for r in robots]

        centered_robots = 0
        for r in moved_robots:
            ax, ay = r.axis(mid_x, mid_y)
            if ax == 0 or ay == 0:
                continue

            if ax**2 + ay**2 < r_square_threshold:
                centered_robots += 1

        if 2 * centered_robots - total_robots > 0:
            break

        seconds += 1

    show_robots(moved_robots, map_width, map_height)
    print(seconds)


def main():
    # solve_part1(test=True)
    # solve_part1(test=False)

    solve_part2(test=False)


if __name__ == "__main__":
    main()
