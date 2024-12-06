import sys
from collections import Counter
from argparse import ArgumentParser


def get_inputs():
    return zip(
        *[(int(x1), int(x2)) for line in sys.stdin for x1, x2 in (line.split(),)]
    )


def part1():
    xs1, xs2 = get_inputs()
    xs1, xs2 = sorted(xs1), sorted(xs2)
    output = sum(abs(x1 - x2) for x1, x2 in zip(xs1, xs2))
    print(output)


def part2():
    xs1, xs2 = get_inputs()
    freqs = Counter(xs2)
    output = sum(x * freqs[x] for x in xs1)
    print(output)


if __name__ == "__main__":
    parser = ArgumentParser("historian_hysteria")
    parser.add_argument("command", choices=["part1", "part2"])
    args = parser.parse_args()

    match args.command:
        case "part1":
            part1()
        case "part2":
            part2()
