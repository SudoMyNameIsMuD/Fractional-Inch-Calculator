# Contributing

Thanks for helping improve Fractional Inch Calculator.

## Project scope

- The Python/Tkinter calculator is the current desktop app and primary
  development focus.
- The SwiftUI source is a prototype for a future iOS app, not a packaged or
  feature-equivalent replacement for the Python app.
- See the [roadmap](ROADMAP.md) before starting a larger change. Open an issue
  to discuss new features or changes to calculation behavior.

## Local setup

Use Python 3 with Tkinter available. No third-party packages are needed for the
app or tests. From the repository directory:

```bash
python3 v8.4.py
```

The app reads and writes `calculator_settings.ini` in the current working
directory. This file is currently tracked; do not include personal input values
or window-position changes in a pull request.

## Run tests

From the repository directory:

```bash
python3 -m unittest discover -s tests -v
```

Tests use the standard-library `unittest` runner and mock Tk widgets. They
require Tkinter to be importable but do not open a window or change saved
settings. They cover parsing, output formatting, the four arithmetic operations,
calculation log contents, and invalid input handling.

The Python entry point has a versioned filename, so the tests load it with
`runpy.run_path`. Importing it must not start the app.

For real-widget interface tests, run the following in a desktop session:

```bash
python3 tests/gui_smoke.py -v
```

These tests briefly open a window, exercise the clipboard, and check keypad
editing, validation, clearing/resetting, shortcuts, settings, and widget bounds
at minimum and larger window sizes. They use temporary settings files. Do not
run them on a headless machine without a display server.

## Making changes

1. Create a focused branch from the branch your pull request will target.
2. Keep changes small and related to one purpose.
3. Add or update tests when changing calculation behavior.
4. Run the tests and `git diff --check`.
5. For interface changes, also launch the app and check input focus, keypad
   behavior, results, history, resizing, and closing/reopening.
6. Update the README and the Unreleased changelog entry when behavior changes.

The current tests preserve existing behavior; they do not prove all arithmetic
edge cases are correct. Negative-result formatting, rounding across whole-inch
boundaries, and exact rational arithmetic still need additional work.

Multiplication and division currently operate on total-inch numeric values and
display their outputs as lengths. Discuss units and any intentional behavior
change before revising those operations.

## Reporting bugs

Include:

- Your operating system, Python version, and how you launched the app.
- The feet, inches, and fraction values entered into both measurements.
- The operation, expected result, and actual result or error message.
- Steps to reproduce, and a screenshot if the problem is visual.

## Pull requests

Describe the problem, your change, and how you tested it. Include before/after
screenshots for visible interface changes. Avoid unrelated formatting changes,
generated files, local environments, and personal settings.

## License status

This repository does not yet include a license. Do not assume it grants
open-source redistribution rights; licensing must be decided by the project
owner before publishing under an open-source license.
