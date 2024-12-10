import sys
from functools import reduce
from collections import namedtuple

SPACE_ID = -1

Block = namedtuple("Block", "id size")


def read_blocks() -> list[Block]:
    return [
        Block(SPACE_ID, int(c)) if i % 2 == 1 else Block(i // 2, int(c))
        for i, c in enumerate(sys.stdin.read())
    ]


def checksum(blocks: list[Block]) -> int:
    def block_sum(start_pos: int, bs_sum: int, b: Block) -> tuple[int, int]:
        if b.id == SPACE_ID:
            return start_pos + b.size, bs_sum
        else:
            b_sum = sum(i * b.id for i in range(start_pos, start_pos + b.size))
            return start_pos + b.size, bs_sum + b_sum

    _, result = reduce(
        lambda c, b: block_sum(c[0], c[1], b),
        blocks,
        (0, 0),
    )
    return result


def compress_blocks_part1(blocks: list[Block]) -> list[Block]:
    compressed = []
    left, right = 0, len(blocks) - 1
    total_space = 0

    while left <= right:
        left_block, right_block = blocks[left], blocks[right]

        if left_block.id != SPACE_ID:
            compressed.append(left_block)
            left += 1
            continue

        if right_block.id == SPACE_ID:
            right -= 1
            continue

        _, space_left = left_block
        block_id, space_used = right_block

        if space_left == space_used:
            compressed.append(right_block)
            total_space += space_left
            right -= 1
            left += 1
        elif space_left > space_used:
            compressed.append(right_block)
            blocks[left] = Block(SPACE_ID, space_left - space_used)
            total_space += space_used
            right -= 1
        elif space_left < space_used:
            new_block = Block(block_id, space_left)
            remain_block = Block(block_id, space_used - space_left)
            total_space += space_left
            compressed.append(new_block)
            blocks[right] = remain_block
            left += 1

    if total_space > 0:
        compressed.append(Block(SPACE_ID, total_space))

    return compressed


def compress_blocks_part2(blocks: list[Block]) -> list[Block]:
    do_more = True

    while do_more:

        do_more = False
        left_index = 0
        right_index = len(blocks) - 1

        while right_index > 0:
            target_block = blocks[right_index]

            if target_block.id == SPACE_ID:
                right_index -= 1
                continue

            space_block_index = -1
            space_block = None
            left_index = 0

            while left_index < right_index:
                left_block = blocks[left_index]
                if (
                    left_block.id == SPACE_ID
                    and left_block.size >= blocks[right_index].size
                ):
                    space_block_index = left_index
                    space_block = left_block
                    break
                left_index += 1

            if space_block:
                do_more = True
                skip_right_index = False

                target_space_blocks = [Block(SPACE_ID, target_block.size)]

                if space_block.size > target_block.size:
                    new_space_block = Block(
                        SPACE_ID, space_block.size - target_block.size
                    )
                    movement_blocks = [target_block, new_space_block]
                    skip_right_index = True
                else:
                    movement_blocks = [target_block]

                blocks = (
                    blocks[:space_block_index]
                    + movement_blocks
                    + blocks[space_block_index + 1 : right_index]
                    + target_space_blocks
                    + blocks[right_index + 1 :]
                )

                if skip_right_index:
                    right_index += 1

            right_index -= 1

    return blocks


def print_blocks(blocks: list[Block]) -> None:
    for b in blocks:
        if b.id == SPACE_ID:
            print("|" + ("." * b.size) + "|", end="")
        else:
            print(f"|{str(b.id)}**{b.size}|", end="")
            # print(str(b.id)*b.size, end="")
    print()


def solve_part1():
    blocks = read_blocks()
    blocks = compress_blocks_part1(blocks)
    answer = checksum(blocks)
    print(answer)


def solve_part2():
    blocks = read_blocks()
    blocks = compress_blocks_part2(blocks)
    print_blocks(blocks)
    answer = checksum(blocks)
    print(answer)


def main():
    # solve_part1()
    solve_part2()


if __name__ == "__main__":
    main()
