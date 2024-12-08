from ast import Expression
import sys
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Equation:
    solution: int
    numbers: list[int]

    @classmethod
    def from_s(cls, s: str) -> "Equation":
        solution, numbers = s.split(":")
        result = Equation(
            solution=int(solution), numbers=list(map(int, numbers.strip().split()))
        )
        return result

    @property
    def resolvable(self) -> bool:
        operator_size = len(self.numbers) - 1
        first_value, *remains = self.numbers
        for operator_trial in generate_trials(operator_size):
            value = first_value
            for operator, operand in zip(operator_trial, remains):
                if operator == "+":
                    value += operand
                elif operator == "*":
                    value *= operand
            # show_expression(self.numbers, operator_trial, self.solution, value)
            if self.solution == value:
                return True
        return False


def display_equation(
    numbers: list[int], operators: list[str], solution: int, actual: int
) -> None:
    print("equation:", numbers[0], end=" ")
    for a, b in zip(operators, numbers[1:]):
        print(f"{a} {b} ", end="")
    print(", solution:", solution, ", actual:", actual)


def generate_trials(size: int) -> Iterator[list[str]]:
    oprs = ["+"] * size
    for _ in range(2**size):
        yield oprs
        oprs = oprs[:]
        for pos in range(size):
            match oprs[pos]:
                case "+":
                    oprs[pos] = "*"
                    break
                case "*":
                    oprs[pos] = "+"


def solve_part1():
    equations = [Equation.from_s(line) for line in sys.stdin.readlines()]
    resolvable_equations = [e for e in equations if e.resolvable]
    answer = sum(e.solution for e in resolvable_equations)
    print(answer)

def main():
    solve_part1()


if __name__ == "__main__":
    main()
