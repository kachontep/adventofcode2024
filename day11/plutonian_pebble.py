from functools import lru_cache
import sys


def main():
    stones = list(map(int, sys.stdin.read().split()))
    print(f"stones: {stones!r}")

    # new_stones = solve_part_1(stones)
    # print(f"#new_stones: {len(new_stones)!r}")

    total_stones = solve_part_2(stones)
    print(f"#new_stones: {total_stones}")



def solve_part_1(stones: list[int]) -> list[int]:
    return blink_part_1(stones, times=25)


def solve_part_2(stones: list[int]) -> int:
    return sum(stones_count(s, 75) for s in stones)


@lru_cache(maxsize=None)
def stones_count(x: int, n: int, t: int = 0, c: int = 1) -> int:
    if t == n:
        return c
    if x == 0:
        return stones_count(1, n, t + 1, c)
    s = str(x)
    s_len = len(s)
    if s_len % 2 == 0:
        mid = s_len // 2
        return stones_count(int(s[:mid]), n, t + 1, c) + stones_count(
            int(s[mid:]), n, t + 1, c
        )
    else:
        return stones_count(x * 2024, n, t + 1, c)


def blink_part_1(stones, times):
    @lru_cache(maxsize=None)
    def split(s: int) -> list[int]:
        result = []
        ss = str(s)
        if len(ss) % 2 == 0:
            mid = len(ss) // 2
            result.append(int(ss[:mid]))
            result.append(int(ss[mid:]))
        return result

    for _ in range(times):
        new_stones = []
        for s in stones:
            if s == 0:
                new_stones.append(1)
                continue
            if ss := split(s):
                new_stones.extend(ss)
                continue
            new_stones.append(s * 2024)
        stones = new_stones
    return new_stones


if __name__ == "__main__":
    main()
