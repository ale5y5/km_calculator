import logging
from collections import deque

from exceptions import InvalidCharacterError, MalformedPrefixNotationError
from operations import PREFIX_OPERATORS, cast_float_to_int_if_no_decimals

logger = logging.getLogger(__name__)


def evaluate_prefix_notation(expression):
    """Evaluate the input expression in prefix notation.

    While traversing the expression in reverse order, read characters until a space is encountered.
    If the section delimited by spaces comprises of digits, convert it to int, and push it to the stack.
    (assumption used: the input literals are positive integers). If it's one of the supported operators,
    pop the last 2 values from the stack and apply the operation on them, then push the result to the stack.
    If it's neither of these, raise an error when finding an unsupported character.
    The implementation calculates in floating point domain.
    Assumption #2: each operator takes exactly 2 args, so it's raising an exception when the number of expected
    args for an operator is not enough (more exactly, when the stack is empty), or if there are more args than
    needed by the operators (more exactly, there are values remaining in the stack when the traversal of the
    expression ends).

    The implementation focus was on doing all the work in O(n), and does not raise errors for malformed expressions
    e.g. tokens are not properly spaced (e.g. too many spaces, or no spaces)
    """
    stack = deque()  # using a double ended queue as a stack of values
    value = 0
    power = 0
    if expression is None or len(expression) == 0:
        raise MalformedPrefixNotationError("The provided expression does not contain any characters.")

    for c in expression[::-1]:
        if c in PREFIX_OPERATORS.keys():
            operation = PREFIX_OPERATORS[c]
            # apply operator to the latest 2 values from the stack, but only push result to stack on next space char
            try:
                value = operation(stack.pop(), stack.pop())
            except IndexError as e:
                # if the stack is empty, raise an error
                logger.exception(e)
                raise MalformedPrefixNotationError(f"There are not enough values to apply the operand '{c}' on.")
            except ZeroDivisionError as e:
                logger.exception(e)
                raise
        else:
            if c.isdigit():
                value += int(c) * 10 ** power
                power += 1
            elif c == " ":
                # always push calculated value in the stack on the next space (while reading backwards)
                stack.append(value)
                value = 0
                power = 0
            else:
                error_mgs = f"Invalid character found in expression: '{c}'."
                logger.error(error_mgs)
                raise InvalidCharacterError(error_mgs)

    # if the stack is not empty at the end, raise an exception
    if stack:
        error_mgs = "There were too many values and not enough operators."
        logger.error(error_mgs)
        raise MalformedPrefixNotationError(error_mgs)

    # return the latest calculated value - we haven't pushed it to the stack yet
    # since there is no preceding "space" on which to do it
    return cast_float_to_int_if_no_decimals(value)


def main():
    print("Type 'exit' to end program.")
    while True:
        expression = input("Please enter a prefix expression to be evaluated: ")
        if expression == "exit":
            break
        try:
            result = evaluate_prefix_notation(expression)
            print(f"The result of evaluating expression {expression} in prefix notation is {result}.")
        except (InvalidCharacterError, MalformedPrefixNotationError, ZeroDivisionError) as e:
            print(f"Failed to evaluate expression: {e}")


if __name__ == "__main__":
    main()
