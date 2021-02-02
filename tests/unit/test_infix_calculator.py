import pytest

from exceptions import (
    InvalidCharacterError,
    InvalidParenthesesError,
    MalformedInfixNotationError,
)
from infix_calculator import evaluate_infix_notation


@pytest.mark.parametrize(
    "expression, expected",
    (
        ["( 1 + 2 )", 3],
        ["( 6 / 2 )", 3],
        ["( 1 + ( 2 * 3 ) )", 7],
        ["( ( 1 * 2 ) + 3 )", 5],
        ["( ( ( 1 + 1 ) / 10 ) - ( 1 * 2 ) )", -1.8],
        ["( 4 * ( ( ( 6 + 1 ) - 2 ) + 6 ) )", 44],
        ["( ( ( ( 12 - 987 ) + 323 ) / 111 ) * 1023 )", (((12 - 987) + 323) / 111) * 1023],
        ["( 1 + ( ( 1 + ( 1 + 1 ) ) + 1 ) )", 5],
        ["( 5000 + ( ( 1000000 / 1000 ) + 0 ) )", 6000],
        ["( ( 0 + 0 ) - ( ( 0 + 0 ) + ( 1 / 1 ) ) )", -1],
        [
            "( 1307993905256673975767120421215822522657964858038981454399109360803651185455244290152830052265253733065911465963809993683089776960073625541502023629723947119620918917825223508962533521125777727280023703876104306028269279939868013618062200188730110219063866757530095479450736063434158250346338582528 + 109836762562089755439710412785302291476310964802292886550311415346968690934362496833960954250583272879636740982263693728593951807995466301001184452657840914432 )",
            (2**987)+(2**525)
        ],
    ),
)
def test_infix_calculator_success(expression, expected):
    assert evaluate_infix_notation(expression) == expected


@pytest.mark.parametrize(
    "expression, exception_type, exception_msg",
    (
        # implementation assumes full parentheses support, including leading and trailing parentheses
        ["6 + 5", InvalidParenthesesError, "Invalid parentheses configuration in input string."],
        # fail at the first unrecognized char when parsing in reverse order
        ["( ( 1 + 2,5 ) * 3 )", InvalidCharacterError, "Invalid character found in expression: ','."],
        # expression contains letters
        ["( a + b )", InvalidCharacterError, "Invalid character found in expression: 'a'."],
        # expression contains unsupported operator
        ["( 1 % 2 )", InvalidCharacterError, "Invalid character found in expression: '%'."],
        # expression is empty string
        ["", MalformedInfixNotationError, "The provided expression does not contain any characters."],
        # expression is None
        [None, MalformedInfixNotationError, "The provided expression does not contain any characters."],
        # too many parentheses sets
        ["( ( ( ( ( ( 1 + 1 ) ) ) ) ) )", MalformedInfixNotationError, "Expected operator or parenthesis not found."],
        # not enough operations
        ["( 6 10 )", MalformedInfixNotationError, "Not enough operators/parentheses to perform the operation."],
        # not enough parentheses
        [
            "( 10 + 4 ) + 6 )",
            MalformedInfixNotationError,
            "Not enough operators/parentheses to perform the operation.",
        ],
        # not enough values
        ["( + 4 )", MalformedInfixNotationError, "Not enough values to apply the operand '+' on."],
        # not using parentheses everywhere
        ["( 6 + ( 4 * 2 + 3 ) )", MalformedInfixNotationError, "Expected operator or parenthesis not found."],
        # parentheses left in the stack
        [
            "( ( 6 + ( 4 * ( 2 + 3 ) ) )",
            MalformedInfixNotationError,
            "There were too many values / operators / parentheses."
        ],
        # values left in the stack
        [
            "( 6000 6 + ( 4 * ( 2 + 3 ) ) )",
            MalformedInfixNotationError,
            "There were too many values / operators / parentheses."
        ],
        # zero division error
        ["( 5 / 0 )", ZeroDivisionError, "division by zero"],
    ),
)
def test_infix_calculator_when_it_raises_exception(expression, exception_type, exception_msg):
    # given
    # ... the infix notation calculator
    # when
    # ... the get orders endpoint is called for an user id
    with pytest.raises(exception_type) as error:
        evaluate_infix_notation(expression)

    # then
    # ... the expected error type and message are raised
    assert error.value.args[0] == exception_msg
