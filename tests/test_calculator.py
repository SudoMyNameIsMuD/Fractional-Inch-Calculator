import runpy
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


APP_PATH = Path(__file__).resolve().parents[1] / "v8.4.py"

with patch("tkinter.Tk") as create_window:
    Calculator = runpy.run_path(str(APP_PATH))["Calculator"]
    create_window.assert_not_called()


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        # Exercise the existing callbacks without creating a Tk window.
        self.calculator = Calculator.__new__(Calculator)
        self.calculator.result_value = Mock(spec=["config", "configure"])
        self.calculator.placeholder_font = "placeholder"
        self.calculator.result_font = "result"
        self.calculator.log_calculation = Mock()
        self.calculator.copy_button = Mock(spec=["state"])
        self.calculator.status = Mock(spec=["set"])
        self.calculator.entry_details = {}
        self.calculator.has_result = False
        self.calculator.operation_buttons = {}
        self.set_inputs(("", "", ""), ("", "", ""))

    def set_inputs(self, first, second):
        for names, values in (
            (("feet_entry", "inches_entry", "fraction_entry"), first),
            (("feet_entry2", "inches_entry2", "fraction_entry2"), second),
        ):
            for name, value in zip(names, values):
                entry = Mock(spec=["get"])
                entry.get.return_value = value
                setattr(self.calculator, name, entry)

    def test_parse_measurement(self):
        cases = [
            (("", "", ""), 0),
            (("6", "2", "3/4"), 74.75),
            (("", "", "23/64"), 23 / 64),
            (("", "14", ""), 14),
            (("", "", "3/2"), 1.5),
            (("", "", "0.5"), 0.5),
            (("-1", "", ""), -12),
        ]
        for fields, expected in cases:
            with self.subTest(fields=fields):
                self.set_inputs(fields, ("", "", ""))
                value = self.calculator._get_value(
                    self.calculator.feet_entry,
                    self.calculator.inches_entry,
                    self.calculator.fraction_entry,
                )
                self.assertEqual(value, expected)

    def test_invalid_input_reports_error_without_logging(self):
        cases = [
            (("abc", "", ""), "Invalid input. Please enter valid numbers and fractions."),
            (("", "1.5", ""), "Invalid input. Please enter valid numbers and fractions."),
            (("", "", "1/"), "Invalid input. Please enter valid numbers and fractions."),
            (("", "", "1/0"), "Invalid fraction. Denominator cannot be zero."),
        ]
        for fields, message in cases:
            for invalid_operand in (0, 1):
                with self.subTest(fields=fields, invalid_operand=invalid_operand):
                    operands = [("", "", ""), ("", "", "")]
                    operands[invalid_operand] = fields
                    self.set_inputs(*operands)
                    self.calculator.result_value.reset_mock()
                    self.calculator.calculate("add")
                    self.calculator.result_value.config.assert_called_once_with(text=message)
                    self.calculator.log_calculation.assert_not_called()

    def test_format_measurement(self):
        cases = [
            (0, "0' 0 0\""),
            (12, "1' 0 0\""),
            (14, "1' 2 0\""),
            (74.75, "6' 2 3/4\""),
            (87.109375, "7' 3 7/64\""),
            (1 / 256, "0' 0 1/256\""),
            (1 / 1024, "0' 0 0\""),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(self.calculator._format_measurement(value), expected)

    def test_arithmetic_and_log(self):
        cases = [
            ("add", ("6", "2", "3/4"), ("1", "", "23/64"),
             "7' 3 7/64\"", "6' 2 3/4\" + 1' 0 23/64\" = 7' 3 7/64\"\n"),
            ("subtract", ("1", "", ""), ("", "1", "1/2"),
             "0' 10 1/2\"", "1' 0 0\" - 0' 1 1/2\" = 0' 10 1/2\"\n"),
            ("multiply", ("", "2", ""), ("", "3", ""),
             "0' 6 0\"", "0' 2 0\" * 0' 3 0\" = 0' 6 0\"\n"),
            ("divide", ("", "6", ""), ("", "2", ""),
             "0' 3 0\"", "0' 6 0\" / 0' 2 0\" = 0' 3 0\"\n"),
        ]
        for operation, first, second, result, log in cases:
            with self.subTest(operation=operation):
                self.set_inputs(first, second)
                self.calculator.result_value.reset_mock()
                self.calculator.log_calculation.reset_mock()
                self.calculator.calculate(operation)
                self.calculator.result_value.config.assert_called_once_with(text=result)
                self.calculator.log_calculation.assert_called_once_with(log)

    def test_divide_by_zero_reports_error_without_logging(self):
        self.set_inputs(("1", "", ""), ("", "", ""))
        self.calculator.calculate("divide")
        self.calculator.result_value.config.assert_called_once_with(text="Cannot divide by zero")
        self.calculator.log_calculation.assert_not_called()

    def test_unknown_operation_reports_error_without_logging(self):
        self.calculator.calculate("unknown")
        self.calculator.result_value.config.assert_called_once_with(text="Invalid operation")
        self.calculator.log_calculation.assert_not_called()

    def test_keypad_inserts_at_cursor(self):
        entry = Mock()
        entry.selection_present.return_value = False
        self.calculator.current_entry = entry
        self.calculator.insert_text("7")
        entry.insert.assert_called_once_with("insert", "7")
        entry.delete.assert_not_called()
        entry.focus_set.assert_called_once_with()

    def test_keypad_replaces_selection(self):
        entry = Mock()
        entry.selection_present.return_value = True
        self.calculator.current_entry = entry
        self.calculator.insert_text("3/4")
        entry.delete.assert_called_once_with("sel.first", "sel.last")
        entry.insert.assert_called_once_with("insert", "3/4")

    def test_backspace_at_cursor_and_start(self):
        for position in (0, 3):
            with self.subTest(position=position):
                entry = Mock()
                entry.selection_present.return_value = False
                entry.index.return_value = position
                self.calculator.current_entry = entry
                self.calculator.backspace()
                if position:
                    entry.delete.assert_called_once_with(position - 1, position)
                else:
                    entry.delete.assert_not_called()

    def test_backspace_deletes_selection(self):
        entry = Mock()
        entry.selection_present.return_value = True
        self.calculator.current_entry = entry
        self.calculator.backspace()
        entry.delete.assert_called_once_with("sel.first", "sel.last")

    def test_edit_invalidates_result(self):
        entry = Mock()
        self.calculator.has_result = True
        self.calculator.input_changed(entry)
        self.assertFalse(self.calculator.has_result)
        self.calculator.copy_button.state.assert_called_once_with(["disabled"])
        self.calculator.result_value.config.assert_called_once_with(
            text=Calculator.RESULT_PROMPT)

    def test_copy_without_result_does_not_touch_clipboard(self):
        self.calculator.master = Mock()
        self.calculator.copy_result()
        self.calculator.master.clipboard_clear.assert_not_called()
        self.calculator.status.set.assert_called_once_with(
            "Calculate a valid result before copying.")

    def test_validation_identifies_field_without_logging(self):
        entry = Mock()
        entry.get.return_value = "1/0"
        self.calculator.entry_details = {
            entry: ("Measurement 1, Fraction",
                    self.calculator.validate_fraction_input,
                    "Use a fraction such as 3/4 (denominator cannot be zero)."),
        }
        self.calculator.calculate("add")
        entry.state.assert_called_with(["invalid"])
        entry.focus_set.assert_called_once_with()
        self.assertIn("Measurement 1, Fraction", self.calculator.status.set.call_args.args[0])
        self.calculator.log_calculation.assert_not_called()
        self.assertFalse(self.calculator.has_result)

    def test_validation_allows_blank_and_valid_values(self):
        for value in ("", "0", "-2"):
            self.assertTrue(self.calculator.validate_integer_input(value))
        for value in ("", "3/4", "0.5"):
            self.assertTrue(self.calculator.validate_fraction_input(value))
        self.assertFalse(self.calculator.validate_integer_input("1.5"))
        for value in ("1/", "1/0", "abc"):
            self.assertFalse(self.calculator.validate_fraction_input(value))

    def test_enter_repeats_last_operation(self):
        self.calculator.last_operation = "subtract"
        self.calculator.calculate = Mock()
        self.assertEqual(self.calculator.repeat_operation(), "break")
        self.calculator.calculate.assert_called_once_with("subtract")

    def test_select_operation_marks_only_active_button(self):
        buttons = {name: Mock(spec=["configure"])
                   for name in ("add", "subtract", "multiply", "divide")}
        self.calculator.operation_buttons = buttons
        self.calculator.select_operation("subtract")
        self.assertEqual(self.calculator.last_operation, "subtract")
        for name, button in buttons.items():
            button.configure.assert_called_once_with(
                text="Subtract (Enter)" if name == "subtract" else name.title(),
                style="ActiveOperation.TButton" if name == "subtract" else "Operation.TButton")


if __name__ == "__main__":
    unittest.main()
