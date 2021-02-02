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
        ["+ 5000 / 1000000 + 1000 0", 6000],
        ["+ / + 5000 1000000 1000 0", 1005],
        ["+ 0 - 0 + 0 + 0 / 1 1", -1],
        ["+ 0 - 0 * 0 + 0 / 1 1", 0],
        [
            "+ 1307993905256673975767120421215822522657964858038981454399109360803651185455244290152830052265253733065911465963809993683089776960073625541502023629723947119620918917825223508962533521125777727280023703876104306028269279939868013618062200188730110219063866757530095479450736063434158250346338582528 109836762562089755439710412785302291476310964802292886550311415346968690934362496833960954250583272879636740982263693728593951807995466301001184452657840914432",
            (2**987)+(2**525)
        ],
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
        # zero division error
        ["/ 5 0", ZeroDivisionError, "division by zero"],
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
