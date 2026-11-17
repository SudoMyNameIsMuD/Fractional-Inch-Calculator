# Roadmap

Current state: a Tkinter app (`v8.4.py`, ~340 lines, single `Calculator` class) that adds/subtracts two
feet-inch-fraction measurements and persists window/values in `calculator_settings.ini`. A Swift version
also exists. Older versions (`v2`–`v8.3`) are kept as separate files.

## Phase 1 – Repo hygiene
- [x] Promote `v8.4.py` to a single `calculator.py`; remove old version files (tagged `pre-cleanup-v8.4`).
- [x] Rename the `.py` files without spaces/dots so they are importable.
- [x] Add `.gitignore` (ignore `calculator_settings.ini` user state, `__pycache__`).
- [ ] Expand README further: screenshot, usage examples (basic run instructions done).
- [x] Add a LICENSE (GPL-3.0).

## Phase 2 – Separate logic from UI
- [x] Extract parsing/arithmetic/formatting into a pure module (`measure.py`) using `fractions.Fraction`.
- [x] Keep `Calculator` (Tkinter) as a thin view over that module.
- [x] Define clear input validation and error messages (bad fractions, zero denominators, negatives); `MeasurementError` carries the message.

## Phase 3 – Tests and CI
- [ ] `pytest` unit tests: parsing, add/subtract, negative results, rounding to 1/16, 1/32, 1/64, carry from inches to feet.
- [ ] GitHub Actions: lint (ruff) + tests on push/PR.
- [ ] Shared test-case file (JSON) that the Swift version can also check, to keep both in sync.

## Phase 4 – Features
- [ ] Multiply/divide already exist; make them scalar-aware and add chained operations.
- [ ] Selectable precision (1/8 … 1/64) and decimal/metric (mm) display.
- [ ] Accept typed input like `5' 3 1/2"`.
- [ ] Calculation history and copy-result button.
- [ ] Keyboard shortcuts and clear/reset.

## Phase 5 – Distribution
- [ ] Package with PyInstaller; publish binaries via GitHub Releases.
- [ ] Decide long-term fate of the Swift port (maintain with shared tests, or archive).

## Open questions
- Is the target audience woodworkers/builders (precision, speed of entry) or general users?
- Should the Swift app be kept at feature parity?
