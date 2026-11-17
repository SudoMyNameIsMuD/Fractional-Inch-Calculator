# Roadmap

Current state: a Tkinter app (`v8.4.py`, ~340 lines, single `Calculator` class) that adds/subtracts two
feet-inch-fraction measurements and persists window/values in `calculator_settings.ini`. A Swift version
also exists. Older versions (`v2`–`v8.3`) are kept as separate files.

## Phase 1 – Repo hygiene
- [x] Promote `v8.4.py` to a single `calculator.py`; remove old version files (tagged `pre-cleanup-v8.4`).
- [x] Rename the `.py` files without spaces/dots so they are importable.
- [x] Add `.gitignore` (ignore `calculator_settings.ini` user state, `__pycache__`).
- [x] Expand README: screenshot, usage examples, run instructions.
- [x] Add a LICENSE (GPL-3.0).

## Phase 2 – Separate logic from UI
- [x] Extract parsing/arithmetic/formatting into a pure module (`measure.py`) using `fractions.Fraction`.
- [x] Keep `Calculator` (Tkinter) as a thin view over that module.
- [x] Define clear input validation and error messages (bad fractions, zero denominators, negatives); `MeasurementError` carries the message.

## Phase 3 – Tests and CI
- [x] `pytest` unit tests: parsing, add/subtract, negative results, rounding to 1/16, 1/32, 1/64, carry from inches to feet.
- [x] GitHub Actions: lint (ruff) + tests on push/PR.
- [x] Shared test-case file (`tests/cases.json`) created; [ ] wire the Swift version up to it.

## Phase 4 – Features
- [x] Multiply/divide treat Measurement 2 as a plain factor; "Use Result" chains operations.
- [x] Selectable precision (1/2 … 1/256) and decimal/metric (mm) display.
- [x] Accept typed input like `5' 3 1/2"`.
- [x] Calculation log and copy-result button (already present).
- [x] Keyboard shortcuts and clear/reset.

## Phase 5 – Distribution
- [x] PyInstaller packaging and release workflow prepared (not yet released; tag `v*` to publish).
- [ ] Decide long-term fate of the Swift port (maintain with shared tests, or archive).

## Open questions
- Is the target audience woodworkers/builders (precision, speed of entry) or general users?
- Should the Swift app be kept at feature parity?
