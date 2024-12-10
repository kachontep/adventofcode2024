import sys
from functools import reduce
from collections import namedtuple

SPACE_ID = -1

Block = namedtuple("Block", "id size")


def read_blocks(SPACE_ID, Block) -> list[Block]:
    return [
        Block(SPACE_ID, int(c)) if i % 2 == 1 else Block(i // 2, int(c))
        for i, c in enumerate(sys.stdin.read())
    ]


def checksum(blocks: list[Block]) -> int:
    def block_sum(start_pos: int, total: int, b: Block) -> tuple[int, int]:
        return start_pos + b.size, total + sum(
            i * b.id for i in range(start_pos, start_pos + b.size)
        )

    _, result = reduce(
        lambda c, b: block_sum(c[0], c[1], b),
        blocks[:-1],
        (0, 0),
    )
    return result


def compressed_blocks(blocks: list[Block]) -> list[Block]:
    compressed = []
    left, right = 0, len(blocks) - 1
    compressed_space = 0

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
            compressed_space += space_left
            right -= 1
            left += 1
        elif space_left > space_used:
            compressed.append(right_block)
            blocks[left] = Block(SPACE_ID, space_left - space_used)
            compressed_space += space_used
            right -= 1
        elif space_left < space_used:
            new_block = Block(block_id, space_left)
            remain_block = Block(block_id, space_used - space_left)
            compressed_space += space_left
            compressed.append(new_block)
            blocks[right] = remain_block
            left += 1

    if compressed_space > 0:
        compressed.append(Block(SPACE_ID, compressed_space))

    return compressed


def solve_part1():
    blocks = read_blocks(SPACE_ID, Block)
    blocks = compressed_blocks(blocks)
    answer = checksum(blocks)
    print(answer)


def main():
    solve_part1()


if __name__ == "__main__":
    main()
