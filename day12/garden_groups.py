import sys


def show_map(table: list[list[str]]):
    for r in table:
        for c in r:
            print(c, end="")
        print()


def show_info(s: str, area: int, perimeter: int, regions: set[tuple[int, int]]) -> None:
    print(
        f"A region of '{s}' plants with price {area} * {perimeter} = {area * perimeter}"
    )


def survey(
    r: int,
    c: int,
    table: list[list[str]],
) -> tuple[int, list[tuple[int, int, int]], set[tuple[int, int]]]:
    max_row = len(table)
    max_col = len(table[0])

    def measure(
        r: int,
        c: int,
        s: str,
        region: set[tuple[int, int]],
        direction: int = 0,
    ) -> tuple[int, list[tuple[int, int, int]], set[tuple[int, int]]]:
        if (r, c) in region:
            return 0, [], set()

        if (r < 0 or r >= max_row) or c < 0 or c >= max_col or table[r][c] != s:
            return 0, [(r, c, direction)], set()

        area = 1
        perim = []
        region = region | {(r, c)}

        for di, (dr, dc) in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)], start=1):
            n_area, n_perim, n_region = measure(r + dr, c + dc, s, region, di)
            area += n_area
            perim += n_perim
            region |= n_region

        return area, perim, region

    area, perims, region = measure(r, c, table[r][c], set())
    return area, perims, region


def num_borders_from_perims(perims: list[tuple[int, int, int]]) -> int:
    def neighbor_perims(p: tuple[int, int, int]) -> set[tuple[int, int, int]]:
        return {
            (p[0] + dr, p[1] + dc, p[2])
            for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]
        }

    relations: list[tuple[int, int]] = []
    for i, p in enumerate(perims):
        nps = neighbor_perims(p)
        for j, q in enumerate(perims):
            if q in nps:
                relations.append((i, j))

    borders = [i for i, _ in enumerate(perims)]
    for i, j in relations:
        i, j = (j, i) if j < i else (i, j)
        for k in range(len(borders)):
            if borders[k] == borders[j]:
                borders[k] = borders[i]

    return len(set(borders))


def solve_part1():
    table = [[c for c in list(line.rstrip())] for line in sys.stdin.readlines()]
    # show_map(table)

    marked = [[False for _ in row] for row in table]

    total_cost = 0

    for r in range(len(table)):
        for c in range(len(table[r])):
            if marked[r][c]:
                continue

            area, perims, region = survey(r, c, table)  # Part 1
            perims_num = len(perims)

            # show_info(table[r][c], area, perims_num, region)
            total_cost += area * perims_num

            for mr, mc in region:
                marked[mr][mc] = True

    print(total_cost)


def solve_part2():
    table = [[c for c in list(line.rstrip())] for line in sys.stdin.readlines()]
    # show_map(table)

    marked = [[False for _ in row] for row in table]

    total_cost = 0

    for r in range(len(table)):
        for c in range(len(table[r])):
            if marked[r][c]:
                continue

            area, perims, region = survey(r, c, table)  # Part 2
            borders_num = num_borders_from_perims(perims)

            # show_info(table[r][c], area, borders_num, region)
            total_cost += area * borders_num

            for mr, mc in region:
                marked[mr][mc] = True

    print(total_cost)


def main():
    # solve_part1()
    solve_part2()


if __name__ == "__main__":
    main()
