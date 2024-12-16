from shutil import move
import sys

World = list[list[str]]
Vector2 = tuple[int, int]

ROBOT = "@"
BLOCK = "#"
WALK_PATH = "."
WAREHOUSE1 = "O"
WAREHOUSE2 = "[]"

UP = "^"
RIGHT = ">"
DOWN = "v"
LEFT = "<"

UP_VEC2 = (0, -1)
RIGHT_VEC2 = (1, 0)
DOWN_VEC2 = (0, 1)
LEFT_VEC2 = (-1, 0)


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
    # solve_part1()
    solve_part2()


def solve_part1():
    world, controls = world_and_controls()
    show_world(world)

    robot, *_ = robot_position(world)

    for seq_no, c in enumerate(controls):
        robot = send_control(robot, c, world, seq_no)

    show_world(world)

    answer = gps_coordinates(world, warehouse_type=WAREHOUSE1)
    print(answer)


def solve_part2():
    world, controls = world_and_controls()
    world = new_world(world)
    show_world(world)

    robot, *_ = robot_position(world)

    for seq_no, c in enumerate(controls):
        robot = send_control(robot, c, world, seq_no)
        # show_world(world)

    show_world(world)

    answer = gps_coordinates(world, warehouse_type=WAREHOUSE2)
    print(answer)


def gps_coordinates(world, warehouse_type: str):
    w = warehouse_type if warehouse_type == WAREHOUSE1 else WAREHOUSE2[0]
    result = 0
    for y, r in enumerate(world):
        for x, c in enumerate(r):
            if c == w:
                result += y * 100 + x
    return result


def robot_position(world):
    return [(x, y) for y, r in enumerate(world) for x, c in enumerate(r) if c == ROBOT]


def send_control(
    robot: tuple[int, int], control: str, world: World, seq_no: int
) -> tuple[int, int]:
    mv = move_vec(control)
    x, y = robot
    nx, ny = x + mv[0], y + mv[1]

    # print(f"{seq_no}:", (x, y), control, (nx, ny), "world[ny][nx]: ", world[ny][nx])

    if world[ny][nx] == BLOCK:
        return robot

    elif world[ny][nx] == WALK_PATH:
        world[y][x], world[ny][nx] = WALK_PATH, ROBOT
        robot = nx, ny

    elif world[ny][nx] == WAREHOUSE1:
        if warehouse_movable((nx, ny), mv, world):
            move_warehouse((nx, ny), mv, world)
            world[y][x] = WALK_PATH
            world[ny][nx] = ROBOT
            robot = nx, ny
    elif is_warehouse2((nx, ny), world):
        if warehouse_movable((nx, ny), mv, world):
            move_warehouse2((nx, ny), mv, world)
            world[y][x] = WALK_PATH
            world[ny][nx] = ROBOT
            robot = nx, ny

    return robot


def is_warehouse2(pos: Vector2, world: World) -> bool:
    return world[pos[1]][pos[0]] in set(list(WAREHOUSE2))


def warehouse2_components(pos: Vector2, world: World) -> tuple[Vector2, Vector2]:
    nx, ny = pos
    if world[ny][nx] == WAREHOUSE2[0]:
        return (nx, ny), (nx + 1, ny)
    elif world[ny][nx] == WAREHOUSE2[1]:
        return (nx - 1, ny), (nx, ny)
    else:
        raise ValueError(f"({nx}, {ny}) doesn't contain a double warehouse")


def warehouse_movable(pos: Vector2, mv: tuple[int, int], world: World) -> bool:
    x, y = pos

    if world[y][x] == BLOCK:
        return False
    if world[y][x] == WALK_PATH:
        return True

    if is_warehouse2((x, y), world):
        c1, c2 = warehouse2_components((x, y), world)
        nc1 = next_move(c1, mv)
        nc2 = next_move(c2, mv)

        if mv == UP_VEC2 or mv == DOWN_VEC2:
            c1_mv = warehouse_movable(nc1, mv, world)
            c2_mv = warehouse_movable(nc2, mv, world)
            return c1_mv and c2_mv
        elif mv == LEFT_VEC2:
            return warehouse_movable(nc1, mv, world)
        elif mv == RIGHT_VEC2:
            return warehouse_movable(nc2, mv, world)

    return warehouse_movable(next_move(pos, mv), mv, world)


def next_move(pos: Vector2, mv: Vector2) -> Vector2:
    return pos[0] + mv[0], pos[1] + mv[1]


def move_warehouse(pos: tuple[int, int], mv: tuple[int, int], world: World) -> None:
    x, y = pos
    nx, ny = x + mv[0], y + mv[1]

    if world[y][x] == WAREHOUSE1 and world[ny][nx] == WAREHOUSE1:
        move_warehouse((nx, ny), mv, world)

    world[y][x], world[ny][nx] = WALK_PATH, world[y][x]


def move_warehouse2(pos: tuple[int, int], mv: tuple[int, int], world: World) -> None:
    if not is_warehouse2(pos, world):
        return

    c1, c2 = warehouse2_components(pos, world)
    nc1 = next_move(c1, mv)
    nc2 = next_move(c2, mv)

    if mv == UP_VEC2 or mv == DOWN_VEC2:
        move_warehouse2(nc1, mv, world)
        move_warehouse2(nc2, mv, world)

        world[nc1[1]][nc1[0]], world[nc2[1]][nc2[0]] = WAREHOUSE2[0], WAREHOUSE2[1]
        world[c1[1]][c1[0]], world[c2[1]][c2[0]] = WALK_PATH, WALK_PATH

    elif mv == LEFT_VEC2:
        move_warehouse2(nc1, mv, world)
        world[nc1[1]][nc1[0]], world[c1[1]][c1[0]], world[c2[1]][c2[0]] = (
            WAREHOUSE2[0],
            WAREHOUSE2[1],
            WALK_PATH,
        )

    elif mv == RIGHT_VEC2:
        move_warehouse2(nc2, mv, world)
        world[nc2[1]][nc2[0]], world[c2[1]][c2[0]], world[c1[1]][c1[0]] = (
            WAREHOUSE2[1],
            WAREHOUSE2[0],
            WALK_PATH,
        )


def move_vec(control: str) -> Vector2:
    match control:
        case "^":
            move_vec = UP_VEC2
        case ">":
            move_vec = RIGHT_VEC2
        case "v":
            move_vec = DOWN_VEC2
        case "<":
            move_vec = LEFT_VEC2
        case _:
            move_vec = (0, 0)
    return move_vec


def new_world(world: World) -> World:
    def world_change(c: str) -> str:
        match c:
            case "@":
                return "@."
            case "#":
                return "##"
            case "O":
                return "[]"
            case ".":
                return ".."
            case _:
                raise ValueError(f"Unknown '{c}' character found")

    return [list("".join(map(world_change, r))) for r in world]


if __name__ == "__main__":
    main()
