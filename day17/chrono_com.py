import sys
from typing import Callable

def lit(x: int) -> int:
    return x

def make_combo(com: dict[str,int]) -> Callable[[int], int]:
    def combo(x: int) -> int: # type: ignore
        match x:
            case 0 | 1 | 2 | 3:
                return x
            case 4:
                return com["a"]
            case 5:
                return com["b"]
            case 6:
                return com["c"]
            case 7:
                raise ValueError("combo should not get 7 as input")
    return combo

reg_a = sys.stdin.readline()
reg_a = int(reg_a[len("Register A:")+1:].strip())

reg_b = sys.stdin.readline()
reg_b = int(reg_b[len("Register B:")+1:].strip())

reg_c = sys.stdin.readline()
reg_c = int(reg_c[len("Register C:")+1:].strip())

sys.stdin.readline()

insts = sys.stdin.readline()
insts = list(map(int, insts[len("Program:")+1:].strip().split(",")))
insts = list(zip(insts[0::2], insts[1::2]))

# print(reg_a, reg_b, reg_c, insts)

com = {
    "a": reg_a,
    "b": reg_b,
    "c": reg_c,
}

LIT = lit
COMBO = make_combo(com)

outputs = []

insts_len = len(insts)
i = 0
while i < insts_len:
    inst, opr = insts[i]
    print("debug >> ", "inst:", inst, "opr:", opr, "->", "com:", com)
    match inst:
        case 0:
            com['a'] = int(com['a'] / (2**COMBO(opr)))
        case 1:
            com['b'] = com['b'] ^ LIT(opr)
        case 2:
            com['b'] = COMBO(opr) % 8
        case 3:
            if com['a'] != 0:
                i = LIT(opr)
                continue
        case 4:
            com['b'] = com['b'] ^ com['c']
        case 5:
            outputs.append(COMBO(opr) % 8)
        case 6:
            com['b'] = int(com['a'] / (2**COMBO(opr)))
        case 7:
            com['c'] = int(com['a'] / (2**COMBO(opr)))
    i += 1

output = ",".join(str(o) for o in outputs)
print(output)
