from dataclasses import dataclass
from collections import deque
from typing import Callable


@dataclass
class Operator:
    priority: int  # operator priority (higher will be performed first)
    operation: Callable[[deque, deque], None]  # function to perform operation (number_stack, operation_stack)
    ltr: bool = True  # associativity of the operator (left-to-right, right-to-left)


# Functions which perform the action for an operator using the number_stack for input and output
# The operation stack parameter is only needed for the parentheses
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
    # do nothing, wait for right parenthesis
    pass


def right_parenthesis(numbers, operations):
    # perform all operations since the last left parenthesis
    operation = operator_stack.pop()

    while operation != "(":
        operators[operation].operation(number_stack, operator_stack)
        operation = operator_stack.pop()


# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Operator_Precedence
operators = {
    '+': Operator(12, add, True),
    '-': Operator(12, sub, True),
    '*': Operator(13, multiply, True),
    '/': Operator(13, divide, True),
    '%': Operator(13, remainder, True),
    '^': Operator(14, power, False),
    # Special case, not a real operator, set to 0 so next operator will always have higher precendence
    '(': Operator(0, left_parenthesis, True),
    ')': Operator(19, right_parenthesis, True)
}

def get_next_syllable(input_string):
    for c in input_string:
        if c == " ":
            continue
        if not c.isnumeric():
            assert c in operators, f"ERROR: unknown operator {c}"
        yield c, not c.isnumeric()


def has_precendence(operator2, operator1):
    # operator1 has priority over operator2 if its priority is higher,
    # or if they have the same priority and their associativity is ltr
    return operators[operator1].priority <= operators[operator2].priority if operators[operator1].ltr \
        else operators[operator1].priority < operators[operator2].priority


if __name__ == '__main__':
    print("Infix 2 Postfix")

    operator_stack = deque()
    number_stack = deque()

    input_string = "((((((2+7)*8*7)-3-9)*(9-2)+9*6)*((2-3)+5-7)-4+3)*(((8-6)-4+3)-7-2)*(1-1)*5+4)*((((((6+8)%9-6)%8%4)%(3%8)-1-5)+((6+2)%9+1)+7-1)-(((7%8)-4-9)-7-5)-(4+7)+6-3)*((((((3+7)-1*5)+3-2)*(6-5)*9-2)*((9-7)*5-4)-9+9)+(((4*7)*1/7)+9*3)+(6-4)*3/1+2^3^2+2^3^2)/((((((5+5)/5-5)-5/5)+(5-5)-5*5)+((5/5)+5/5)/5*5)*(((5+5)-5-5)+5+5)*(5-5)/5+5)/((((((2+1)/3+3)/1+2)+(2+1)+2+1)/((2/1)+3/3)+2+3)/(((3+1)/2+1)/2+3)/(1/2)+2+1)/((((((8+9)%8%4)%8%1)+(1%6)%4+8)+((4%2)+8+8)%1+2)+(((1%1)+4+8)+6+5)%(2%7)+1%5)/((((9+9)-8-9)+8-8)*(9-8)+9*8)"

    for value, is_operator in get_next_syllable(input_string):
        if is_operator:
            # left parenthesis are only used for grouping. just store and 'wait' for the right parenthesis
            if value == "(":
                operator_stack.append(value)
                continue

            # if the operator on the stack has precedence over this operator it needs to be
            # executed before adding the new operator to the stack
            while len(operator_stack) > 0 and has_precendence(operator_stack[-1], value):
                operation = operators[operator_stack.pop()]
                operation.operation(number_stack, operator_stack)

            operator_stack.append(value)
        else:
            number_stack.append(int(value))

    # execute remaining operators on the stack
    while len(operator_stack) > 0:
        operation = operators[operator_stack.pop()]
        operation.operation(number_stack, operator_stack)

    print(f"Result = {number_stack[0]}")
