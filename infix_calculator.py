import logging
from collections import deque

from exceptions import (
    InvalidCharacterError,
    InvalidParenthesesError,
    MalformedInfixNotationError,
)
from operations import INFIX_OPERATORS, cast_float_to_int_if_no_decimals

logger = logging.getLogger(__name__)


def evaluate_infix_notation(expression):
    """Evaluate the input expression in infix notation.

    Pass through the expression in order, put ( and operators in op_stack, and operands in val_stack.
    When encountering a ), check the latest value in the operators stack is an operand, and last but one
    is a "(". Pop both, and use the operand on the latest 2 values in val_stack, and add the result to
    val_stack on the next " " char.
    Raises errors for some malformed expressions (but assumes proper spacing).
    """
    op_stack = deque()  # using a double ended queue as a stack of operations/parentheses
    val_stack = deque()  # using a double ended queue as a stack of values
    value = None

    if expression is None or len(expression) == 0:
        raise MalformedInfixNotationError("The provided expression does not contain any characters.")
    if expression[0] != "(" or expression[-1] != ")":
        raise InvalidParenthesesError("Invalid parentheses configuration in input string.")

    for c in expression:
        if c == ")":
            try:
                top_op, next_parenthesis = op_stack.pop(), op_stack.pop()
            except IndexError as e:
                # if the op_stack is empty, raise an error
                logger.exception(e)
                raise MalformedInfixNotationError(f"Not enough operators/parentheses to perform the operation.")

            if top_op not in INFIX_OPERATORS or next_parenthesis != "(":
                raise MalformedInfixNotationError(f"Expected operator or parenthesis not found.")

            operation = INFIX_OPERATORS[top_op]
            # apply operator to the latest 2 values from the val_stack, but only push result to stack on next space char
            try:
                value = operation(val_stack.pop(), val_stack.pop())
            except IndexError as e:
                # if the val_stack is empty, raise an error
                logger.exception(e)
                raise MalformedInfixNotationError(f"Not enough values to apply the operand '{top_op}' on.")
            except ZeroDivisionError as e:
                logger.exception(e)
                raise
        # add operands and open parentheses to the op_stack
        elif c in INFIX_OPERATORS.keys() or c == "(":
            op_stack.append(c)
        else:
            if c.isdigit():
                if value is None:
                    value = 0
                value = value * 10 + int(c)
            elif c == " ":
                # always push calculated value in the stack on the next space
                if value is not None:
                    val_stack.append(value)
                value = None
            else:
                error_mgs = f"Invalid character found in expression: '{c}'."
                logger.error(error_mgs)
                raise InvalidCharacterError(error_mgs)

    # if any of the stacks is not empty at the end, raise an exception
    if val_stack or op_stack:
        error_mgs = "There were too many values / operators / parentheses."
        logger.error(error_mgs)
        raise MalformedInfixNotationError(error_mgs)

    # return the latest calculated value - we haven't pushed it to the val_stack yet
    # since there is no space char on which to do it
    return cast_float_to_int_if_no_decimals(value)


def main():
    print("Type 'exit' to end program.")
    while True:
        expression = input("Please enter an infix expression with full parentheses to be evaluated: ")
        if expression == "exit":
            break
        try:
            result = evaluate_infix_notation(expression)
            print(f"The result of evaluating expression {expression} in infix notation is {result}.")
        except (InvalidCharacterError, InvalidParenthesesError, MalformedInfixNotationError, ZeroDivisionError) as e:
            print(f"Failed to evaluate expression: {e}")


if __name__ == "__main__":
    main()
