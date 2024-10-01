import tkinter as tk
from math import floor
from appmechanics import TypingTestMechanics

class TypingSpeedTestUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg="#D0E7FF")  # Set background color

        self.sample_text = "The quick brown fox jumps over the lazy dog"

        # Create an instance of the mechanics
        self.mechanics = TypingTestMechanics(self.sample_text)

        # Timer variables
        self.time_left = 60
        self.timer_running = False

        # Header label
        self.header_label = tk.Label(root, text="Typing Speed Test", font=("Arial", 18, "bold"), bg="#f5f5f5",
                                     fg="#007BFF")
        self.header_label.pack(pady=10)

        # Label to display the sample text
        self.text_label = tk.Label(root, text=self.sample_text, font=("Arial", 14), bg="#ffffff", fg="#333333",
                                   wraplength=500)
        self.text_label.pack(pady=10)

        # Textbox for user input
        self.typing_area = tk.Text(root, height=5, width=50, font=("Arial", 14), bg="#f9f9f9", fg="#333333")
        self.typing_area.pack(pady=10)

        # Create a frame to hold the Start button, Timer label, and Reset button side by side
        self.button_timer_frame = tk.Frame(root, bg="#f5f5f5")
        self.button_timer_frame.pack(pady=5)

        # Start button inside the frame
        self.start_button = tk.Button(self.button_timer_frame, text="Start", command=self.start_test,
                                      font=("Arial", 12, "bold"),
                                      bg="#28a745", fg="#ffffff")
        self.start_button.pack(side=tk.LEFT, padx=10)

        # Timer label inside the frame
        self.timer_label = tk.Label(self.button_timer_frame, text="Time left: 60s", font=("Arial", 12, "bold"),
                                    bg="#f5f5f5", fg="#dc3545")
        self.timer_label.pack(side=tk.LEFT, padx=10)

        # Reset button inside the frame
        self.reset_button = tk.Button(self.button_timer_frame, text="Reset", command=self.reset_test,
                                      font=("Arial", 12, "bold"),
                                      bg="#ffc107", fg="#ffffff")
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Result label for WPM
        self.result_label = tk.Label(root, text="", font=("Arial", 12), bg="#D0E7FF", fg="#007BFF")
        self.result_label.pack(pady=5)


        # Create a frame to hold the labels side by side
        self.score_frame = tk.Frame(root, bg="#f5f5f5")
        self.score_frame.pack(pady=5)

        # Correct characters label
        self.correct_label = tk.Label(self.score_frame, text="CPM: 0", font=("Arial", 12),
                                      bg="#f5f5f5",
                                      fg="#28a745")
        self.correct_label.pack(side="left", padx=10)  # Align to the left with padding

        # WPM label to display the calculated WPM
        self.wpm_label = tk.Label(self.score_frame, text="WPM: 0", font=("Arial", 12), bg="#f5f5f5", fg="#007bff")
        self.wpm_label.pack(side="left", padx=10)  # Align to the left with padding

        # Incorrect characters label
        self.incorrect_label = tk.Label(self.score_frame, text="Incorrect Characters: 0", font=("Arial", 12),
                                        bg="#f5f5f5", fg="#dc3545")
        self.incorrect_label.pack(side="left", padx=10) # Align to the left with padding

        # Footer section for useful info
        # Footer section for useful info
        self.info_frame = tk.Frame(root, bg="#e9ecef")  # Lighter background color
        self.info_frame.pack(pady=15, fill="x", padx=20)  # Add padding on the sides

        self.info_label1 = tk.Label(self.info_frame, text="Why are there no difficult words in this test?",
                                    font=("Arial", 12, "bold"), bg="#e9ecef",
                                    fg="#0056b3")  # Change font size and color
        self.info_label1.pack(anchor="w", pady=5)  # Add vertical space

        self.info_label2 = tk.Label(self.info_frame,
                                    text="The words are selected from a list of commonly used words to focus on typing speed, not reading skill.",
                                    font=("Arial", 11), bg="#e9ecef", fg="#333333")
        self.info_label2.pack(anchor="w", pady=5)  # Add vertical space

        self.info_label3 = tk.Label(self.info_frame, text="What are CPM and WPM?", font=("Arial", 12, "bold"),
                                    bg="#e9ecef", fg="#0056b3")  # Change font size and color
        self.info_label3.pack(anchor="w", pady=5)  # Add vertical space

        self.info_label4 = tk.Label(self.info_frame,
                                    text="CPM: Characters Per Minute (raw count of characters, including mistakes).",
                                    font=("Arial", 11), bg="#e9ecef", fg="#333333")
        self.info_label4.pack(anchor="w", pady=5)  # Add vertical space

        self.info_label5 = tk.Label(self.info_frame,
                                    text="WPM: Words Per Minute (corrected CPM divided by 5, a standard measure).",
                                    font=("Arial", 11), bg="#e9ecef", fg="#333333")
        self.info_label5.pack(anchor="w", pady=5)  # Add vertical space

    def start_test(self):
        """Clear the typing area, start the timer, and begin countdown"""
        self.typing_area.delete(1.0, tk.END)  # Clear text area
        self.typing_area.focus()  # Set focus to the typing area
        self.mechanics.start_timer()  # Call start_timer from mechanics
        self.time_left = 60  # Reset time left to 60 seconds
        self.timer_running = True
        self.update_timer()  # Start the countdown
        self.root.bind('<Return>', self.calculate_wpm)  # Bind 'Enter' key to finish typing

    def update_timer(self):
        """Update the countdown timer every second"""
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.root.after(1000, self.update_timer)  # Call this method again after 1 second
        elif self.time_left == 0:
            self.timer_running = False
            self.calculate_wpm()  # Automatically calculate WPM when time runs out

    def calculate_wpm(self, event=None):
        """Calculate WPM and update the result label"""
        self.timer_running = False  # Stop the timer
        typed_text = self.typing_area.get(1.0, tk.END).strip()
        words_per_minute, correct_chars, incorrect_chars = self.mechanics.calculate_wpm_and_accuracy(typed_text)

        # Update the labels with the results
        self.result_label.config(text=f"Your typing speed: {words_per_minute:.2f} WPM")
        self.correct_label.config(text=f"CPM: {correct_chars}")
        self.incorrect_label.config(text=f"Incorrect Characters: {incorrect_chars}")
        self.wpm_label.config(text=f"WPM: {floor(correct_chars/5)}")

    def reset_test(self):
        """Reset the test to its initial state"""
        self.typing_area.delete(1.0, tk.END)  # Clear the typing area
        self.result_label.config(text="")  # Clear the result
        self.correct_label.config(text="Correct Characters: 0")
        self.incorrect_label.config(text="Incorrect Characters: 0")
        self.time_left = 60  # Reset the timer
        self.timer_label.config(text="Time left: 60s")  # Reset the timer label
        self.timer_running = False  # Stop the timer
        self.mechanics.start_time = None  # Reset the start time


