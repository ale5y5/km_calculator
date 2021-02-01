import pytest

from exceptions import InvalidCharacterError, MalformedPrefixNotationError
from prefix_calculator import evaluate_prefix_notation


@pytest.mark.parametrize(
    "expression, expected",
    (
        # single operand, no operator
        ["3", 3],
        ["+ 1 2", 3],
        ["+ 1 * 2 3", 7],
        ["+ * 1 2 3", 5],
        ["- / 10 + 1 1 * 1 2", 3],
        ["- 0 3", -3],
        ["/ 3 2", 1.5],
        ["* / + - 12 987 323 111 1023", (((12 - 987) + 323) / 111) * 1023],
        ["+ + 1 2 - 4 3", 4],
    ),
)
def test_prefix_calculator_success(expression, expected):
    assert evaluate_prefix_notation(expression) == expected


@pytest.mark.parametrize(
    "expression, exception_type, exception_msg",
    (
        # implementation assumed only integer values are passed as parameters
        ["* / + - 12 98.7 323 111 1023", InvalidCharacterError, "Invalid character found in expression: '.'."],
        # fail at the first unrecognized char when parsing in reverse order
        ["* / + - 12 98.7 323 111 10,23", InvalidCharacterError, "Invalid character found in expression: ','."],
        # expression contains letters
        ["* a b", InvalidCharacterError, "Invalid character found in expression: 'b'."],
        # expression contains unsupported operator
        ["% 1 2", InvalidCharacterError, "Invalid character found in expression: '%'."],
        # expression is empty string
        ["", MalformedPrefixNotationError, "The provided expression does not contain any characters."],
        # expression is None
        [None, MalformedPrefixNotationError, "The provided expression does not contain any characters."],
        # expression contains insufficient args for the operator
        ["+ 1", MalformedPrefixNotationError, "There are not enough values to apply the operand '+' on."],
        # expression ends with operator
        ["+ 3 1 2 *", MalformedPrefixNotationError, "There are not enough values to apply the operand '*' on."],
        # expression contains too many args and not enough operators
        ["+ 1 2 3", MalformedPrefixNotationError, "There were too many values and not enough operators."],
        # expression contains too many args and not enough operators
        ["+ * 1 2 - 3 4 5", MalformedPrefixNotationError, "There were too many values and not enough operators."],
        # expression starts with extra operand
        ["5 + + 1 2 - 4 3", MalformedPrefixNotationError, "There were too many values and not enough operators."],
        # more than one operand and no operators
        ["5 10", MalformedPrefixNotationError, "There were too many values and not enough operators."],
    ),
)
def test_prefix_calculator_when_it_raises_exception(expression, exception_type, exception_msg):
    # given
    # ... the prefix notation calculator
    # when
    # ... the get orders endpoint is called for an user id
    with pytest.raises(exception_type) as error:
        evaluate_prefix_notation(expression)

    # then
    # ... the expected error type and message are raised
    assert error.value.args[0] == exception_msg
