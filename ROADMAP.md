# Roadmap

This roadmap is directional; priorities may change as the app is used.

## 1. Improve calculation correctness

- Keep measurements as exact rational values throughout calculations instead
  of converting to floating point.
- Define and test how results are rounded to the selected fractional-inch
  precision.
- Cover negative results, carry/borrow across inches and feet, and division by
  zero.

## 2. Improve input and error feedback

- Field-specific validation, cursor-aware keypad editing, and stale-result
  protection are implemented.
- Refine feedback using real-world input examples and accessibility checks.

## 3. Polish the desktop interface

- The native layout now resizes, highlights the result, and keeps history
  visible; keyboard shortcuts cover repeating an operation, clearing, and copying.
- Check readability and keyboard navigation across supported desktop platforms
  and display scaling settings.

## 4. Expand automated tests

- Initial regression tests are in place; run
  `python3 -m unittest discover -s tests -v`.
- Separate measurement parsing, arithmetic, and formatting from the Tkinter
  interface.
- Expand edge-case coverage for negative results and rounding boundaries.
- Add automated checks in continuous integration.

## 5. Improve settings and app delivery

- Store settings in a predictable per-user location rather than depending on
  the launch directory.
- Add a proper application icon and package the Python app for macOS.
- Document installation, upgrades, and any platform-specific requirements.

## 6. Develop the future iOS app

- Keep Python as the primary desktop app.
- Evolve the SwiftUI prototype into an iOS app with a proper Xcode project.
- Add iOS app icons, device/simulator testing, and installation documentation.
