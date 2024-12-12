import sys


def show_map(table: list[list[str]]):
    for r in table:
        for c in r:
            print(c, end="")
        print()


def show_info(s: str, area: int, perimeter: int, regions: set[tuple[int, int]]) -> None:
    print(f"Group '{s}' found with cost {area} * {perimeter} = {area * perimeter}")


def survey(
    r: int, c: int, table: list[list[str]]
) -> tuple[int, int, set[tuple[int, int]]]:
    max_row = len(table)
    max_col = len(table[0])

    def measure(
        r: int,
        c: int,
        s: str,
        region: set[tuple[int, int]],
        area: int = 1,
        perimeter: int = 0,
    ) -> tuple[int, int, set[tuple[int, int]]]:
        if (r, c) in region:
            return 0, 0, set()

        if (r < 0 or r >= max_row) or c < 0 or c >= max_col or table[r][c] != s:
            return 0, 1, set()

        region = region | {(r, c)}
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            _area, _perimeter, _region = measure(r + dr, c + dc, s, region)
            area += _area
            perimeter += _perimeter
            region |= _region

        return area, perimeter, region

    return measure(r, c, table[r][c], set())


def main():
    table = [[c for c in list(line.rstrip())] for line in sys.stdin.readlines()]
    show_map(table)

    marked = [[False for _ in row] for row in table]

    total_cost = 0

    for r in range(len(table)):
        for c in range(len(table[r])):
            if marked[r][c]:
                continue

            area, perimeter, region = survey(r, c, table)
            show_info(table[r][c], area, perimeter, region)
            total_cost += area * perimeter

            for mr, mc in region:
                marked[mr][mc] = True

    print(total_cost)


if __name__ == "__main__":
    main()
