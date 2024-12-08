from re import S
import sys
from collections import namedtuple

MAP_OBSTRUCTION = "#"
MAP_WALKPATH = "."
MAP_GUARD = "^"

Dungeon = list[list[str]]
GuardPos = namedtuple("_GuardPos", "row col")
Journey = list[GuardPos]


DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def lets_scan_dungeon() -> tuple[Dungeon, GuardPos]:
    dungeon: Dungeon = []
    guard_row, guard_col = -1, -1
    for row, line in enumerate(sys.stdin.readlines()):
        section = []
        for col, c in enumerate(line):
            if c == MAP_GUARD:
                guard_row, guard_col = row, col
                section.append(MAP_WALKPATH)
            elif c in (MAP_OBSTRUCTION, MAP_WALKPATH):
                section.append(c)
        dungeon.append(section)
    assert guard_row > 0 and guard_col > 0, "Guard position not found in map"
    return (dungeon, GuardPos(guard_row, guard_col))


def is_exit_pos(dungeon_width: int, dungeon_height: int, pos: GuardPos) -> bool:
    return (
        pos.col == 0
        or pos.col == dungeon_width - 1
        or pos.row == 0
        or pos.row == dungeon_height - 1
    )


def dungeon_dimension(dungeon: Dungeon) -> tuple[int, int]:
    dungeon_width, dungeon_height = len(dungeon[0]), len(dungeon)
    return dungeon_width, dungeon_height


def get_next_pos(pos, direction) -> GuardPos:
    return GuardPos(pos[0] + direction[0], pos[1] + direction[1])


def guard_journey_path(dungeon: Dungeon, pos: GuardPos) -> Journey:
    dungeon_width, dungeon_height = dungeon_dimension(dungeon)

    direction = 0
    journey = []
    is_patrol = False
    journey.append(pos)

    while not is_patrol and not is_exit_pos(dungeon_width, dungeon_height, pos):
        new_pos = get_next_pos(pos, DIRECTIONS[direction])
        dungeon_state = dungeon[new_pos.row][new_pos.col]
        if dungeon_state == MAP_WALKPATH:
            journey.append(new_pos)
            pos = new_pos
        elif dungeon_state == MAP_OBSTRUCTION:
            direction = (direction + 1) % len(DIRECTIONS)

    return journey


def compute_journey_distance(journey: Journey) -> int:
    return len(set(journey))


def solve_part1():
    dungeon, pos = lets_scan_dungeon()
    journey = guard_journey_path(dungeon, pos)
    answer = compute_journey_distance(journey)
    print(answer)


def is_guard_patrol(dungeon, guard_pos) -> bool:
    dungeon_width, dungeon_height = dungeon_dimension(dungeon)
    patrols = set()
    last_patrol = None
    direction = 0

    while True:
        if is_exit_pos(dungeon_width, dungeon_height, guard_pos):
            return False

        drow, dcol = DIRECTIONS[direction]
        new_pos = GuardPos(guard_pos.row + drow, guard_pos.col + dcol)

        state = dungeon[new_pos.row][new_pos.col]
        if state == MAP_OBSTRUCTION:
            if guard_pos in patrols and last_patrol and last_patrol != guard_pos:
                return True

            patrols.add(guard_pos)
            last_patrol = guard_pos
            direction = (direction + 1) % len(DIRECTIONS)

        elif state == MAP_WALKPATH:
            guard_pos = new_pos


def show_dungeon(dungeon, guard_pos):
    for row, line in enumerate(dungeon):
        for col, c in enumerate(line):
            if guard_pos == (row, col):
                print(MAP_GUARD, end="")
            else:
                print(c, end="")
        print()
    print()


def solve_part2():
    dungeon, guard_pos = lets_scan_dungeon()

    num_solutions = 0
    for row in range(len(dungeon)):
        for col in range(len(dungeon[row])):
            dungeon_state = dungeon[row][col]

            # Nothing to do for existing blocks
            if dungeon_state == MAP_OBSTRUCTION:
                continue

            # Trial with a block
            dungeon[row][col] = MAP_OBSTRUCTION

            if is_guard_patrol(dungeon, guard_pos):
                # show_dungeon(dungeon, guard_pos)
                num_solutions += 1

            # Reset trial block
            dungeon[row][col] = MAP_WALKPATH

    print(num_solutions)


def main():
    # solve_part1()
    solve_part2()


if __name__ == "__main__":
    main()
