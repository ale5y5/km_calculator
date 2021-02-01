PREFIX_OPERATORS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}

INFIX_OPERATORS = {
    "+": lambda a, b: b + a,
    "-": lambda a, b: b - a,
    "*": lambda a, b: b * a,
    "/": lambda a, b: b / a,
}


def cast_float_to_int_if_no_decimals(value):
    """Casts floats with no decimals to their equivalent int values."""

    return int(value) if isinstance(value, float) and value.is_integer() else value
