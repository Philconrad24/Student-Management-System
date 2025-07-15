import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime

def show_info_message(title, message):
    """Displays an information message box."""
    messagebox.showinfo(title, message)

def show_warning_message(title, message):
    """Displays a warning message box."""
    messagebox.showwarning(title, message)

def show_error_message(title, message):
    """Displays an error message box."""
    messagebox.showerror(title, message)

def ask_confirmation(title, message):
    """Asks for user confirmation."""
    return messagebox.askyesno(title, message)

def is_valid_date(date_string):
    """
    Checks if a string is a valid date in YYYY-MM-DD format.
    """
    if not isinstance(date_string, str):
        return False
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_email(email):
    """
    Checks if a string is a valid email address using a simple regex.
    """
    if not isinstance(email, str):
        return False
    # Basic regex for email validation
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def is_valid_student_id(student_id):
    """
    Checks if a student ID is valid (e.g., alphanumeric, specific format).
    For now, just checks if it's a non-empty string.
    """
    return isinstance(student_id, str) and len(student_id.strip()) > 0

def is_valid_marks(marks):
    """
    Checks if marks are a valid float or int and non-negative.
    """
    try:
        marks_float = float(marks)
        return marks_float >= 0
    except (ValueError, TypeError):
        return False

# Example Usage (for testing purposes)
if __name__ == '__main__':
    print("--- Testing Helper Functions ---")

    # Test message boxes (will open actual GUI message boxes)
    # show_info_message("Test Info", "This is an information message.")
    # show_warning_message("Test Warning", "This is a warning message.")
    # show_error_message("Test Error", "This is an error message.")
    # if ask_confirmation("Test Confirmation", "Do you want to proceed?"):
    #     print("User confirmed.")
    # else:
    #     print("User cancelled.")

    # Test date validation
    print(f"Is '2023-01-15' a valid date? {is_valid_date('2023-01-15')}") # True
    print(f"Is '2023/01/15' a valid date? {is_valid_date('2023/01/15')}") # False
    print(f"Is 'invalid-date' a valid date? {is_valid_date('invalid-date')}") # False
    print(f"Is None a valid date? {is_valid_date(None)}") # False

    # Test email validation
    print(f"Is 'test@example.com' a valid email? {is_valid_email('test@example.com')}") # True
    print(f"Is 'invalid-email' a valid email? {is_valid_email('invalid-email')}") # False
    print(f"Is 'user@.com' a valid email? {is_valid_email('user@.com')}") # False

    # Test student ID validation
    print(f"Is 'S123' a valid student ID? {is_valid_student_id('S123')}") # True
    print(f"Is '' a valid student ID? {is_valid_student_id('')}") # False
    print(f"Is None a valid student ID? {is_valid_student_id(None)}") # False

    # Test marks validation
    print(f"Is 85.5 a valid mark? {is_valid_marks(85.5)}") # True
    print(f"Is '90' a valid mark? {is_valid_marks('90')}") # True
    print(f"Is -5 a valid mark? {is_valid_marks(-5)}") # False
    print(f"Is 'abc' a valid mark? {is_valid_marks('abc')}") # False
    print(f"Is None a valid mark? {is_valid_marks(None)}") # False
