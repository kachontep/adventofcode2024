import sys
from enum import Enum, auto

XMAS_WORD = "XMAS"
MAS_WORD = "MAS"


class Direction(Enum):
    TOP = auto()
    TOP_RIGHT = auto()
    RIGHT = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM = auto()
    BOTTOM_LEFT = auto()
    LEFT = auto()
    TOP_LEFT = auto()


def check_xmas(
    table: list[list[str]], x: int, y: int, direction: Direction
) -> bool:
    row_max = len(table)
    col_max = len(table[0])
    word_len = len(XMAS_WORD)

    table_word = None

    if direction == Direction.RIGHT:
        if y + word_len <= col_max:
            table_word = "".join([table[x][y + i] for i in range(word_len)])
    elif direction == Direction.LEFT:
        if y - word_len + 1 >= 0:
            table_word = "".join([table[x][y - i] for i in range(word_len)])
    elif direction == Direction.TOP:
        if x - word_len + 1 >= 0:
            table_word = "".join([table[x - i][y] for i in range(word_len)])
    elif direction == Direction.BOTTOM:
        if x + word_len <= row_max:
            table_word = "".join([table[x + i][y] for i in range(word_len)])
    elif direction == Direction.TOP_RIGHT:
        if x - word_len + 1 >= 0 and y + word_len <= col_max:
            table_word = "".join([table[x - i][y + i] for i in range(word_len)])
    elif direction == Direction.BOTTOM_RIGHT:
        if x + word_len <= row_max and y + word_len <= col_max:
            table_word = "".join([table[x + i][y + i] for i in range(word_len)])
    elif direction == Direction.BOTTOM_LEFT:
        if x + word_len <= row_max and y - word_len + 1 >= 0:
            table_word = "".join([table[x + i][y - i] for i in range(word_len)])
    elif direction == Direction.TOP_LEFT:
        if x - word_len + 1 >= 0 and y - word_len + 1 >= 0:
            table_word = "".join([table[x - i][y - i] for i in range(word_len)])

    return table_word == XMAS_WORD if table_word else False


def check_mas_cross(table: list[list[str]], x: int, y: int) -> bool:
    if table[x][y] != "A":
        return False
    d1 = "".join([table[x-1][y-1], table[x][y], table[x+1][y+1]])
    if d1 != MAS_WORD and d1[::-1] != MAS_WORD:
        return False
    d2 = "".join([table[x+1][y-1], table[x][y], table[x-1][y+1]])
    if d2 != MAS_WORD and d2[::-1] != MAS_WORD:
        return False
    return True


def solve():
    table = [list(line) for line in sys.stdin.read().split("\n")]
    num_rows = len(table)
    num_cols = len(table[0])

    xmas_count = sum(
        int(check_xmas(table, x, y, d))
        for x in range(num_rows)
        for y in range(num_cols)
        for d in Direction
    )

    print("Total xmas count:", xmas_count)

    mas_cross_count = sum(
        int(check_mas_cross(table, x, y))
        for x in range(1, num_rows - 1) # No need to scan the first and the last rows
        for y in range(1, num_cols - 1) # No need to scan the first and the last columns
    )

    print("Total mas cross count:", mas_cross_count)


if __name__ == "__main__":
    solve()
