import sys

EMPTY_ROW = "." * 5
FILLED_ROW = "#" * 5


def get_inputs() -> tuple[list[list[int]], list[list[int]]]:
    def lock_or_key(blocks: list[str]) -> tuple[list[int] | None, list[int] | None]:
        assert len(blocks) == 7 and len(blocks[0]) == 5, "Inputs has invalid dimension"
        result = [sum(1 for b in blocks[1:-1] if b[i] == "#") for i in range(5)]
        if blocks[0] == FILLED_ROW and blocks[-1] == EMPTY_ROW:
            return result, None
        elif blocks[0] == EMPTY_ROW and blocks[-1] == FILLED_ROW:
            return None, result
        else:
            raise ValueError("Schematic inputs is neither a key or a lock")

    locks: list[list[int]] = []
    keys: list[list[int]] = []
    blocks: list[str] = []
    for line in sys.stdin.readlines():
        line = line.rstrip()
        if line == "":
            if blocks:
                lock, key = lock_or_key(blocks)
                if lock:
                    locks.append(lock)
                if key:
                    keys.append(key)
            blocks.clear()
        else:
            blocks.append(line)
    if blocks:
        lock, key = lock_or_key(blocks)
        if lock:
            locks.append(lock)
        if key:
            keys.append(key)
    return locks, keys

def fit(a_lock: list[int], a_key: list[int]) -> bool:
    return all(a_lock[i] + a_key[i] <= 5 for i in range(5))

def solve_part_1():
    locks, keys = get_inputs()
    answer = 0
    answer = sum(
        1
        for a_lock in locks
        for a_key in keys
        if fit(a_lock, a_key)
    )
    print(answer)
            


def main():
    solve_part_1()


if __name__ == "__main__":
    main()
