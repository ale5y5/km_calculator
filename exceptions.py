class InvalidCharacterError(Exception):
    """Raised when an unsupported character is encountered in the expression."""

    pass


class MalformedPrefixNotationError(Exception):
    """Raised when the prefix expression is malformed.

    Examples: not enough values in the stack to perform the operation, too many operands and not enough operators,
    expression is None or the empty string.
    """

    pass


class InvalidParenthesesError(Exception):
    """Raised when an invalid parentheses config is encountered in the expression.

    Examples: no opening and closing parentheses for the overall expression, not an equal number of open and close
    parentheses, unexpected order of parentheses ())(."""

    pass


class MalformedInfixNotationError(Exception):
    """Raised when the infix expression is malformed."""

    pass
