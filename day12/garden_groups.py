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
    border: bool = False,
) -> tuple[int, int, set[tuple[int, int]]]:
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
        perimeter = []
        region = region | {(r, c)}

        for di, (dr, dc) in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)], start=1):
            n_area, n_perimeter, n_region = measure(r + dr, c + dc, s, region, di)
            area += n_area
            perimeter += n_perimeter
            region |= n_region

        return area, perimeter, region

    area, perimeters, region = measure(r, c, table[r][c], set())

    if not border:
        return area, len(perimeters), region
    
    borders = perimeters[:]
    border_ctr = 0
    print(f"{borders}")
    while borders:
        print(f"{borders[0]}")
        bfp = _border_from_perimeter(borders[0], perimeters=borders)
        print(f"{bfp}")
        for b in bfp:
            borders.remove(b)
        border_ctr += 1


    return area, border_ctr, region

def _border_from_perimeter(p: tuple[int, int, int], perimeters: list[tuple[int, int, int]], border: set[tuple[int, int, int]]|None = None) -> set[tuple[int, int, int]]:
    border = border or {p}
    for pp in perimeters:
        if pp in border:
            continue
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if (p[0] + dr, p[1] + dc, p[2]) == pp:
                border |= _border_from_perimeter(pp, perimeters, border | {p})
    return border

def main():
    table = [[c for c in list(line.rstrip())] for line in sys.stdin.readlines()]
    show_map(table)

    marked = [[False for _ in row] for row in table]

    total_cost = 0

    for r in range(len(table)):
        for c in range(len(table[r])):
            if marked[r][c]:
                continue

            # area, perimeter, region = survey(r, c, table, use_border=False) # Part1
            area, perim_or_border, region = survey(r, c, table, border=True)  # Part 2

            show_info(table[r][c], area, perim_or_border, region)
            total_cost += area * perim_or_border

            for mr, mc in region:
                marked[mr][mc] = True

    print(total_cost)


if __name__ == "__main__":
    main()
