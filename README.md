# Fractional-Inch-Calculator

Version 1.0.0 (version is defined in `measure.py` as `__version__`; release tags are `v<version>`).

A desktop calculator for US customary measurements. Enter two values as feet, inches and a fraction of an inch, then add, subtract, multiply or divide them. Results are shown as feet, inches and fractions.

## Run

Requires Python 3 with Tkinter (included in most Python installs).

```
python calculator.py
```

Features:
- Enter values in the feet/inches/fraction fields, or type a measurement such as `5' 3 1/2"`, `3-1/2"` or `10.5in` in "Or type" and press Enter.
- Multiply and divide treat Measurement 2 as a plain number (e.g. `6' 2 1/4"` × `2` – enter 2 in the inches field).
- **Use Result** moves the last result into Measurement 1 for chained calculations.
- Choose precision (1/2 to 1/256) and display units (feet-inches, decimal inches, millimeters).
- Shortcuts: `Ctrl+1/2/3/4` add/subtract/multiply/divide, `Ctrl+U` use result, `Ctrl+Shift+C` copy result, `Ctrl+Delete` clear.

Window size and the last entered values are saved to `calculator_settings.ini` (created on first close, git-ignored).

## Files

- `calculator.py` – Tkinter UI.
- `measure.py` – GUI-free parsing, arithmetic and formatting (exact `Fraction` math).
- `Fractional-Inch-Calculator.swift` – Swift version.
- `ROADMAP.md` – planned improvements.

## Development

```
pip install -r requirements-dev.txt
ruff check .
pytest
```

## Building a release

Binaries are built with PyInstaller (`pip install pyinstaller`):

```
pyinstaller --noconfirm --onefile --windowed --name FractionalInchCalculator calculator.py
```

The `Build release binaries` workflow does this for Linux, Windows and macOS. Running it manually (Actions tab) only produces downloadable artifacts. Pushing a tag like `v1.0.0` also publishes a GitHub Release. Packaged builds store settings in the user config folder (`%APPDATA%` or `~/.config`).

## License

GNU General Public License v3.0 – see [LICENSE](LICENSE).

Earlier versions (v2–v8.3) were removed from the tree; they remain in git history and at the `pre-cleanup-v8.4` tag.
