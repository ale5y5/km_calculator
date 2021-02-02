import pytest

from webapp import app


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_status_endpoint_success(client):
    # given
    # ... the status endpoint and a running app
    # when
    # ... the /status/ endpoint is called
    response = client.get("/status/")
    # then
    # ... the status code is 200 and the expected json response is received
    assert response.status_code == 200
    assert response.json == {"status": "Webapp is running."}


@pytest.mark.parametrize(
    "expression, expected",
    (
        # simple operation
        ["+ 1 2", 3],
        # more complex operations
        ["* / + - 12 987 323 111 1023", (((12 - 987) + 323) / 111) * 1023],
        # operations with operands ending in zeroes
        ["+ / + 5000 1000000 1000 0", 1005],
        # operations with zeroes
        ["+ 0 - 0 + 0 + 0 / 1 1", -1],
        # operations with very long operands
        [
            "+ 1307993905256673975767120421215822522657964858038981454399109360803651185455244290152830052265253733065911465963809993683089776960073625541502023629723947119620918917825223508962533521125777727280023703876104306028269279939868013618062200188730110219063866757530095479450736063434158250346338582528 109836762562089755439710412785302291476310964802292886550311415346968690934362496833960954250583272879636740982263693728593951807995466301001184452657840914432",
            (2 ** 987) + (2 ** 525),
        ],
    ),
)
def test_prefix_calculator_endpoint_success(client, expression, expected):
    # given
    # ... the prefix calculator endpoint and a running app
    # when
    # ... the /calculator/prefix/ endpoint is called
    response = client.post("/calculator/prefix/", json={"expression": expression})
    # then
    # ... the status code is 200 and the expected json response is received
    assert response.status_code == 200
    assert response.json == {"result": expected}


@pytest.mark.parametrize(
    "expression, expected_status_code, exception_msg",
    (
        # expression contains invalid character, InvalidCharacterError is handled
        [
            "* a b",
            400,
            "Please check the provided expression is in the prefix notation: Invalid character found in "
            "expression: 'b'.",
        ],
        # expression is empty string, MalformedPrefixNotationError is handled
        [
            "",
            400,
            "Please check the provided expression is in the prefix notation: The provided expression does "
            "not contain any characters.",
        ],
        # expression contains insufficient args for the operator, MalformedPrefixNotationError is handled
        [
            "+ 1",
            400,
            "Please check the provided expression is in the prefix notation: There are not enough values to "
            "apply the operand '+' on.",
        ],
        # expression contains zero division, ZeroDivisionError is handled
        ["/ 2 0", 500, "Zero division not supported."],
    ),
)
def test_prefix_calculator_endpoint_raises_exception(client, expression, expected_status_code, exception_msg):
    # given
    # ... the prefix calculator endpoint and a running app
    # when
    # ... the /calculator/prefix/ endpoint is called
    response = client.post("/calculator/prefix/", json={"expression": expression})
    # then
    # ... the expected exceptions are processed and the expected status code and message are returned
    assert response.status_code == expected_status_code
    assert response.json == {"message": exception_msg}


@pytest.mark.parametrize(
    "expression, expected",
    (
        # simple operations
        ["( 1 + 2 )", 3],
        # more complex operations
        ["( 4 * ( ( ( 6 + 1 ) - 2 ) + 6 ) )", 44],
        # operations with operands ending in zeroes
        ["( 5000 + ( ( 1000000 / 1000 ) + 0 ) )", 6000],
        # operations with zeroes
        ["( ( 0 + 0 ) - ( ( 0 + 0 ) + ( 1 / 1 ) ) )", -1],
        # operations with very long operands
        [
            "( 1307993905256673975767120421215822522657964858038981454399109360803651185455244290152830052265253733065911465963809993683089776960073625541502023629723947119620918917825223508962533521125777727280023703876104306028269279939868013618062200188730110219063866757530095479450736063434158250346338582528 + 109836762562089755439710412785302291476310964802292886550311415346968690934362496833960954250583272879636740982263693728593951807995466301001184452657840914432 )",
            (2 ** 987) + (2 ** 525),
        ],
    ),
)
def test_infix_calculator_endpoint_success(client, expression, expected):
    # given
    # ... the infix calculator endpoint and a running app
    # when
    # ... the /calculator/infix/ endpoint is called
    response = client.post("/calculator/infix/", json={"expression": expression})
    # then
    # ... the status code is 200 and the expected json response is received
    assert response.status_code == 200
    assert response.json == {"result": expected}


@pytest.mark.parametrize(
    "expression, expected_status_code, exception_msg",
    (
        # expression contains invalid parentheses, InvalidParenthesesError is handled
        [
            "6 + 5",
            400,
            "Please check the provided expression is in the infix notation: Invalid parentheses configuration "
            "in input string.",
        ],
        # expression contains letters, InvalidCharacterError is handled
        [
            "( a + b )",
            400,
            "Please check the provided expression is in the infix notation: Invalid character found in expression: 'a'.",
        ],
        # expression is empty string, MalformedInfixNotationError is handled
        [
            "",
            400,
            "Please check the provided expression is in the infix notation: The provided expression does not contain "
            "any characters.",
        ],
        # too many parentheses sets, MalformedInfixNotationError is handled
        [
            "( ( ( ( ( ( 1 + 1 ) ) ) ) ) )",
            400,
            "Please check the provided expression is in the infix notation: Expected operator or parenthesis not found.",
        ],
        # zero division error
        ["( 5 / 0 )", 500, "Zero division not supported."],
    ),
)
def test_infix_calculator_endpoint_raises_exception(client, expression, expected_status_code, exception_msg):
    # given
    # ... the infix calculator endpoint and a running app
    # when
    # ... the /calculator/infix/ endpoint is called
    response = client.post("/calculator/infix/", json={"expression": expression})
    # then
    # ... the expected exceptions are processed and the expected status code and message are returned
    assert response.status_code == expected_status_code
    assert response.json == {"message": exception_msg}
