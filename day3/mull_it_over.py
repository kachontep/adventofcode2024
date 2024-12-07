import re
import sys
from typing import Iterator

BUFFER_LEN = 12

MUL_REGEX = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

DO_INST = "do()"
DO_INST_LEN = len(DO_INST)

DONT_INST = "don't()"
DONT_INST_LEN = len(DONT_INST)


def solve():
    s = sys.stdin.read()
    slen = len(s)
    enabled = True

    pos = 0
    total = 0
    value = None
    while pos < slen:
        s_curr = s[pos:]

        if enabled and (m := MUL_REGEX.match(s_curr)):
            left, right = m.groups()
            left, right = int(left), int(right)
            pos += m.end() - m.start()
            value = left * right
            total += value
        elif s_curr.startswith(DONT_INST):
            enabled = False
            pos += DONT_INST_LEN
        elif s_curr.startswith(DO_INST):
            enabled = True
            pos += DO_INST_LEN
        else:
            pos += 1

    print(total)


if __name__ == "__main__":
    solve()
