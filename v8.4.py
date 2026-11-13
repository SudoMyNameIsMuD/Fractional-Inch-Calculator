import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tkfont
from fractions import Fraction
import configparser  # For persistent settings
import os # To check if the config file exists

class Calculator:
    FRACTION_DENOMINATORS = [2, 4, 8, 16, 32, 64, 128, 256]  # Constant for denominators
    CONFIG_FILE = "calculator_settings.ini" #Filename for settings
    RESULT_PROMPT = "Enter measurements, then choose an operation."
    ACCENT_COLOR = "#0A84FF"

    def __init__(self, master):
        self.master = master
        master.title("Fractional Inch Calculator")

        # --- Load Settings Object ---
        self.config = configparser.ConfigParser()
        self.style = ttk.Style(master)
        self.style.map("Calculator.TEntry", foreground=[("invalid", "#d04444")])
        self.operation_font = tkfont.nametofont("TkDefaultFont").copy()
        self.operation_font.configure(weight="bold")
        self.style.configure("Operation.TButton", padding=(12, 7))
        self.style.configure("ActiveOperation.TButton", font=self.operation_font,
                             foreground=self.ACCENT_COLOR, padding=(12, 7))
        self.style.configure("Secondary.TButton", padding=(10, 5))
        self.style.configure("Keypad.TButton", padding=(9, 6))
        self.style.configure("Result.TLabel", foreground=self.ACCENT_COLOR)

        self.current_entry = None
        self.last_operation = "add"
        self.has_result = False
        self.entry_details = {}
        self.input_variables = []
        self.status = tk.StringVar(master, value="Blank fields count as zero. Choose an operation.")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.geometry("780x660")

        self.menu_bar = tk.Menu(master)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.help_menu.add_command(
            label="Keyboard Shortcuts...",
            command=self.show_shortcuts)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        master.configure(menu=self.menu_bar)

        content = ttk.Frame(master, padding=16)
        content.grid(sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(4, weight=1)
        header = ttk.Frame(content)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        header.columnconfigure(1, weight=1)
        self.header_accent = tk.Frame(header, background=self.ACCENT_COLOR, width=4)
        self.header_accent.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(0, 12))
        self.title_font = tkfont.nametofont("TkDefaultFont").copy()
        self.title_font.configure(size=22, weight="bold")
        self.title_label = ttk.Label(header, text="Fractional Inch Calculator",
                                     font=self.title_font)
        self.title_label.grid(row=0, column=1, sticky="w")
        self.subtitle_label = ttk.Label(
            header, text="Calculate with feet, inches, and fractions.")
        self.subtitle_label.grid(row=1, column=1, sticky="w", pady=(4, 0))

        measurements = ttk.Frame(content)
        measurements.grid(row=1, column=0, sticky="ew")
        measurements.columnconfigure((0, 1), weight=1, uniform="measurement")
        self.measurement1_frame = self._build_measurement(measurements, 1, 0)
        self.measurement2_frame = self._build_measurement(measurements, 2, 1)

        controls = ttk.Frame(content)
        controls.grid(row=2, column=0, sticky="ew", pady=12)
        controls.columnconfigure((0, 1), weight=1, uniform="controls")
        actions = ttk.Frame(controls)
        actions.grid(row=0, column=0, sticky="e", padx=(0, 12))
        self.operation_buttons = {}
        for index, (name, operation) in enumerate((
            ("Add", "add"), ("Subtract", "subtract"),
            ("Multiply", "multiply"), ("Divide", "divide"),
        )):
            button = ttk.Button(actions, text=name,
                                command=lambda op=operation: self.calculate(op),
                                width=14, style="Operation.TButton")
            button.grid(row=index // 2, column=index % 2, padx=3, pady=3)
            setattr(self, f"{operation}_button", button)
            self.operation_buttons[operation] = button
        self.select_operation("add")
        self.clear_button = ttk.Button(actions, text="Clear Inputs", command=self.clear_fields,
                                       width=14, style="Secondary.TButton")
        self.clear_button.grid(row=2, column=0, padx=3, pady=(12, 3))
        self.reset_button = ttk.Button(actions, text="Reset All", command=self.reset_all,
                                       width=14, style="Secondary.TButton")
        self.reset_button.grid(row=2, column=1, padx=3, pady=(12, 3))
        self.reset_hint = ttk.Label(
            actions, text="Clear Inputs keeps history; Reset All clears it.",
            wraplength=320, justify="left")
        self.reset_hint.grid(row=3, column=0, columnspan=2, sticky="w", padx=3, pady=(3, 0))
        self.number_pad_frame = ttk.LabelFrame(controls, text="Keypad", padding=6)
        self.number_pad_frame.grid(row=0, column=1, sticky="w")
        self.number_pad_frame.columnconfigure((0, 1, 2), weight=1, uniform="keypad")
        for index, text in enumerate(("7", "8", "9", "4", "5", "6",
                                      "1", "2", "3", "0", "/", ".")):
            ttk.Button(self.number_pad_frame, text=text, width=5, takefocus=False,
                       style="Keypad.TButton",
                       command=lambda value=text: self.insert_text(value)).grid(
                           row=index // 3, column=index % 3, padx=2, pady=2, sticky="ew")
        ttk.Button(self.number_pad_frame, text="-", width=5, takefocus=False,
                   style="Keypad.TButton",
                   command=lambda: self.insert_text("-")).grid(row=4, column=0, padx=2, pady=2)
        self.backspace_button = ttk.Button(
            self.number_pad_frame, text="Backspace", takefocus=False, style="Keypad.TButton",
            command=self.backspace)
        self.backspace_button.grid(row=4, column=1, columnspan=2, padx=2, pady=2, sticky="ew")

        result = ttk.LabelFrame(content, text="Result", padding=12)
        result.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        result.columnconfigure(1, weight=1)
        self.result_accent = tk.Frame(result, background=self.ACCENT_COLOR, width=4)
        self.result_accent.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        self.placeholder_font = tkfont.nametofont("TkDefaultFont").copy()
        self.result_font = tkfont.nametofont("TkDefaultFont").copy()
        self.result_font.configure(size=22, weight="bold")
        self.result_value = ttk.Label(result, text=self.RESULT_PROMPT,
                                      font=self.placeholder_font, anchor="w")
        self.result_value.grid(row=0, column=1, sticky="ew")
        self.result_value.bind("<Configure>", lambda event: self.result_value.configure(
            wraplength=max(1, event.width)))
        self.copy_button = ttk.Button(result, text="Copy Result",
                                      command=self.copy_result, state=tk.DISABLED)
        self.copy_button.grid(row=0, column=2, padx=(12, 0))

        history = ttk.LabelFrame(content, text="Calculation History", padding=8)
        history.grid(row=4, column=0, sticky="nsew")
        history.columnconfigure(0, weight=1)
        history.rowconfigure(1, weight=1)
        history_actions = ttk.Frame(history)
        history_actions.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        history_actions.columnconfigure(0, weight=1)
        self.clear_history_button = ttk.Button(
            history_actions, text="Clear History", style="Secondary.TButton",
            command=self.clear_history)
        self.clear_history_button.grid(row=0, column=1, sticky="e")
        self.latest_log_font = tkfont.nametofont("TkFixedFont").copy()
        self.latest_log_font.configure(weight="bold")
        self.log_text = tk.Text(history, width=1, height=6, state=tk.DISABLED,
                                wrap=tk.WORD, font="TkFixedFont", borderwidth=0,
                                highlightthickness=0, padx=6, pady=6,
                                spacing1=4, spacing3=4)
        self.log_text.grid(row=1, column=0, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(history, command=self.log_text.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=self.scrollbar.set)
        self.log_text.tag_configure("latest", font=self.latest_log_font,
                                    foreground=self.ACCENT_COLOR)
        self.status_label = ttk.Label(content, textvariable=self.status, wraplength=700)
        self.status_label.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        self.status_label.bind("<Configure>", lambda event: self.status_label.configure(
            wraplength=max(1, event.width)))

        master.bind("<Return>", self.repeat_operation)
        master.bind("<KP_Enter>", self.repeat_operation)
        master.bind("<Escape>", self.clear_shortcut)
        copy_modifier = "Command" if master.tk.call("tk", "windowingsystem") == "aqua" else "Control"
        master.bind(f"<{copy_modifier}-Shift-C>", self.copy_shortcut)

        # --- Save Settings on Close ---
        master.protocol("WM_DELETE_WINDOW", self.on_close) #Handle window close event

        # --- Load Settings After Widget Creation ---
        self.load_settings()

        master.update_idletasks()
        master.minsize(max(680, content.winfo_reqwidth()),
                       max(620, content.winfo_reqheight()))
        self.set_current_entry(self.feet_entry)
        self.feet_entry.focus_set()

    def _build_measurement(self, parent, number, column):
        frame = ttk.LabelFrame(parent, text=f"Measurement {number}", padding=10)
        frame.grid(row=0, column=column, sticky="nsew",
                   padx=(0, 6) if column == 0 else (6, 0))
        label_width = tkfont.nametofont("TkDefaultFont").measure("Fraction")
        frame.columnconfigure(0, minsize=label_width + 10)
        frame.columnconfigure(2, weight=1)
        for row, (name, label) in enumerate((
            ("feet", "Feet"), ("inches", "Inches"), ("fraction", "Fraction"),
        )):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=4)
            variable = tk.StringVar(self.master)
            entry = ttk.Entry(frame, width=12, textvariable=variable, style="Calculator.TEntry")
            entry.grid(row=row, column=1, sticky="w", pady=4)
            suffix = "" if number == 1 else "2"
            setattr(self, f"{name}_entry{suffix}", entry)
            validator = self.validate_fraction_input if name == "fraction" else self.validate_integer_input
            hint = "Use a fraction such as 3/4 (denominator cannot be zero)." if name == "fraction" else "Use a whole number."
            self.entry_details[entry] = (f"Measurement {number}, {label}", validator, hint)
            entry.bind("<FocusIn>", lambda event, field=entry: self.set_current_entry(field))
            entry.bind("<FocusOut>", lambda event, field=entry: self.validate_entry(field))
            variable.trace_add("write", lambda *args, field=entry: self.input_changed(field))
            self.input_variables.append(variable)
        ttk.Label(frame, text="Fraction example: 3/4").grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(6, 0))
        return frame

    def input_changed(self, entry):
        entry.state(["!invalid"])
        self.show_result(self.RESULT_PROMPT)
        self.status.set("Input changed. Choose an operation to calculate.")

    def validate_entry(self, entry):
        label, validator, hint = self.entry_details[entry]
        valid = validator(entry.get())
        entry.state(["!invalid"] if valid else ["invalid"])
        if not valid:
            self.status.set(f"{label}: {hint}")
        return valid

    def show_result(self, text, valid=False):
        self.result_value.config(text=text)
        self.result_value.configure(
            font=self.placeholder_font if text == self.RESULT_PROMPT else self.result_font,
            style="Result.TLabel" if valid else "TLabel")
        self.has_result = valid
        self.copy_button.state(["!disabled"] if valid else ["disabled"])

    def repeat_operation(self, event=None):
        self.calculate(self.last_operation)
        return "break"

    def select_operation(self, operation):
        self.last_operation = operation
        for name, button in self.operation_buttons.items():
            active = name == operation
            button.configure(text=f"{name.title()} (Enter)" if active else name.title(),
                             style="ActiveOperation.TButton" if active else "Operation.TButton")

    def clear_shortcut(self, event=None):
        self.clear_fields()
        return "break"

    def copy_shortcut(self, event=None):
        self.copy_result()
        return "break"

    def show_shortcuts(self):
        modifier = "Command" if self.master.tk.call("tk", "windowingsystem") == "aqua" else "Control"
        shortcuts = (
            "Enter: Calculate using the marked operation\n"
            "Escape: Clear measurements and result\n"
            f"{modifier}+Shift+C: Copy the result\n"
            "Tab / Shift+Tab: Move between fields and controls"
        )
        messagebox.showinfo("Keyboard Shortcuts", shortcuts, parent=self.master)

    def load_settings(self):
        """Loads settings from the config file."""
        if os.path.exists(self.CONFIG_FILE): # Only load if the file exists
            try:
                self.config.read(self.CONFIG_FILE)
                self.master.geometry(self.config['WINDOW']['geometry'])
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
        with open(self.CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def on_close(self):
        """Handles the window close event."""
        self.save_settings()
        self.master.destroy()

    def validate_integer_input(self, new_text):
        """Validates if the new input is a valid integer."""
        if not new_text:  # Allow empty string (clearing the field)
            return True
        try:
            int(new_text)
            return True
        except ValueError:
            return False

    def validate_fraction_input(self, new_text):
        """Validates if the new input is a valid fraction string."""
        if not new_text:  # Allow empty string
            return True
        try:
            Fraction(new_text)
            return True
        except ValueError:
            return False
        except ZeroDivisionError:
            return False

    def set_current_entry(self, entry):
        """Sets the currently selected entry field."""
        self.current_entry = entry

    def insert_text(self, text):
        """Inserts text into the currently selected entry field."""
        entry = self.current_entry
        if entry is not None:
            if entry.selection_present():
                entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
            entry.insert(tk.INSERT, text)
            entry.focus_set()

    def backspace(self):
        entry = self.current_entry
        if entry is not None:
            if entry.selection_present():
                entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
            else:
                position = entry.index(tk.INSERT)
                if position > 0:
                    entry.delete(position - 1, position)
            entry.focus_set()

    def _get_value(self, feet_entry, inches_entry, fraction_entry):
        """Helper function to get the total inches from the entries."""
        try:
            feet = int(feet_entry.get() or 0)
            inches = int(inches_entry.get() or 0)
            fraction_str = fraction_entry.get() or "0/1"
            fraction = Fraction(fraction_str)
            return (feet * 12) + inches + float(fraction)  # Convert Fraction to float for calculations
        except ValueError:
            self.show_result("Invalid input. Please enter valid numbers and fractions.")
            return None
        except ZeroDivisionError:
            self.show_result("Invalid fraction. Denominator cannot be zero.")
            return None

    def _format_measurement(self, total_inches, is_input=False):
        """Helper function to format the result back into feet, inches, and fraction."""
        feet = int(total_inches // 12)
        remaining_inches = total_inches % 12
        inches = int(remaining_inches // 1)  # Get the whole number of inches
        fractional_inches = remaining_inches - inches

        # Find the closest common fraction (down to 1/256)
        best_denominator = 1
        min_diff = 1.0
        for denominator in self.FRACTION_DENOMINATORS:
            numerator = round(fractional_inches * denominator)
            diff = abs(fractional_inches - Fraction(numerator, denominator))
            if diff < min_diff:
                min_diff = diff
                best_denominator = denominator
        numerator = round(fractional_inches * best_denominator)
        closest_fraction = Fraction(numerator, best_denominator)

        if is_input:
            return f"{feet}\' {inches} {closest_fraction}\""
        else:
            return f"{feet}\' {inches} {closest_fraction}\""

    def calculate(self, operation):
        if operation in self.operation_buttons:
            self.select_operation(operation)
        first_invalid = None
        for entry in self.entry_details:
            if not self.validate_entry(entry):
                if first_invalid is None:
                    first_invalid = entry
        if first_invalid is not None:
            self.show_result(self.RESULT_PROMPT)
            self.validate_entry(first_invalid)
            first_invalid.focus_set()
            return
        value1 = self._get_value(self.feet_entry, self.inches_entry, self.fraction_entry)
        value2 = self._get_value(self.feet_entry2, self.inches_entry2, self.fraction_entry2)

        if value1 is not None and value2 is not None:
            try:
                if operation == "add":
                    total_inches = value1 + value2
                    operator = "+"
                elif operation == "subtract":
                    total_inches = value1 - value2
                    operator = "-"
                elif operation == "multiply":
                    total_inches = value1 * value2
                    operator = "*"
                elif operation == "divide":
                    if value2 == 0:
                        self.show_result("Cannot divide by zero")
                        self.status.set("Measurement 2 must be nonzero when dividing.")
                        return
                    total_inches = value1 / value2
                    operator = "/"
                else:
                    self.show_result("Invalid operation")
                    return

                result_formatted = self._format_measurement(total_inches)
                self.show_result(result_formatted, valid=True)
                self.status.set("Result ready. Copy it or edit a measurement.")

                # Log the calculation
                log_entry = f"{self._format_measurement(value1, is_input=True)} {operator} {self._format_measurement(value2, is_input=True)} = {result_formatted}\n"
                self.log_calculation(log_entry)

            except Exception as e:
                self.show_result(f"An unexpected error occurred: {e}")

    def log_calculation(self, entry):
        """Appends a calculation entry to the log."""
        self.log_text.config(state=tk.NORMAL)  # Enable editing
        self.log_text.tag_remove("latest", "1.0", tk.END)
        if self.log_text.compare("end-1c", ">", "1.0"):
            self.log_text.insert(tk.END, "\n")
        self.log_text.insert(tk.END, entry, "latest")
        self.log_text.config(state=tk.DISABLED)  # Disable editing again
        self.log_text.yview(tk.END)  # Scroll to the end

    def clear_history(self):
        """Clears only the calculation history."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.status.set("Calculation history cleared.")

    def clear_fields(self):
        """Clears the input fields."""
        self.feet_entry.delete(0, tk.END)
        self.inches_entry.delete(0, tk.END)
        self.fraction_entry.delete(0, tk.END)
        self.feet_entry2.delete(0, tk.END)
        self.inches_entry2.delete(0, tk.END)
        self.fraction_entry2.delete(0, tk.END)
        self.show_result(self.RESULT_PROMPT)
        for entry in self.entry_details:
            entry.state(["!invalid"])
        self.status.set("Inputs cleared. Calculation history kept.")
        self.set_current_entry(self.feet_entry)
        self.feet_entry.focus_set()

    def reset_all(self):
        """Clears all input fields and the calculation log."""
        self.clear_fields()
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.status.set("Inputs and calculation history cleared.")

    def copy_result(self):
        """Copies the result to the clipboard."""
        if not self.has_result:
            self.status.set("Calculate a valid result before copying.")
            return
        result = self.result_value.cget("text") #Get text from label
        self.master.clipboard_clear() #Clear clipboard
        self.master.clipboard_append(result) #Append result to clipboard
        self.master.update() #Make sure the clipboard content is available
        self.status.set("Result copied to clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
