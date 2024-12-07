import sys
from dataclasses import dataclass
from functools import reduce
from typing import Iterator, Tuple


@dataclass
class Level:
    values: list[int]

    @staticmethod
    def get_detlas(values: list[int]) -> list[int]:
        return [a - b for a, b in zip(values[:-1], values[1:])]
    
    @staticmethod
    def check_monotical_list(values: list[int]) -> bool:
        _, increasing, decreasing = reduce(
            lambda c, x: (c[0] + x, c[1] and c[0] + x > c[0], c[2] and c[0] + x < c[0]),
            Level.get_detlas(values),
            (0, True, True),
        )
        return increasing or decreasing

    @staticmethod
    def check_diff_spread(values: list[int]) -> bool:
        deltas: list[int] = Level.get_detlas(values)
        delta_over = any(filter(lambda d: d == 0 or d > 3, (abs(d) for d in deltas)))  # type: ignore
        return not delta_over

    @staticmethod
    def check_safe(values, removal_allows: bool = True) -> bool:
        safety = Level.check_monotical_list(values) and Level.check_diff_spread(values)
        if safety:
            return True
        if removal_allows:
            return any(
                Level.check_safe(values[:pos] + values[pos+1:], removal_allows=False)
                for pos in range(len(values))
            )
        return False

    def is_safe(self) -> bool:
        return Level.check_safe(self.values, removal_allows=True)


@dataclass
class Report:
    levels: list[Level]

    def __iter__(self) -> Iterator:
        return iter(self.levels)


report = Report(levels=[Level([int(x) for x in line.split()]) for line in sys.stdin])
safe_count = sum([1 for level in report if level.is_safe()])
print(safe_count)
