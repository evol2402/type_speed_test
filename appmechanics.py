import time
import tkinter.messagebox as messagebox



class TypingTestMechanics:
    def __init__(self, sample_text):
        self.sample_text = sample_text
        self.start_time = None

    def start_timer(self):
        """Start the timer"""
        self.start_time = time.time()

    def calculate_wpm_and_accuracy(self, typed_text):
        """Calculate WPM, correct and incorrect character counts"""
        if self.start_time is None:
            # Show a message box to inform the user
            messagebox.showerror("Timer Not Started", "Please start the timer first.")
            return None, None, None  # Return None values to indicate an error

        # End the timer and calculate total time in minutes
        end_time = time.time()
        total_time_seconds = end_time - self.start_time
        total_time_minutes = total_time_seconds / 60

        # Count words typed by the user
        typed_words = len(typed_text.split())

        # Calculate words per minute (WPM)
        words_per_minute = typed_words / total_time_minutes if total_time_minutes > 0 else 0  # Prevent division by zero

        # Count correct and incorrect characters
        correct_chars = 0
        incorrect_chars = 0
        for i, char in enumerate(typed_text):
            if i < len(self.sample_text) and char == self.sample_text[i]:
                correct_chars += 1
            else:
                incorrect_chars += 1

        # If the user typed fewer characters than the sample text, remaining characters are incorrect
        if len(typed_text) < len(self.sample_text):
            incorrect_chars += len(self.sample_text) - len(typed_text)

        return words_per_minute, correct_chars, incorrect_chars