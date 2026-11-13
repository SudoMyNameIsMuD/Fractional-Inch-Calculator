"""Desktop-only integration checks. Run explicitly with python3 tests/gui_smoke.py."""

import runpy
import tempfile
import tkinter as tk
from tkinter import ttk
import unittest
from pathlib import Path
from unittest.mock import patch


APP_PATH = Path(__file__).resolve().parents[1] / "v8.4.py"
Calculator = runpy.run_path(str(APP_PATH))["Calculator"]


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = tk.Tk()
        self.addCleanup(self.root.destroy)
        settings_patch = patch.object(
            Calculator, "CONFIG_FILE", str(Path(self.directory.name) / "settings.ini"))
        settings_patch.start()
        self.addCleanup(settings_patch.stop)
        self.calculator = Calculator(self.root)
        self.root.update()

    def fill_inputs(self):
        for entry, value in (
            (self.calculator.feet_entry, "6"),
            (self.calculator.inches_entry, "2"),
            (self.calculator.fraction_entry, "3/4"),
            (self.calculator.feet_entry2, "1"),
            (self.calculator.fraction_entry2, "23/64"),
        ):
            entry.insert(0, value)

    def test_calculation_copy_and_edit(self):
        self.assertEqual(self.calculator.result_value.cget("text"), Calculator.RESULT_PROMPT)
        self.assertEqual(self.calculator.header_accent.cget("background"),
                         Calculator.ACCENT_COLOR)
        self.assertEqual(self.calculator.result_accent.cget("background"),
                         Calculator.ACCENT_COLOR)
        self.fill_inputs()
        self.calculator.add_button.invoke()
        self.assertEqual(self.calculator.result_value.cget("text"), "7' 3 7/64\"")
        self.assertEqual(self.calculator.result_value.cget("style"), "Result.TLabel")
        self.assertFalse(self.calculator.copy_button.instate(["disabled"]))
        self.calculator.copy_button.invoke()
        self.assertEqual(self.root.clipboard_get(), "7' 3 7/64\"")
        self.assertIn("7' 3 7/64\"", self.calculator.log_text.get("1.0", tk.END))
        self.calculator.feet_entry.insert(tk.END, "1")
        self.assertTrue(self.calculator.copy_button.instate(["disabled"]))
        self.assertEqual(self.calculator.result_value.cget("text"), Calculator.RESULT_PROMPT)

    def test_empty_result_prompt_returns_after_clear(self):
        self.fill_inputs()
        self.calculator.calculate("add")
        self.assertEqual(self.calculator.result_value.cget("text"), "7' 3 7/64\"")
        self.calculator.clear_button.invoke()
        self.assertEqual(self.calculator.result_value.cget("text"), Calculator.RESULT_PROMPT)
        self.assertTrue(self.calculator.copy_button.instate(["disabled"]))

    def test_cursor_selection_and_backspace(self):
        entry = self.calculator.feet_entry
        entry.insert(0, "123")
        self.calculator.set_current_entry(entry)
        entry.icursor(1)
        self.calculator.insert_text("9")
        self.assertEqual(entry.get(), "1923")
        entry.selection_range(1, 3)
        self.calculator.insert_text("7")
        self.assertEqual(entry.get(), "173")
        self.calculator.backspace_button.invoke()
        self.assertEqual(entry.get(), "13")
        entry.selection_range(0, tk.END)
        self.calculator.backspace()
        self.assertEqual(entry.get(), "")
        self.calculator.backspace()
        self.assertEqual(entry.get(), "")

    def test_validation_and_recovery(self):
        entry = self.calculator.fraction_entry
        entry.insert(0, "1/0")
        self.calculator.add_button.invoke()
        self.assertTrue(entry.instate(["invalid"]))
        self.assertIn("Measurement 1, Fraction", self.calculator.status.get())
        self.assertTrue(self.calculator.copy_button.instate(["disabled"]))
        entry.delete(0, tk.END)
        entry.insert(0, "1/2")
        self.calculator.add_button.invoke()
        self.assertFalse(entry.instate(["invalid"]))
        self.assertEqual(self.calculator.result_value.cget("text"), "0' 0 1/2\"")

    def test_clear_keeps_history_and_reset_removes_it(self):
        self.fill_inputs()
        self.calculator.calculate("add")
        history = self.calculator.log_text.get("1.0", tk.END)
        self.calculator.clear_button.invoke()
        self.assertTrue(all(entry.get() == "" for entry in self.calculator.entry_details))
        self.assertEqual(self.calculator.log_text.get("1.0", tk.END), history)
        self.calculator.reset_button.invoke()
        self.assertEqual(self.calculator.log_text.get("1.0", tk.END).strip(), "")

    def test_history_spacing_latest_highlight_and_clear(self):
        self.fill_inputs()
        self.calculator.calculate("add")
        self.calculator.fraction_entry2.delete(0, tk.END)
        self.calculator.fraction_entry2.insert(0, "1/2")
        self.calculator.calculate("subtract")
        log_text = self.calculator.log_text
        latest_range = log_text.tag_ranges("latest")
        self.assertEqual(len(latest_range), 2)
        latest_entry = log_text.get(*latest_range)
        self.assertEqual(log_text.tag_cget("latest", "foreground"),
                         Calculator.ACCENT_COLOR)
        self.assertIn(" - ", latest_entry)
        self.assertTrue(latest_entry.endswith(" = 5' 2 1/4\"\n"))
        self.assertIn("\n\n", log_text.get("1.0", "end-1c"))

        result = self.calculator.result_value.cget("text")
        inputs = [entry.get() for entry in self.calculator.entry_details]
        self.calculator.clear_history_button.invoke()
        self.assertEqual(log_text.get("1.0", "end-1c"), "")
        self.assertEqual(tuple(log_text.tag_ranges("latest")), ())
        self.assertEqual(self.calculator.result_value.cget("text"), result)
        self.assertEqual([entry.get() for entry in self.calculator.entry_details], inputs)
        self.assertEqual(self.calculator.status.get(), "Calculation history cleared.")

    def test_clear_and_reset_are_secondary_and_explain_history(self):
        self.assertEqual(self.calculator.clear_button.cget("style"), "Secondary.TButton")
        self.assertEqual(self.calculator.reset_button.cget("style"), "Secondary.TButton")
        self.assertEqual(
            self.calculator.reset_hint.cget("text"),
            "Clear Inputs keeps history; Reset All clears it.")
        self.root.update()
        self.assertGreaterEqual(self.calculator.clear_button.winfo_height(), 32)
        self.assertGreaterEqual(self.calculator.reset_button.winfo_height(), 32)

    def test_layout_at_minimum_and_larger_size(self):
        self.root.deiconify()
        minimum_width, minimum_height = self.root.minsize()
        for width, height in ((minimum_width, minimum_height), (1100, 850)):
            self.root.geometry(f"{width}x{height}")
            self.root.update()
            for widget in (
                self.calculator.measurement1_frame,
                self.calculator.measurement2_frame,
                self.calculator.number_pad_frame,
                self.calculator.result_value,
                self.calculator.copy_button,
                self.calculator.log_text,
                self.calculator.status_label,
            ):
                with self.subTest(size=(width, height), widget=str(widget)):
                    x = widget.winfo_rootx() - self.root.winfo_rootx()
                    y = widget.winfo_rooty() - self.root.winfo_rooty()
                    self.assertGreaterEqual(x, 0)
                    self.assertGreaterEqual(y, 0)
                    self.assertLessEqual(x + widget.winfo_width(), self.root.winfo_width())
                    self.assertLessEqual(y + widget.winfo_height(), self.root.winfo_height())
        self.assertTrue(self.root.bind("<Return>"))
        self.assertTrue(self.root.bind("<Escape>"))

    def test_measurement_fields_stay_compact_and_aligned(self):
        self.root.deiconify()
        minimum_width, minimum_height = self.root.minsize()
        initial_widths = None
        for width, height in ((minimum_width, minimum_height), (1100, 850)):
            self.root.geometry(f"{width}x{height}")
            self.root.update()
            widths = [entry.winfo_width() for entry in self.calculator.entry_details]
            self.assertEqual(len(set(widths)), 1)
            if initial_widths is None:
                initial_widths = widths
            else:
                self.assertEqual(widths, initial_widths)
            for frame in (self.calculator.measurement1_frame,
                          self.calculator.measurement2_frame):
                entries = [entry for entry in self.calculator.entry_details
                           if entry.master == frame]
                self.assertEqual(len({entry.winfo_x() for entry in entries}), 1)
                self.assertLessEqual(entries[0].winfo_width(), frame.winfo_width() * 0.6)

    def test_keyboard_shortcuts(self):
        self.root.deiconify()
        self.fill_inputs()
        self.calculator.subtract_button.invoke()
        expected = self.calculator.result_value.cget("text")
        self.calculator.feet_entry.focus_force()
        self.root.update()
        self.calculator.feet_entry.event_generate("<Return>")
        self.root.update()
        self.assertEqual(self.calculator.result_value.cget("text"), expected)
        modifier = "Command" if self.root.tk.call("tk", "windowingsystem") == "aqua" else "Control"
        self.calculator.feet_entry.event_generate(f"<{modifier}-Shift-C>")
        self.root.update()
        self.assertEqual(self.root.clipboard_get(), expected)
        self.calculator.feet_entry.event_generate("<Escape>")
        self.root.update()
        self.assertTrue(all(entry.get() == "" for entry in self.calculator.entry_details))

    def test_shortcut_help_is_in_help_menu(self):
        self.assertEqual(self.calculator.help_menu.entrycget(0, "label"),
                         "Keyboard Shortcuts...")
        self.assertIn("Help", self.calculator.menu_bar.entrycget(0, "label"))
        with patch("tkinter.messagebox.showinfo") as showinfo:
            self.calculator.help_menu.invoke(0)
        modifier = "Command" if self.root.tk.call("tk", "windowingsystem") == "aqua" else "Control"
        self.assertEqual(showinfo.call_args.args[0], "Keyboard Shortcuts")
        self.assertIn("Enter: Calculate using the marked operation",
                      showinfo.call_args.args[1])
        self.assertIn(f"{modifier}+Shift+C", showinfo.call_args.args[1])

    def test_active_operation_tracks_clicks_and_enter(self):
        self.assertEqual(self.calculator.add_button.cget("text"), "Add (Enter)")
        self.assertEqual(self.calculator.add_button.cget("style"), "ActiveOperation.TButton")
        for operation, button in self.calculator.operation_buttons.items():
            with self.subTest(operation=operation):
                button.invoke()
                self.assertEqual(self.calculator.last_operation, operation)
                self.assertEqual(button.cget("text"), f"{operation.title()} (Enter)")
                self.assertEqual(button.cget("style"), "ActiveOperation.TButton")
                for other, other_button in self.calculator.operation_buttons.items():
                    if other != operation:
                        self.assertEqual(other_button.cget("text"), other.title())
                        self.assertEqual(other_button.cget("style"), "Operation.TButton")
                self.calculator.repeat_operation()
                self.assertEqual(self.calculator.last_operation, operation)

    def test_operation_and_keypad_buttons_have_balanced_sizes(self):
        self.root.geometry("1100x850")
        self.root.update()
        operation_sizes = {
            (button.winfo_width(), button.winfo_height())
            for button in self.calculator.operation_buttons.values()
        }
        self.assertEqual(len(operation_sizes), 1)
        operation_width, operation_height = operation_sizes.pop()
        self.assertGreaterEqual(operation_width, 120)
        self.assertGreaterEqual(operation_height, 32)
        self.assertGreaterEqual(self.calculator.clear_button.winfo_height(), 32)
        keypad_buttons = [
            child for child in self.calculator.number_pad_frame.winfo_children()
            if isinstance(child, ttk.Button)
        ]
        numeric_sizes = {
            (button.winfo_width(), button.winfo_height())
            for button in keypad_buttons
            if button.cget("text") not in ("-", "Backspace")
        }
        self.assertEqual(len(numeric_sizes), 1)
        keypad_width, keypad_height = numeric_sizes.pop()
        self.assertGreaterEqual(keypad_width, 40)
        self.assertGreaterEqual(keypad_height, 32)
        self.assertLessEqual(operation_width, 220)
        self.assertLessEqual(operation_height, keypad_height + 12)
    def test_settings_round_trip(self):
        self.fill_inputs()
        self.calculator.save_settings()
        for entry in self.calculator.entry_details:
            entry.delete(0, tk.END)
        self.calculator.load_settings()
        self.assertEqual(self.calculator.feet_entry.get(), "6")
        self.assertEqual(self.calculator.fraction_entry2.get(), "23/64")


if __name__ == "__main__":
    unittest.main()
