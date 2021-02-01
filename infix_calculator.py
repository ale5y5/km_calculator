import logging

from exceptions import InvalidCharacterError, MalformedInfixNotationError, InvalidParenthesesError

logger = logging.getLogger(__name__)


def evaluate_infix_notation(expression):
    """Evaluate the input expression in infix notation. Initial naive implementation."""

    if expression is None or len(expression) == 0:
        raise MalformedInfixNotationError("The provided expression does not contain any characters.")
    if expression[0] != "(" or expression[-1] != ")":
        raise InvalidParenthesesError("Invalid parentheses configuration in input string.")
    return eval(expression[1:-1].replace(" ", ""))


def main():
    print("Type 'exit' to end program.")
    while True:
        expression = input("Please enter an infix expression with full parentheses to be evaluated: ")
        if expression == "exit":
            break
        try:
            result = evaluate_infix_notation(expression)
            print(f" The result of evaluating expression {expression} in infix notation is {result}.")
        except (InvalidCharacterError, MalformedInfixNotationError, ZeroDivisionError) as e:
            print(f"Failed to evaluate expression: {e}")


if __name__ == "__main__":
    main()
