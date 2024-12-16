import sys

World = list[list[str]]

ROBOT = "@"
BLOCK = "#"
WALK_PATH = "."
WAREHOUSE = "O"
DOUBLE_WAREHOUSE = "[]"

UP = "^"
RIGHT = ">"
DOWN = "v"
LEFT = "<"


def show_world(world: World) -> None:
    for r in world:
        for c in r:
            print(c, end="")
        print()


def world_and_controls():
    controls = []
    world = []

    lines = sys.stdin.readlines()

    line_num = 0
    for line in lines:
        line_num += 1
        line = line.rstrip()
        if line == "":
            break
        world.append(list(line))

    for line in lines[line_num:]:
        line.rstrip()
        controls.extend(list(line))

    return world, controls


def main():
    solve_part1()

def solve_part1():
    world, controls = world_and_controls()
    show_world(world)

    robot, *_ = robot_position(world)

    for c in controls:
        robot = send_control(robot, c, world)

    show_world(world)

    answer = gps_coordinates(world)
    print(answer)

def gps_coordinates(world):
    result = 0
    for y, r in enumerate(world):
        for x, c in enumerate(r):
            if c == WAREHOUSE:
                result += y*100 + x
    return result


def robot_position(world):
    return [(x, y) for y, r in enumerate(world) for x, c in enumerate(r) if c == ROBOT]


def send_control(robot: tuple[int, int], control: str, world: World) -> tuple[int, int]:
    mv = move_vec(control)
    x, y = robot
    nx, ny = x + mv[0], y + mv[1]

    # print((x, y), control, (nx, ny), "world[ny][nx]: ", world[ny][nx])

    if world[ny][nx] == BLOCK:
        return robot

    if world[ny][nx] == WALK_PATH:
        world[y][x], world[ny][nx] = WALK_PATH, ROBOT
        robot = nx, ny

    if world[ny][nx] == WAREHOUSE:
        if warehouse_movable((nx, ny), mv, world):
            move_warehouse((nx, ny), mv, world)
            world[y][x] = WALK_PATH
            world[ny][nx] = ROBOT
            robot = nx, ny

    return robot

def warehouse_movable(
    position: tuple[int, int], move_vec: tuple[int, int], world: World
) -> bool:
    x, y = position
    if world[y][x] == BLOCK:
        return False
    if world[y][x] == WALK_PATH:
        return True

    nx, ny = x + move_vec[0], y + move_vec[1]
    return warehouse_movable((nx, ny), move_vec, world)


def move_warehouse(
    position: tuple[int, int], move_vec: tuple[int, int], world: World
) -> None:
    x, y = position
    nx, ny = x + move_vec[0], y + move_vec[1]

    if world[y][x] == WAREHOUSE and world[ny][nx] == WAREHOUSE:
        move_warehouse((nx, ny), move_vec, world)

    world[ny][nx] = WAREHOUSE
    world[y][x] = WALK_PATH


def move_double_warehouse():
    # TODO:
    pass

def move_vec(control):
    match control:
        case "^":
            move_vec = (0, -1)
        case ">":
            move_vec = (1, 0)
        case "v":
            move_vec = (0, 1)
        case "<":
            move_vec = (-1, 0)
        case _:
            move_vec = (0, 0)
    return move_vec


if __name__ == "__main__":
    main()
