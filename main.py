from dataclasses import dataclass

@dataclass
class Precedence:
    priority: int
    ltr: bool = True

# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence
operators = {
    '+': Precedence(12, True),
    '-': Precedence(12, True),
    '*': Precedence(13, True),
    '/': Precedence(13, True),
    '%': Precedence(13, True),
    '^': Precedence(14, False),
    '(': Precedence(19, True), # True => n/a
    ')': Precedence(19, True)
}

def get_next_syllable(input_string):
    for c in input_string:
        if c == " ":
            continue
        if not c.isnumeric():
            assert c in operators, f"ERROR: unknown operator {c}"
        yield c, not c.isnumeric()

if __name__ == '__main__':
    print("Infix 2 Postfix")

    input_string = "1 + 2 * 3 - 4"

    for value, is_operator in get_next_syllable(input_string):
        print(value, is_operator)


