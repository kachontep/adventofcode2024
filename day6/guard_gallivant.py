from hmac import new
import sys

MAP_OBSTRUCTION = "#"
MAP_WALKPATH = "."
MAP_GUARD = "^"

Dungeon = list[list[str]]
GuardPos = tuple[int, int]
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
            else:
                section.append(c)
        dungeon.append(section)
    assert guard_row > 0 and guard_col > 0, "Guard position not found in map"
    return (dungeon, (guard_row, guard_col))


def is_exit_pos(dungeon_width: int, dungeon_height: int, pos: GuardPos) -> bool:
    return (
        pos[0] == 0
        or pos[0] == dungeon_width - 1
        or pos[1] == 0
        or pos[1] == dungeon_height - 1
    )


def record_guard_journey(dungeon: Dungeon, pos: GuardPos) -> Journey:
    dungeon_width, dungeon_height = len(dungeon[0]), len(dungeon)
    direction = 0
    journey = []

    journey.append(pos)
    while not is_exit_pos(dungeon_width, dungeon_height, pos):
        new_pos = (pos[0] + DIRECTIONS[direction][0], pos[1] + DIRECTIONS[direction][1])
        dungeon_state = dungeon[new_pos[0]][new_pos[1]]
        if dungeon_state == MAP_WALKPATH:
            journey.append(new_pos)
            pos = new_pos
        elif dungeon_state == MAP_OBSTRUCTION:
            direction = (direction + 1) % len(DIRECTIONS)

    return journey


def compute_journey_distance(journey: Journey) -> int:
    return len(set(journey))


def main():
    dungeon, pos = lets_scan_dungeon()
    journey = record_guard_journey(dungeon, pos)
    answer = compute_journey_distance(journey)
    print(answer)


if __name__ == "__main__":
    main()
