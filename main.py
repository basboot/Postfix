from dataclasses import dataclass
from collections import deque
from typing import Callable


@dataclass
class Precedence:
    priority: int
    operation: Callable[[deque, deque], None]
    ltr: bool = True


def add(numbers, operations):
    a = numbers.pop()
    b = numbers.pop()
    numbers.append(b + a)

def sub(numbers, operations):
    a = numbers.pop()
    b = numbers.pop()
    numbers.append(b - a)

def multiply(numbers, operations):
    a = numbers.pop()
    b = numbers.pop()
    numbers.append(b * a)

def divide(numbers, operations):
    a = numbers.pop()
    b = numbers.pop()
    numbers.append(b / a)

def remainder(numbers, operations):
    a = numbers.pop()
    b = numbers.pop()
    numbers.append(b % a)

def power(numbers, operations):
    a = numbers.pop()
    b = numbers.pop()
    numbers.append(b ** a)

def left_parenthesis(numbers, operations):
    # do nothing
    pass

def right_parenthesis(numbers, operations):
    # perform all operations since the last left parenthesis
    operation = operator_stack.pop()

    while operation != "(":
        print("perform within ()")
        print(len(operator_stack))
        operators[operation].operation(number_stack, operator_stack)
        operation = operator_stack.pop()

# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence
operators = {
    '+': Precedence(12, add, True),
    '-': Precedence(12, sub, True),
    '*': Precedence(13, multiply, True),
    '/': Precedence(13, divide, True),
    '%': Precedence(13, remainder, True),
    '^': Precedence(14, power, False),
    '(': Precedence(0, left_parenthesis, True),  # Special case, True => n/a
    ')': Precedence(19, right_parenthesis, True)
}

operator_stack = deque()
number_stack = deque()


def get_next_syllable(input_string):
    for c in input_string:
        if c == " ":
            continue
        if not c.isnumeric():
            assert c in operators, f"ERROR: unknown operator {c}"
        yield c, not c.isnumeric()


def perform_operation():
    pass


if __name__ == '__main__':
    print("Infix 2 Postfix")

    input_string = "(1 + 2) * (3 + 1)"

    for value, is_operator in get_next_syllable(input_string):
        print("NEXT: ", value, is_operator)
        if is_operator:
            # if operator has precedence add it to the stack
            # else execute operators from the stack until it has precedence
            # TODO: fit ltr vs rtl
            if value == "(":
                print("store left bracket")
                operator_stack.append(value)
                print(operator_stack)
                continue

            while len(operator_stack) > 0 and (operators[value].priority <= operators[operator_stack[-1]].priority and operator_stack[-1] != "("):
                print("perform operator")
                print(len(operator_stack))
                operation = operators[operator_stack.pop()]
                operation.operation(number_stack, operator_stack)
            else:
                print("store operator")
                operator_stack.append(value)
        else:
            print("store number")
            number_stack.append(int(value))


    print(operator_stack)
    print(number_stack)

    while len(operator_stack) > 0:
        print("perform remaining")
        print(len(operator_stack))
        operation = operators[operator_stack.pop()]
        operation.operation(number_stack, operator_stack)

    print(f"Result = {number_stack[0]}")
