# Fractional Inch Calculator

A small desktop calculator for measurements in feet, inches, and fractional
inches. The current desktop app is written in Python with Tkinter.

> **Project status:** The Python calculator is usable locally and is still in
> development. It is not currently packaged as an installer or standalone Mac
> app. Python is the primary app; the Swift file is a prototype for a future iOS
> app. This repository does not yet contain an Xcode project.

## Features

- Enter two measurements as feet, whole inches, and a fraction of an inch.
- Add, subtract, multiply, and divide measurements.
- View results formatted as feet, inches, and a fraction.
- Format output using common fraction denominators up to 1/256.
- Use an on-screen number pad, copy the result, and review spaced calculation
  history with the newest calculation highlighted.
- Clear history independently without clearing measurements or the current result.
- Restore the window size and input values from a settings file.
- Resize a compact native interface with a prominent result and visible history.
- Use a centered, fixed-width operation group and evenly sized keypad buttons.
- See a clear prompt before calculating, with successful answers emphasized.
- Follow the blue accent through the heading, active operation, result, and newest history entry.
- Edit at the cursor with the keypad, replace selected text, and use Backspace.

## Requirements

- Python 3
- Tkinter, which is included with many Python installations

The app uses only Python standard-library modules; no third-party packages are
required.

On macOS, if the app fails to start with a Tkinter-related error, install or
select a Python distribution that includes Tk support.

## Run locally

Open Terminal, change to the project directory, and start the Python app:

```bash
cd "/path/to/Fractional-Inch-Calculator"
python3 v8.4.py
```

The calculator window should open. Close it using the window's close button;
the app saves its window geometry and current input values to
`calculator_settings.ini` in the current working directory.

## Input format

Enter each measurement in three fields:

| Field | Example |
| --- | --- |
| Feet | `6` |
| Inches | `2` |
| Fraction | `3/4` |

Use whole numbers for feet and inches, and a fraction such as `1/2` or `23/64`
for the fractional-inch field. Leave a field blank when its value is zero.

Invalid fields are marked when leaving them or calculating, with a message
identifying the measurement and field. Editing an input clears the previous
result so an outdated answer cannot be copied.

### Keyboard and controls

- **Enter:** calculate using the last operation (Add initially).
- **Escape / Clear Inputs:** clear both measurements and the result, keeping history.
- **Reset All:** clear inputs, result, and history; saved preferences are not reset.
  The interface distinguishes these secondary actions and notes that Reset All
  also clears history.
- **Clear History:** clear only the calculation log, keeping inputs and the result.
- **Cmd+Shift+C** on macOS, or **Ctrl+Shift+C** elsewhere: copy a valid result.
- **Tab / Shift+Tab:** navigate fields and controls.

The keypad edits the last selected input at its cursor and replaces any selected
text. Copy Result is available only after a successful calculation.
The active operation is marked with `(Enter)` and a bold label.
Clicking another operation updates the marker, even if inputs need
correction, so Enter repeats that operation after editing.
In the app, choose **Help → Keyboard Shortcuts...** to view the shortcuts.

## Repository contents

| File | Purpose |
| --- | --- |
| `v8.4.py` | Current Python/Tkinter desktop calculator |
| `Fractional-Inch-Calculator.swift` | Separate SwiftUI calculator prototype |
| `calculator_settings.ini` | Sample/default window and input settings |
| `CHANGELOG.md` | Recorded project changes |
| `ROADMAP.md` | Planned improvements |
| `CONTRIBUTING.md` | Setup, testing, bug reports, and contribution guidelines |
| `tests/` | Automated Python regression tests |

## Tests and contributions

From the repository directory, run the standard-library test suite:

```bash
python3 -m unittest discover -s tests -v
```

Tests require Tkinter to be importable but do not open a window. See
[CONTRIBUTING.md](CONTRIBUTING.md) for development and contribution instructions.

To also check real Tk widgets, resizing, shortcuts, and clipboard behavior on a
desktop session:

```bash
python3 tests/gui_smoke.py -v
```

These checks briefly open a window and use the clipboard. They use temporary
settings files rather than changing your saved inputs.

## Known limitations

- Calculation values are converted to floating-point numbers internally, so
  some results may be rounded when formatted.
- Settings are stored relative to the directory from which the app is run.
- Multiplication and division treat both inputs as total-inch numeric values
  and display the result as a length, rather than area or a unitless ratio.
- Negative-result formatting and rounding at whole-inch boundaries need more
  work; the current tests do not cover every arithmetic edge case.
- There is no packaged app yet.

## License

A license has not yet been selected. No open-source license is currently
granted by this repository.

See [ROADMAP.md](ROADMAP.md) for planned improvements and [CHANGELOG.md](CHANGELOG.md)
for recorded changes.
