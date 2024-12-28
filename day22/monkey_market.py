from functools import reduce
import sys


def accept_secrets() -> list[int]:
    return list(map(int, (l.rstrip() for l in sys.stdin.readlines())))


def next_secret1(n: int, t: int = 1) -> int:
    for _ in range(t):
        n ^= n << 6
        n &= 0b11111111_11111111_11111111
        n ^= n >> 5
        n &= 0b11111111_11111111_11111111
        n ^= n << 11
        n &= 0b11111111_11111111_11111111
    return n


def next_secret2(n: int, t: int = 1) -> list[tuple[int, tuple[int, int, int, int]]]:
    secret_values = []
    for _ in range(t):
        n ^= n << 6
        n &= 0b11111111_11111111_11111111
        n ^= n >> 5
        n &= 0b11111111_11111111_11111111
        n ^= n << 11
        n &= 0b11111111_11111111_11111111
        secret_values.append(n % 10)
    secret_changes = [(m - n) for n, m in zip(secret_values[:-1], secret_values[1:])]
    result = list(
        map(
            lambda x: (x[1], tuple(secret_changes[x[0]+1:x[0]+5])),
            enumerate(secret_values[(1 + 4) :]),
        )
    )
    return result


def solve_part_1():
    secrets = accept_secrets()

    total = 0
    for x in secrets:
        total += next_secret1(x, t=2000)
    print(total)


def solve_part_2():
    secrets = accept_secrets()

    values = [{v: k for k, v in next_secret2(s, t=2_000)[::-1]} for s in secrets]
    values_keys = reduce(lambda a,ks: a | ks, [value.keys() for value in values])

    most_bananas = 0
    secret_sequence = None
    for vk in values_keys:
        vk_bananas = 0
        for value in values:
            vk_bananas += value.get(vk, 0)
        if vk_bananas >= most_bananas:
            most_bananas = vk_bananas
            secret_sequence = vk

    print("Sequence:", secret_sequence)
    print("Most bananas:", most_bananas)


def main():
    # solve_part_1()
    solve_part_2()


if __name__ == "__main__":
    main()
