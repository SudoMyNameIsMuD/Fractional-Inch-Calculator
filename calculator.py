import tkinter as tk
from tkinter import ttk
from fractions import Fraction
import configparser  # For persistent settings
import os # To check if the config file exists

class Calculator:
    FRACTION_DENOMINATORS = [2, 4, 8, 16, 32, 64, 128, 256]  # Constant for denominators
    CONFIG_FILE = "calculator_settings.ini" #Filename for settings

    def __init__(self, master):
        self.master = master
        master.title("US Customary Units Calculator")

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
            int(new_text)
            return True
        except ValueError:
            return False

    def validate_fraction_input(self, new_text):
        """Validates if the new input is a valid fraction string."""
        self.set_entry_background(self.master.focus_get(), "white")  # Reset background
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
        if self.current_entry:
            self.current_entry.insert(tk.END, text)

    def _get_value(self, feet_entry, inches_entry, fraction_entry):
        """Helper function to get the total inches from the entries."""
        try:
            feet = int(feet_entry.get() or 0)
            inches = int(inches_entry.get() or 0)
            fraction_str = fraction_entry.get() or "0/1"
            fraction = Fraction(fraction_str)
            return (feet * 12) + inches + float(fraction)  # Convert Fraction to float for calculations
        except ValueError:
            self.result_value.config(text="Invalid input. Please enter valid numbers and fractions.")
            return None
        except ZeroDivisionError:
            self.result_value.config(text="Invalid fraction. Denominator cannot be zero.")
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
                        self.result_value.config(text="Cannot divide by zero")
                        return
                    total_inches = value1 / value2
                    operator = "/"
                else:
                    self.result_value.config(text="Invalid operation")
                    return

                result_formatted = self._format_measurement(total_inches)
                self.result_value.config(text=result_formatted)

                # Log the calculation
                log_entry = f"{self._format_measurement(value1, is_input=True)} {operator} {self._format_measurement(value2, is_input=True)} = {result_formatted}\n"
                self.log_calculation(log_entry)

            except Exception as e:
                self.result_value.config(text=f"An unexpected error occurred: {e}")

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
        self.result_value.config(text="")

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

root = tk.Tk()
calculator = Calculator(root)
root.mainloop()