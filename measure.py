"""Pure measurement logic (no GUI): parsing, arithmetic and formatting in inches."""
import re
from fractions import Fraction

__version__ = "1.0.0"

FRACTION_DENOMINATORS = [2, 4, 8, 16, 32, 64, 128, 256]
UNITS = ["Feet-inches", "Decimal inches", "Millimeters"]
MM_PER_INCH = Fraction(254, 10)
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


def denominators_for(precision):
    """Allowed fraction denominators up to 1/precision (e.g. 16 -> 2, 4, 8, 16)."""
    return [d for d in FRACTION_DENOMINATORS if d <= precision]


def format_decimal(total_inches, places=3):
    return f"{float(total_inches):.{places}f}\""


def format_metric(total_inches, places=1):
    return f"{float(Fraction(total_inches) * MM_PER_INCH):.{places}f} mm"


def format_result(total_inches, unit="Feet-inches", precision=256):
    """Formats a result in the chosen display unit."""
    if unit == "Decimal inches":
        return format_decimal(total_inches)
    if unit == "Millimeters":
        return format_metric(total_inches)
    return format_measurement(total_inches, denominators_for(precision))


def format_number(value):
    """Formats a unitless factor (used for the second operand of multiply/divide)."""
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else f"{float(value):.4g}"


def split_inches(total_inches, denominators=FRACTION_DENOMINATORS):
    """Splits inches into (feet, inches, fraction string) entry values; the sign is applied to each non-zero part."""
    total = Fraction(total_inches)
    sign = -1 if total < 0 else 1
    finest = max(denominators)
    total = Fraction(round(abs(total) * finest), finest)
    feet, remaining = divmod(total, 12)
    inches = int(remaining)
    fraction = remaining - inches

    def signed(n):
        return str(sign * n) if n else ""

    return signed(int(feet)), signed(inches), (str(sign * fraction) if fraction else "")


_TYPED = re.compile(
    r"""^\s*(?P<sign>[-+])?\s*
    (?:(?P<feet>\d+(?:\.\d+)?)\s*(?:'|ft|feet)\s*)?
    (?:(?P<whole>\d+)(?:\s+|-)(?P<mixed>\d+\s*/\s*\d+)
      |(?P<frac>\d+\s*/\s*\d+)
      |(?P<inch>\d+(?:\.\d+)?))?
    \s*(?:"|in|inches)?\s*$""",
    re.VERBOSE | re.IGNORECASE,
)


def parse_typed(text):
    """Parses free-form text like 5' 3 1/2", 3-1/2", 10.5in or 2ft into exact inches."""
    m = _TYPED.match(text)
    if not text.strip() or not m or not any(m.group(g) for g in ("feet", "whole", "frac", "inch")):
        raise MeasurementError("Could not read that measurement. Try something like 5' 3 1/2\".")
    try:
        total = Fraction(m.group("feet") or 0) * 12
        if m.group("whole"):
            total += int(m.group("whole")) + Fraction(m.group("mixed").replace(" ", ""))
        elif m.group("frac"):
            total += Fraction(m.group("frac").replace(" ", ""))
        elif m.group("inch"):
            total += Fraction(m.group("inch"))
    except ZeroDivisionError:
        raise MeasurementError("Invalid fraction. Denominator cannot be zero.") from None
    return -total if m.group("sign") == "-" else total
