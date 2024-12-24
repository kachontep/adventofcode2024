import sys

secrets = list(map(int, (l.rstrip() for l in sys.stdin.readlines())))

def next_secret(n: int, t: int = 1) -> int:
    for _ in range(t):
        n ^= n << 6
        n &= 0b11111111_11111111_11111111
        n ^= n >> 5
        n &= 0b11111111_11111111_11111111
        n ^= n << 11
        n &= 0b11111111_11111111_11111111
    return n

total = 0
for x in secrets:
    total += next_secret(x, t=2000)
print(total)