import sys
from collections import namedtuple

Coord = namedtuple("Coord", "x y")

NUMERIC_KEYPAD = {
    "A": Coord(3, 4),
    "0": Coord(2, 4),
    "1": Coord(1, 3),
    "2": Coord(2, 3),
    "3": Coord(3, 3),
    "4": Coord(1, 2),
    "5": Coord(2, 2),
    "6": Coord(3, 2),
    "7": Coord(1, 1),
    "8": Coord(2, 1),
    "9": Coord(3, 1),
}

DIRECTIONAL_PAD = {
    "A": Coord(3, 1),
    "^": Coord(2, 1),
    "<": Coord(1, 2),
    "v": Coord(2, 2),
    ">": Coord(3, 2),
}


DIRECTIONS = {
    (-1, 0): "<",
    (1, 0): ">",
    (0, -1): "^",
    (0, 1): "v",
}


def num2dir(x: str) -> str:
    actions = []
    x = "A" + x
    for src, dest in zip(x[:-1], x[1:]):
        src_loc, dest_loc = NUMERIC_KEYPAD[src], NUMERIC_KEYPAD[dest]
        x_diff, y_diff = dest_loc[0] - src_loc[0], dest_loc[1] - src_loc[1]
        x_moves = (
            DIRECTIONS[(int(x_diff / abs(x_diff)), 0)] * abs(x_diff)
            if x_diff != 0
            else ""
        )
        y_moves = (
            DIRECTIONS[(0, int(y_diff / abs(y_diff)))] * abs(y_diff)
            if y_diff != 0
            else ""
        )
        if src_loc[1] == 3:
            actions.append(y_moves + x_moves + "A")
        else:
            actions.append(x_moves + y_moves + "A")
    result = "".join(actions)
    return result


def dir2dir(x: str) -> str:
    actions = []
    x = "A" + x
    for i, (src, dest) in enumerate(zip(x[:-1], x[1:])):
        src_loc, dest_loc = DIRECTIONAL_PAD[src], DIRECTIONAL_PAD[dest]
        x_diff, y_diff = dest_loc[0] - src_loc[0], dest_loc[1] - src_loc[1]
        x_moves = (
            DIRECTIONS[(int(x_diff / abs(x_diff)), 0)] * abs(x_diff)
            if x_diff != 0
            else ""
        )
        y_moves = (
            DIRECTIONS[(0, int(y_diff / abs(y_diff)))] * abs(y_diff)
            if y_diff != 0
            else ""
        )
        if src_loc[0] == 1:
            actions.append(x_moves + y_moves + "A")
        else:
            actions.append(y_moves + x_moves + "A")
        # print(str(i) + ":", x[:i+1], ":>", src, dest, ":-", actions[-1])
    result = "".join(actions)
    return result

def control(x: str) -> str:
    # return x
    # return num2dir(x)
    # return dir2dir(num2dir(x))
    return dir2dir(dir2dir(num2dir(x)))
    # return "\n".join([x, num2dir(x), dir2dir(num2dir(x)), dir2dir(dir2dir(num2dir(x)))])


def get_codes():
    codes = [line.rstrip() for line in sys.stdin.readlines()]
    return codes


def solve_part_1():
    codes = get_codes()
    answer = 0
    for code in codes:
        # print(code + ":", control(code), len(control(code)))
        print(int(code[:-1]), len(control(code)))
        answer += int(code[:-1]) * len(control(code))
    print(answer)

def main():
    solve_part_1()


if __name__ == "__main__":
    main()