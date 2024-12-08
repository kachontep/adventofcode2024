from functools import lru_cache
import sys
from collections import defaultdict
from typing import Callable


def get_page_ordering_rules() -> dict[int, list[int]]:
    rules = defaultdict(list)
    while line := sys.stdin.readline():
        line = line.rstrip()
        if not line:
            break
        before, after = line.split("|")
        rules[int(before)].append(int(after))
    return rules


def get_updates() -> list[list[int]]:
    return [list(map(int, line.split(","))) for line in sys.stdin.readlines()]


def make_dependent_pages(rules: dict[int, list[int]]) -> Callable[[int], set[int]]:
    def dependent_pages(page: int, history: set[int] = set()) -> set[int]:
        children = rules[page]
        result = set(rules[page])
        history = history | result
        for child in children:
            if child not in history:
                result |= dependent_pages(child, history)
        return result

    return dependent_pages


def get_answer(updates: list[list[int]]) -> int:
    return sum(update[len(update) // 2] for update in updates)


def is_valid_update(
    dependent_pages_func: Callable[[int], set[int]], update: list[int]
) -> bool:
    update_pages = set(update)
    for i in range(len(update)):
        needed_pages = update_pages & dependent_pages_func(update[i])
        if not needed_pages.issubset(set(update[i + 1 :])):
            return False
    return True

def fix_update(
    dependent_pages_func: Callable[[int], set[int]], update: list[int]
) -> list[int]:
    result = update[:]
    update_pages = set(update)
    update_len = len(update)

    current_pos = 0
    while current_pos < update_len:
        needed_pages = update_pages & dependent_pages_func(update[current_pos])
        remain_pages = set(update[current_pos+1:])
        if needed_pages.issubset(remain_pages):
            current_pos += 1
            continue
        # reorder_pages = needed_pages & remain_pages
        # if not reorder_pages:
        #     print(i, update, needed_pages, remain_pages)
        swap_pos = update.index(needed_pages.pop())
        result[current_pos], result[swap_pos] = result[swap_pos], result[current_pos]
        if swap_pos < current_pos:
            current_pos = swap_pos
    return result

def solve_part1(rules, updates):
    valid_updates = [
        update
        for update in updates
        if is_valid_update(make_dependent_pages(rules), update)
    ]
    answer = get_answer(valid_updates)
    print(answer)


def solve_part2(rules, updates):
    dependent_pages_func = make_dependent_pages(rules)
    invalid_updates = [
        update for update in updates if not is_valid_update(dependent_pages_func, update)
    ]
    fixed_updates = [
        fix_update(dependent_pages_func, update) for update in invalid_updates
    ]
    answer = get_answer(fixed_updates)
    print(answer)


def main():
    rules = get_page_ordering_rules()
    updates = get_updates()

    # solve_part1(rules, updates)
    solve_part2(rules, updates)


if __name__ == "__main__":
    main()
