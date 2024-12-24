import sys
from collections import defaultdict, namedtuple

Expression = namedtuple("Expression", "operand1 operator operand2 result")

facts: dict[str, int] = defaultdict(lambda: -1)
expressions: dict[str, Expression] = {}

# Read facts
while (line := sys.stdin.readline()) != "\n":
    gate, value = line.rstrip().split(":")
    facts[gate] = int(value.strip())

# Read expressions
while line := sys.stdin.readline():
    operand1, operator, operand2, _, result = line.rstrip().split(" ")
    expressions[result] = Expression(operand1, operator, operand2, result)

def process(z, facts: dict[str, int], expressions: dict[str, Expression]) -> None:

    def resolve(k: str) -> int:
        if k in facts and facts[k] != -1:
            return facts[k]
        k_expr = expressions[k]
        match k_expr.operator:
            case "AND":
                facts[k] = resolve(k_expr.operand1) & resolve(k_expr.operand2)
            case "OR":
                facts[k] = resolve(k_expr.operand1) | resolve(k_expr.operand2)
            case "XOR":
                facts[k] = resolve(k_expr.operand1) ^ resolve(k_expr.operand2)
        return facts[k]

    facts[z] = resolve(z)

z_gates = sorted([k for k in (set(expressions.keys()) | set(facts.keys())) if k.startswith("z")])
for z in z_gates:
    process(z, facts, expressions)

value = 0
for z in z_gates:
    value += 2**(int(z[1:]))*facts[z]

print(value)