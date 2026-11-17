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
