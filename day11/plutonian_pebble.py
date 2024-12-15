import sys
from functools import lru_cache


def main():
    stones = list(map(int, sys.stdin.read().split()))
    print(f"stones: {stones!r}")

    # total_stones = solve_part_1(stones)
    total_stones = solve_part_2(stones)
    print(f"#num_stones: {total_stones}")


def solve_part_1(stones: list[int]) -> int:
    return sum(stones_count(s, 25) for s in stones)


def solve_part_2(stones: list[int]) -> int:
    return sum(stones_count(s, 75) for s in stones)


@lru_cache(maxsize=None)
def stones_count(x: int, t: int) -> int:
    if t == 0: # any stone value without blinking returns 1
        return 1
    
    if x == 0:
        return stones_count(1, t - 1)
    
    s = str(x)
    s_len = len(s)

    if s_len % 2 == 0:
        mid = s_len // 2
        return stones_count(int(s[:mid]), t - 1) + stones_count(int(s[mid:]), t - 1)
    else:
        return stones_count(x * 2024, t - 1)


if __name__ == "__main__":
    main()
