import re
import sys

BUTTON_PATTERN = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
PRIZE_PATTERN = re.compile(r"Prize: X=(\d+), Y=(\d+)")


def matchine_inputs():
    inputs = []
    for i, line in enumerate(sys.stdin.readlines()):
        line = line.rstrip()
        if not line:
            continue
        match i % 4:
            case 0:
                ax, ay = map(int, BUTTON_PATTERN.match(line).groups())  # type: ignore
            case 1:
                bx, by = map(int, BUTTON_PATTERN.match(line).groups())  # type: ignore
            case 2:
                px, py = map(int, PRIZE_PATTERN.match(line).groups())  # type: ignore
                inputs.append(((ax, ay), (bx, by), (px, py)))
    return inputs


def min_win_cost(inputs, n_times: int | None = None) -> int:
    total_cost = 0
    for input in inputs:
        a, b, p = input

        det = a[0] * b[1] - b[0] * a[1]

        if int(det) == 0:
            continue

        inv = ((b[1] / det, -1 * b[0] / det), (-1 * a[1] / det, a[0] / det))
        times = (
            inv[0][0] * p[0] + inv[0][1] * p[1],
            inv[1][0] * p[0] + inv[1][1] * p[1],
        )
        times = list(map(round, times))

        if n_times and any(t < 0 or t > n_times for t in times):
            continue

        validation = (
            a[0] * times[0] + b[0] * times[1],
            a[1] * times[0] + b[1] * times[1],
        )
        m_cost = times[0] * 3 + times[1] * 1

        # print(f"input: {input}, det: {det}, times: {times}, check: {validation}, m_cost: {m_cost}, valid: {validation == p and 'true' or 'false'}")

        if validation != p:
            continue

        total_cost += m_cost

    return total_cost


def solve_part1():
    print(min_win_cost(matchine_inputs(), n_times=100))


def solve_part2():
    def adjust_prize(inputs, compensate_amount: int = 10000000000000):
        return [
            (a, b, (p[0] + compensate_amount, p[1] + compensate_amount))
            for a, b, p in inputs
        ]

    print(min_win_cost(adjust_prize(matchine_inputs())))


def main():
    # solve_part1()
    solve_part2()


if __name__ == "__main__":
    main()
