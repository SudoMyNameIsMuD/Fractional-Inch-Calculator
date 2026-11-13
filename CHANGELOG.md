# Changelog

Notable project changes are recorded here. Entries describe repository changes;
they do not imply that a packaged application release has been published.

## [Unreleased]

- Added a restrained blue accent to the heading and result markers, active
  operation, and newest history entry while retaining native controls.
- Marked the active operation with `(Enter)` and a bold label
  so the keyboard's repeat behavior is visible.
- Centered the operation controls with consistent widths and comfortable
  button padding; kept keypad keys evenly sized.
- Added an empty-result prompt that returns after edits or clearing; successful
  answers remain visually emphasized.
- De-emphasized Clear Inputs and Reset All relative to calculation actions, and
  added an inline note clarifying that Reset All clears history.
- Moved the visible shortcut instructions into a native Help menu dialog to
  reduce clutter around the calculator controls.
- Added paragraph spacing and a bold highlight for the newest history entry, plus
  a separate Clear History action that keeps inputs and the current result.
- Added a larger, bold interface title and a short explanatory subtitle.
- Kept measurement fields compact at larger window sizes, aligned field labels
  consistently, and shortened the fraction hint.
- Reworked the Tkinter interface with native themed controls, paired measurement
  panels, a larger result, resizable history, and a minimum usable window size.
- Added cursor-aware keypad insertion, selection replacement, a minus key, and
  Backspace.
- Added Enter to repeat the last operation, Escape to clear inputs, and
  Cmd/Ctrl+Shift+C to copy a valid result.
- Added field-specific validation messages and invalid field states without
  forcing white entry backgrounds; editing inputs clears stale results.
- Disabled copying until a calculation succeeds and clarified Clear Inputs
  versus Reset All.
- Added desktop-only real-widget checks for layout, editing, validation,
  clipboard, shortcuts, and settings alongside the non-GUI regression tests.
- Added project documentation for setup, usage, current limitations, and planned
  work.
- Added standard-library regression tests for measurement parsing, formatting,
  arithmetic, calculation logs, and invalid input handling.
- Guarded Python app startup so loading the module for tests does not open a
  window; the direct launch command remains unchanged.
- Added a `.gitignore` for Python caches, local environments, build output, and
  editor-local files.
- Added contribution guidelines and clarified that Python is the primary app
  while SwiftUI is a prototype for a future iOS app.

## [v.0.0.2]

- Removed superseded Python calculator versions from this branch, retaining
  `v8.4.py` as the current Python app.
