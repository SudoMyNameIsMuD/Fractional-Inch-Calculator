"""Pure measurement logic (no GUI): parsing, arithmetic and formatting in inches."""
from fractions import Fraction

FRACTION_DENOMINATORS = [2, 4, 8, 16, 32, 64, 128, 256]
OPERATORS = {"add": "+", "subtract": "-", "multiply": "*", "divide": "/"}


class MeasurementError(ValueError):
    """Raised with a user-presentable message when input or an operation is invalid."""


def parse_int(text):
    """Parses a whole-number field; empty means 0."""
    try:
        return int(text.strip() or 0)
    except ValueError:
        raise MeasurementError("Invalid input. Please enter valid numbers and fractions.") from None


def parse_fraction(text):
    """Parses a fraction field such as '1/2' or '0.25'; empty means 0."""
    try:
        return Fraction(text.strip() or "0")
    except ValueError:
        raise MeasurementError("Invalid input. Please enter valid numbers and fractions.") from None
    except ZeroDivisionError:
        raise MeasurementError("Invalid fraction. Denominator cannot be zero.") from None


def to_inches(feet="", inches="", fraction=""):
    """Combines the three entry strings into an exact total number of inches."""
    return parse_int(feet) * 12 + parse_int(inches) + parse_fraction(fraction)


def calculate(operation, a, b):
    """Applies an operation to two inch values; returns an exact Fraction."""
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise MeasurementError("Cannot divide by zero")
        return a / b
    raise MeasurementError("Invalid operation")


def format_measurement(total_inches, denominators=FRACTION_DENOMINATORS):
    """Formats inches as feet' inches fraction", rounded to the nearest 1/max(denominators)."""
    total = Fraction(total_inches)
    sign = "-" if total < 0 else ""
    total = abs(total)

    finest = max(denominators)
    total = Fraction(round(total * finest), finest)

    feet, remaining = divmod(total, 12)
    inches = int(remaining)
    fractional = remaining - inches

    # Smallest denominator that represents the fraction exactly (ties favour simpler fractions).
    fraction = min(
        (Fraction(round(fractional * d), d) for d in denominators),
        key=lambda f: (abs(f - fractional), f.denominator),
    )
    return f"{sign}{int(feet)}' {inches} {fraction}\""
