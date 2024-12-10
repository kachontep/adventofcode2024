from collections import defaultdict
import sys
from itertools import groupby


def is_order_valid(page_order: list[int], page_rules: dict[int, list[int]]) -> bool:
    for idx in range(len(page_order) - 1, -1, -1):
        p = page_order[idx]
        if p not in page_rules:
            continue
        has_dp = len(set(page_order[idx + 1 :]) & set(page_rules[p])) > 0
        if has_dp:
            return False
    return True


def solve_part_1(page_orders: list[list[int]], page_rules: dict[int, list[int]]):
    valid_page_orders = [
        page_order
        for page_order in page_orders
        if is_order_valid(page_order, page_rules)
    ]
    print(f"valid_page_orders: {valid_page_orders!r}")
    answer = sum(page_order[len(page_order) // 2] for page_order in valid_page_orders)
    print(answer)


def fix_page_order(
    page_order: list[int], page_rules: dict[int, list[int]]
) -> list[int]:
    new_page_order = page_order[:]
    page_order_len = len(new_page_order)
    last_page_order_idx = page_order_len - 1
    idx = last_page_order_idx
    while idx >= 0:
        p = new_page_order[idx]
        if p not in page_rules:
            idx -= 1
            continue
        page_rule_set = set(page_rules[new_page_order[idx]])
        for idx2, pp in enumerate(new_page_order[idx + 1 :], start=idx+1):
            if pp in page_rule_set:
                new_page_order[idx], new_page_order[idx2] = (
                    new_page_order[idx2],
                    new_page_order[idx],
                )
                idx = last_page_order_idx
                continue
        idx -= 1
    return new_page_order


def solve_part_2(page_orders: list[list[int]], page_rules: dict[int, list[int]]):
    invalid_page_orders = [
        page_order
        for page_order in page_orders
        if not is_order_valid(page_order, page_rules)
    ]
    print(f"invalid_page_orders: {invalid_page_orders!r}")
    answer = sum(
        fix_page_order(page_order, page_rules)[len(page_order) // 2]
        for page_order in invalid_page_orders
    )
    print(answer)


def main():
    lines = [line.rstrip() for line in sys.stdin.readlines()]
    sep_pos = lines.index("")

    page_rules_kv = [
        (int(v), int(k)) for line in lines[:sep_pos] for k, v in [line.split("|")]
    ]
    page_rules = defaultdict(list)
    for k, v in page_rules_kv:
        page_rules[k].append(v)

    page_orders = [list(map(int, line.split(","))) for line in lines[sep_pos + 1 :]]

    print(f"pager_rules: {page_rules!r}")
    print(f"page_orders: {page_orders!r}")

    # solve_part_1(page_orders, page_rules)
    solve_part_2(page_orders, page_rules)


if __name__ == "__main__":
    main()
