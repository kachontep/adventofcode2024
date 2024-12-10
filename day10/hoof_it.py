import sys
from collections import deque


def next_walk_paths(
    p: tuple[int, int], topo_map: list[list[int]], max_rows: int, max_cols: int
) -> list[tuple[int, int]]:
    row, col = p
    height = topo_map[row][col]
    next_height = height + 1
    result = []
    if row > 0 and topo_map[row - 1][col] == next_height:
        result.append((row - 1, col))
    if col < max_cols - 1 and topo_map[row][col + 1] == next_height:
        result.append((row, col + 1))
    if row < max_rows - 1 and topo_map[row + 1][col] == next_height:
        result.append((row + 1, col))
    if col > 0 and topo_map[row][col - 1] == next_height:
        result.append((row, col - 1))
    return result


def traihead_score_part1(p: tuple[int, int], topo_map: list[list[int]]):
    max_rows = len(topo_map)
    max_cols = len(topo_map[0])

    goals = set()
    fringe = deque()
    fringe.appendleft(p)
    while fringe:
        # print(f"fringe: {fringe!r}")
        p = fringe.popleft()
        row, col = p
        if topo_map[row][col] == 9:
            goals.add((row, col))
        else:
            for next_p in next_walk_paths(p, topo_map, max_rows, max_cols):
                fringe.appendleft(next_p)
    return len(goals)


def traihead_score_part2(p: tuple[int, int], topo_map: list[list[int]]) -> int:
    max_rows = len(topo_map)
    max_cols = len(topo_map[0])

    rating = 0
    fringe = deque()
    fringe.appendleft(p)
    while fringe:
        # print(f"fringe: {fringe!r}")
        p = fringe.popleft()
        row, col = p
        if topo_map[row][col] == 9:
            rating += 1
        else:
            for next_p in next_walk_paths(p, topo_map, max_rows, max_cols):
                fringe.appendleft(next_p)
    return rating


def solve_part1(topo_map, zero_points):
    scores = [traihead_score_part1(p, topo_map) for p in zero_points]
    print(f"scores: {scores!r}")
    total_score = sum(scores)
    print(f"total_score: {total_score!r}")


def solve_part2(topo_map, zero_points):
    ratings = [traihead_score_part2(p, topo_map) for p in zero_points]
    print(f"ratings: {ratings!r}")
    total_ratings = sum(ratings)
    print(f"total_rating: {total_ratings!r}")


def main():
    topo_map = [[int(c) for c in line.rstrip()] for line in sys.stdin.readlines()]
    zero_points = [
        (row, col)
        for row in range(len(topo_map))
        for col in range(len(topo_map[row]))
        if topo_map[row][col] == 0
    ]
    print(f"zero_points: {zero_points!r}")
    # solve_part1(topo_map, zero_points)
    solve_part2(topo_map, zero_points)


if __name__ == "__main__":
    main()
