import configparser  # For persistent settings
import os  # To check if the config file exists
import sys
import tkinter as tk
from tkinter import ttk

import measure


def default_config_path():
    """Settings live beside the script when run from source, or in the user's config dir in a packaged build."""
    name = "calculator_settings.ini"
    if not getattr(sys, "frozen", False):
        return name
    base = os.environ.get("APPDATA") or os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    folder = os.path.join(base, "FractionalInchCalculator")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, name)


class Calculator:
    CONFIG_FILE = default_config_path()  # Filename for settings

    def __init__(self, master):
        self.master = master
        master.title(f"US Customary Units Calculator v{measure.__version__}")

        # --- Load Settings Object ---
        self.config = configparser.ConfigParser()

        # --- Measurement 1 Frame ---
        self.measurement1_frame = ttk.LabelFrame(master, text="Measurement 1")
        self.measurement1_frame.grid(row=0, column=0, padx=5, pady=5, columnspan=4)

        self.feet_label = ttk.Label(self.measurement1_frame, text="Feet:")
        self.feet_label.grid(row=0, column=0, padx=5, pady=5)
        self.feet_entry = ttk.Entry(self.measurement1_frame, width=10, takefocus=True,
                                    validate="focusout",  # Changed to "focusout"
                                    validatecommand=(master.register(self.validate_integer_input), "%P"),
                                    invalidcommand=lambda: self.set_entry_background(self.feet_entry, "red"))
        self.feet_entry.grid(row=0, column=1, padx=5, pady=5)

        self.inches_label = ttk.Label(self.measurement1_frame, text="Inches:")
        self.inches_label.grid(row=1, column=0, padx=5, pady=5)
        self.inches_entry = ttk.Entry(self.measurement1_frame, width=10, takefocus=True,
                                      validate="focusout",  # Changed to "focusout"
                                      validatecommand=(master.register(self.validate_integer_input), "%P"),
                                      invalidcommand=lambda: self.set_entry_background(self.inches_entry, "red"))
        self.inches_entry.grid(row=1, column=1, padx=5, pady=5)

        self.fraction_label = ttk.Label(self.measurement1_frame, text="Fraction (e.g., 1/2):")
        self.fraction_label.grid(row=2, column=0, padx=5, pady=5)
        self.fraction_entry = ttk.Entry(self.measurement1_frame, width=10, takefocus=True,
                                        validate="focusout",  # Changed to "focusout"
                                        validatecommand=(master.register(self.validate_fraction_input), "%P"),
                                        invalidcommand=lambda: self.set_entry_background(self.fraction_entry, "red"))
        self.fraction_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.measurement1_frame, text="Or type:").grid(row=3, column=0, padx=5, pady=5)
        self.typed_entry = ttk.Entry(self.measurement1_frame, width=14)
        self.typed_entry.grid(row=3, column=1, padx=5, pady=5)
        self.typed_entry.bind(
            "<Return>",
            lambda event: self.apply_typed(self.typed_entry, self.feet_entry, self.inches_entry, self.fraction_entry),
        )

        # --- Measurement 2 Frame ---
        self.measurement2_frame = ttk.LabelFrame(master, text="Measurement 2")
        self.measurement2_frame.grid(row=0, column=5, padx=5, pady=5, columnspan=4)

        self.feet_label2 = ttk.Label(self.measurement2_frame, text="Feet:")
        self.feet_label2.grid(row=0, column=0, padx=5, pady=5)
        self.feet_entry2 = ttk.Entry(self.measurement2_frame, width=10, takefocus=True,
                                     validate="focusout",  # Changed to "focusout"
                                     validatecommand=(master.register(self.validate_integer_input), "%P"),
                                     invalidcommand=lambda: self.set_entry_background(self.feet_entry2, "red"))
        self.feet_entry2.grid(row=0, column=1, padx=5, pady=5)

        self.inches_label2 = ttk.Label(self.measurement2_frame, text="Inches:")
        self.inches_label2.grid(row=1, column=0, padx=5, pady=5)
        self.inches_entry2 = ttk.Entry(self.measurement2_frame, width=10, takefocus=True,
                                       validate="focusout",  # Changed to "focusout"
                                       validatecommand=(master.register(self.validate_integer_input), "%P"),
                                       invalidcommand=lambda: self.set_entry_background(self.inches_entry2, "red"))
        self.inches_entry2.grid(row=1, column=1, padx=5, pady=5)

        self.fraction_label2 = ttk.Label(self.measurement2_frame, text="Fraction (e.g., 1/2):")
        self.fraction_label2.grid(row=2, column=0, padx=5, pady=5)
        self.fraction_entry2 = ttk.Entry(self.measurement2_frame, width=10, takefocus=True,
                                         validate="focusout",  # Changed to "focusout"
                                         validatecommand=(master.register(self.validate_fraction_input), "%P"),
                                         invalidcommand=lambda: self.set_entry_background(self.fraction_entry2, "red"))
        self.fraction_entry2.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.measurement2_frame, text="Or type:").grid(row=3, column=0, padx=5, pady=5)
        self.typed_entry2 = ttk.Entry(self.measurement2_frame, width=14)
        self.typed_entry2.grid(row=3, column=1, padx=5, pady=5)
        self.typed_entry2.bind(
            "<Return>",
            lambda event: self.apply_typed(self.typed_entry2, self.feet_entry2, self.inches_entry2, self.fraction_entry2),
        )

        # Buttons
        self.add_button = ttk.Button(master, text="Add", command=lambda: self.calculate("add"))
        self.add_button.grid(row=3, column=0, padx=5, pady=5)

        self.subtract_button = ttk.Button(master, text="Subtract", command=lambda: self.calculate("subtract"))
        self.subtract_button.grid(row=3, column=1, padx=5, pady=5)

        self.multiply_button = ttk.Button(master, text="Multiply", command=lambda: self.calculate("multiply"))
        self.multiply_button.grid(row=3, column=2, padx=5, pady=5)

        self.divide_button = ttk.Button(master, text="Divide", command=lambda: self.calculate("divide"))
        self.divide_button.grid(row=3, column=3, padx=5, pady=5)

        self.clear_button = ttk.Button(master, text="Clear", command=self.clear_fields)
        self.clear_button.grid(row=4, column=1, padx=5, pady=5)

        self.reset_button = ttk.Button(master, text="Reset All", command=self.reset_all)  # Reset All button
        self.reset_button.grid(row=4, column=2, padx=5, pady=5)

        self.use_result_button = ttk.Button(master, text="Use Result", command=self.use_result)
        self.use_result_button.grid(row=4, column=0, padx=5, pady=5)

        # Display options
        self.precision_var = tk.StringVar(value="1/256")
        self.units_var = tk.StringVar(value=measure.UNITS[0])
        ttk.Label(master, text="Precision:").grid(row=6, column=0, padx=5, pady=5)
        self.precision_box = ttk.Combobox(master, textvariable=self.precision_var, width=8, state="readonly",
                                          values=[f"1/{d}" for d in measure.FRACTION_DENOMINATORS])
        self.precision_box.grid(row=6, column=1, padx=5, pady=5)
        ttk.Label(master, text="Units:").grid(row=6, column=2, padx=5, pady=5)
        self.units_box = ttk.Combobox(master, textvariable=self.units_var, width=14, state="readonly", values=measure.UNITS)
        self.units_box.grid(row=6, column=3, padx=5, pady=5)
        self.precision_box.bind("<<ComboboxSelected>>", lambda event: self.refresh_result())
        self.units_box.bind("<<ComboboxSelected>>", lambda event: self.refresh_result())

        self.last_total = None  # Exact inches of the most recent result

        # Result
        self.result_label = ttk.Label(master, text="Result:")
        self.result_label.grid(row=5, column=0, padx=5, pady=5)
        self.result_value = ttk.Label(master, text="")
        self.result_value.grid(row=5, column=1, padx=5, pady=5)

        self.copy_button = ttk.Button(master, text="Copy Result", command=self.copy_result)
        self.copy_button.grid(row=5, column=2, padx=5, pady=5)

        # --- Number Pad ---
        self.number_pad_frame = ttk.Frame(master)
        self.number_pad_frame.grid(row=3, column=5, rowspan=3, padx=5, pady=5)

        self.current_entry = None  # To keep track of which entry is currently selected

        # Create number buttons
        numbers = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '/', '.'
        ]
        row_val = 0
        col_val = 0
        for button_text in numbers:
            ttk.Button(self.number_pad_frame, text=button_text, width=4,
                       command=lambda text=button_text: self.insert_text(text)).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 2:
                col_val = 0
                row_val += 1

        # Set focus to an entry field when clicked
        self.feet_entry.bind("<FocusIn>", lambda event: self.set_current_entry(self.feet_entry))
        self.inches_entry.bind("<FocusIn>", lambda event: self.set_current_entry(self.inches_entry))
        self.fraction_entry.bind("<FocusIn>", lambda event: self.set_current_entry(self.fraction_entry))
        self.feet_entry2.bind("<FocusIn>", lambda event: self.set_current_entry(self.feet_entry2))
        self.inches_entry2.bind("<FocusIn>", lambda event: self.set_current_entry(self.inches_entry2))
        self.fraction_entry2.bind("<FocusIn>", lambda event: self.set_current_entry(self.fraction_entry2))

        # Keyboard shortcuts
        for key, op in (("1", "add"), ("2", "subtract"), ("3", "multiply"), ("4", "divide")):
            master.bind(f"<Control-Key-{key}>", lambda event, op=op: self.calculate(op))
        master.bind("<Control-Delete>", lambda event: self.clear_fields())
        master.bind("<Control-u>", lambda event: self.use_result())
        master.bind("<Control-Shift-C>", lambda event: self.copy_result())

        # Log
        self.log_label = ttk.Label(master, text="Calculation Log:")
        self.log_label.grid(row=8, column=0, padx=5, pady=5)

        self.log_text = tk.Text(master, width=45, height=10, state=tk.DISABLED)
        self.log_text.grid(row=9, column=0, rowspan=4, columnspan=4, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(master, command=self.log_text.yview)
        self.scrollbar.grid(row=9, column=4, rowspan=4, sticky='ns')
        self.log_text['yscrollcommand'] = self.scrollbar.set

        # --- Save Settings on Close ---
        master.protocol("WM_DELETE_WINDOW", self.on_close) #Handle window close event

        # --- Load Settings After Widget Creation ---
        self.load_settings()

        # --- Apply saved settings ---
        self.apply_settings()

    def load_settings(self):
        """Loads settings from the config file."""
        if os.path.exists(self.CONFIG_FILE): # Only load if the file exists
            try:
                self.config.read(self.CONFIG_FILE)
                self.master.geometry(self.config['WINDOW']['geometry'])
                self.precision_var.set(self.config.get('OPTIONS', 'precision', fallback=self.precision_var.get()))
                self.units_var.set(self.config.get('OPTIONS', 'units', fallback=self.units_var.get()))
                try: #Wrap entry population
                    self.feet_entry.insert(0, self.config['VALUES']['feet1'])
                    self.inches_entry.insert(0, self.config['VALUES']['inches1'])
                    self.fraction_entry.insert(0, self.config['VALUES']['fraction1'])
                    self.feet_entry2.insert(0, self.config['VALUES']['feet2'])
                    self.inches_entry2.insert(0, self.config['VALUES']['inches2'])
                    self.fraction_entry2.insert(0, self.config['VALUES']['fraction2'])
                except (KeyError, TypeError) as e:
                    print(f"Error loading settings: {e}") #Print error to console for debugging
                    pass #Skip loading values if there's an error
            except KeyError:
                pass #Use default values if section or key is missing

    def apply_settings(self):
        """Applies saved settings to the calculator."""
        #This is currently empty, but could be expanded to apply theme settings, etc.
        pass

    def save_settings(self):
        """Saves settings to the config file."""
        self.config['WINDOW'] = {'geometry': self.master.geometry()}
        self.config['VALUES'] = {
            'feet1': self.feet_entry.get(),
            'inches1': self.inches_entry.get(),
            'fraction1': self.fraction_entry.get(),
            'feet2': self.feet_entry2.get(),
            'inches2': self.inches_entry2.get(),
            'fraction2': self.fraction_entry2.get()
        }
        self.config['OPTIONS'] = {'precision': self.precision_var.get(), 'units': self.units_var.get()}
        with open(self.CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def on_close(self):
        """Handles the window close event."""
        self.save_settings()
        self.master.destroy()

    def set_entry_background(self, entry, color):
        """Sets the background color of an entry field."""
        entry.config(background=color)

    def validate_integer_input(self, new_text):
        """Validates if the new input is a valid integer."""
        self.set_entry_background(self.master.focus_get(), "white")  # Reset background
        if not new_text:  # Allow empty string (clearing the field)
            return True
        try:
            measure.parse_int(new_text)
            return True
        except measure.MeasurementError:
            return False

    def validate_fraction_input(self, new_text):
        """Validates if the new input is a valid fraction string."""
        self.set_entry_background(self.master.focus_get(), "white")  # Reset background
        if not new_text:  # Allow empty string
            return True
        try:
            measure.parse_fraction(new_text)
            return True
        except measure.MeasurementError:
            return False

    def set_current_entry(self, entry):
        """Sets the currently selected entry field."""
        self.current_entry = entry

    def insert_text(self, text):
        """Inserts text into the currently selected entry field."""
        if self.current_entry:
            self.current_entry.insert(tk.END, text)

    def _get_value(self, feet_entry, inches_entry, fraction_entry):
        """Returns the total inches from a set of entries, or None (showing the error) if invalid."""
        try:
            return measure.to_inches(feet_entry.get(), inches_entry.get(), fraction_entry.get())
        except measure.MeasurementError as e:
            self.result_value.config(text=str(e))
            return None

    def calculate(self, operation):
        value1 = self._get_value(self.feet_entry, self.inches_entry, self.fraction_entry)
        value2 = self._get_value(self.feet_entry2, self.inches_entry2, self.fraction_entry2)
        if value1 is None or value2 is None:
            return

        try:
            total_inches = measure.calculate(operation, value1, value2)
        except measure.MeasurementError as e:
            self.result_value.config(text=str(e))
            return

        self.last_total = total_inches
        result_formatted = self.format_total(total_inches)
        self.result_value.config(text=result_formatted)
        operator = measure.OPERATORS[operation]
        # Multiply/divide treat Measurement 2 as a plain factor, not a length.
        right = measure.format_number(value2) if operation in ("multiply", "divide") else self.format_total(value2)
        self.log_calculation(f"{self.format_total(value1)} {operator} {right} = {result_formatted}\n")

    def format_total(self, total_inches):
        return measure.format_result(total_inches, self.units_var.get(), int(self.precision_var.get().split("/")[1]))

    def refresh_result(self):
        """Re-renders the last result after a precision or unit change."""
        if self.last_total is not None:
            self.result_value.config(text=self.format_total(self.last_total))

    def apply_typed(self, typed_entry, feet_entry, inches_entry, fraction_entry):
        """Fills the feet/inches/fraction fields from a free-form typed measurement."""
        try:
            parts = measure.split_inches(measure.parse_typed(typed_entry.get()))
        except measure.MeasurementError as e:
            self.result_value.config(text=str(e))
            self.set_entry_background(typed_entry, "red")
            return
        self.set_entry_background(typed_entry, "white")
        for entry, value in zip((feet_entry, inches_entry, fraction_entry), parts):
            entry.delete(0, tk.END)
            entry.insert(0, value)
        typed_entry.delete(0, tk.END)

    def use_result(self):
        """Moves the last result into Measurement 1 so calculations can be chained."""
        if self.last_total is None:
            return
        parts = measure.split_inches(self.last_total)
        for entry, value in zip((self.feet_entry, self.inches_entry, self.fraction_entry), parts):
            entry.delete(0, tk.END)
            entry.insert(0, value)
        for entry in (self.feet_entry2, self.inches_entry2, self.fraction_entry2, self.typed_entry, self.typed_entry2):
            entry.delete(0, tk.END)

    def log_calculation(self, entry):
        """Appends a calculation entry to the log."""
        self.log_text.config(state=tk.NORMAL)  # Enable editing
        self.log_text.insert(tk.END, entry)
        self.log_text.config(state=tk.DISABLED)  # Disable editing again
        self.log_text.yview(tk.END)  # Scroll to the end

    def clear_fields(self):
        """Clears the input fields."""
        self.feet_entry.delete(0, tk.END)
        self.inches_entry.delete(0, tk.END)
        self.fraction_entry.delete(0, tk.END)
        self.feet_entry2.delete(0, tk.END)
        self.inches_entry2.delete(0, tk.END)
        self.fraction_entry2.delete(0, tk.END)
        self.typed_entry.delete(0, tk.END)
        self.typed_entry2.delete(0, tk.END)
        self.result_value.config(text="")
        self.last_total = None

    def reset_all(self):
        """Clears all input fields and the calculation log."""
        self.clear_fields()
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)

    def copy_result(self):
        """Copies the result to the clipboard."""
        result = self.result_value.cget("text") #Get text from label
        self.master.clipboard_clear() #Clear clipboard
        self.master.clipboard_append(result) #Append result to clipboard
        self.master.update() #Make sure the clipboard content is available

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
