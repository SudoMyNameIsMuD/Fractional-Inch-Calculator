# Fractional-Inch-Calculator

A desktop calculator for US customary measurements. Enter two values as feet, inches and a fraction of an inch, then add, subtract, multiply or divide them. Results are shown as feet, inches and fractions.

## Run

Requires Python 3 with Tkinter (included in most Python installs).

```
python calculator.py
```

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

## License

GNU General Public License v3.0 – see [LICENSE](LICENSE).

Earlier versions (v2–v8.3) were removed from the tree; they remain in git history and at the `pre-cleanup-v8.4` tag.
