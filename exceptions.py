class InvalidCharacterError(Exception):
    """Raised when an unsupported character is encountered in the expression."""

    pass


class MalformedPrefixNotationError(Exception):
    """Raised when the prefix expression is malformed.

    Examples: not enough values in the stack to perform the operation, too many operands and not enough operators,
    expression is None or the empty string.
    """

    pass
