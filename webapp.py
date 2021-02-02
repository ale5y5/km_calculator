from exceptions import (
    InvalidCharacterError,
    InvalidParenthesesError,
    MalformedInfixNotationError,
    MalformedPrefixNotationError,
)
from flask import Flask, request
from infix_calculator import evaluate_infix_notation
from prefix_calculator import evaluate_prefix_notation

app = Flask(__name__)


@app.route("/status/")
def status():
    """Route for the status of the webapp."""
    return {"status": "Webapp is running."}


@app.route("/calculator/prefix/", methods=["POST"])
def prefix_calculator():
    """Route for the prefix calculator."""
    try:
        data = request.json
        expression = data.get("expression", "")
        result = evaluate_prefix_notation(expression)
        return {"result": result}
    except (InvalidCharacterError, MalformedPrefixNotationError) as e:
        return {"message": f"Please check the provided expression is in the prefix notation: {e}"}, 400
    except ZeroDivisionError:
        return {"message": f"Zero division not supported."}, 500


@app.route("/calculator/infix/", methods=["POST"])
def infix_calculator():
    """Route for the infix calculator."""
    try:
        data = request.json
        expression = data.get("expression", "")
        result = evaluate_infix_notation(expression)
        return {"result": result}
    except (InvalidCharacterError, InvalidParenthesesError, MalformedInfixNotationError) as e:
        return {"message": f"Please check the provided expression is in the infix notation: {e}"}, 400
    except ZeroDivisionError:
        return {"message": f"Zero division not supported."}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3456)
