import json
import pathlib

import pytest

import measure

CASES = json.loads((pathlib.Path(__file__).parent / "cases.json").read_text())


def run(case):
    a = measure.to_inches(*case["a"])
    b = measure.to_inches(*case["b"])
    return measure.format_measurement(measure.calculate(case["op"], a, b))


@pytest.mark.parametrize("case", CASES["calculations"], ids=lambda c: f"{c['op']}-{c['expected']}")
def test_calculations(case):
    assert run(case) == case["expected"]


@pytest.mark.parametrize("case", CASES["errors"], ids=lambda c: c["message"][:20] + "-" + c["op"])
def test_errors(case):
    with pytest.raises(measure.MeasurementError) as exc:
        run(case)
    assert str(exc.value) == case["message"]


def test_arithmetic_is_exact():
    assert measure.to_inches("", "", "1/3") * 3 == 1


def test_coarser_denominators_preferred_on_exact_values():
    assert measure.format_measurement(measure.to_inches("", "", "8/16")) == "0' 0 1/2\""


@pytest.mark.parametrize(
    "text, inches",
    [("5' 3 1/2\"", "127/2"), ("3-1/2\"", "7/2"), ("10.5in", "21/2"), ("2ft", "24"), ("-3/4\"", "-3/4"), ("1' 1/2", "25/2")],
)
def test_parse_typed(text, inches):
    assert measure.parse_typed(text) == measure.Fraction(inches)


@pytest.mark.parametrize("text", ["", "abc", "1/0"])
def test_parse_typed_rejects_bad_input(text):
    with pytest.raises(measure.MeasurementError):
        measure.parse_typed(text)


def test_split_inches_round_trips_including_negatives():
    for total in (measure.Fraction(127, 2), measure.Fraction(-29, 2), measure.Fraction(0)):
        assert measure.to_inches(*measure.split_inches(total)) == total


def test_display_units_and_precision():
    assert measure.format_result(74, "Millimeters") == "1879.6 mm"
    assert measure.format_result(measure.Fraction(37, 2), "Decimal inches") == '18.500"'
    assert measure.format_result(measure.Fraction(1, 3), precision=16) == "0' 0 5/16\""
