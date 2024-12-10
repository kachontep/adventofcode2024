from os import read
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
    def block_sum(start_pos: int, total: int, b: Block) -> tuple[int, int]:
        block_total = 0
        if b.id != SPACE_ID:
            block_total = sum(i * b.id for i in range(start_pos, start_pos + b.size))
        return start_pos + b.size, total + block_total

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


def combine_space_blocks(blocks: list[Block]) -> list[Block]:
    result = blocks[:1][:]
    for current_block in blocks[1:]:
        if current_block.id == SPACE_ID and result[-1].id == SPACE_ID:
            last_block = result.pop()
            result.append(Block(SPACE_ID, last_block.size + current_block.size))
        else:
            result.append(current_block)
    return result


def compress_blocks_part2(blocks: list[Block]) -> list[Block]:
    done = False
    curr_blocks = blocks[:]

    while not done:
        moves = 0
        left = 0
        right = len(curr_blocks) - 1
        subblocks_left = []
        subblocks_right = []

        while left <= right:
            left_block, right_block = curr_blocks[left], curr_blocks[right]

            if left_block.id != SPACE_ID:
                subblocks_left.append(left_block)
                left += 1
                continue

            if right_block.id == SPACE_ID:
                subblocks_right.append(right_block)
                right -= 1
                continue

            _, space_left = left_block
            right_block_id, space_used = right_block

            if space_left >= space_used:
                subblocks_right.append(Block(SPACE_ID, space_used))

                subblocks_left.append(Block(right_block_id, space_used))
                if space_left > space_used:
                    subblocks_left.append(Block(SPACE_ID, space_left - space_used))

                moves += 1
                left += 1
                right -= 1
            else:
                subblocks_right.append(right_block)
                right -= 1

        curr_blocks = subblocks_left + subblocks_right[::-1]
        curr_blocks = combine_space_blocks(curr_blocks)

        if moves == 0:
            done = True

    return curr_blocks

def show_blocks(blocks: list[Block]) -> None:
    for b in blocks:
        c = "." if b.id == SPACE_ID else str(b.id)
        print(c * b.size, end="")
    print()

def solve_part1():
    blocks = read_blocks()
    blocks = compress_blocks_part1(blocks)
    answer = checksum(blocks)
    print(answer)


def solve_part2():
    blocks = read_blocks()
    blocks = compress_blocks_part2(blocks)
    answer = checksum(blocks)
    print(answer)


def main():
    # solve_part1()
    solve_part2()


if __name__ == "__main__":
    main()
