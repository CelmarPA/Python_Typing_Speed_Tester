from tkinter import *
from tkinter import messagebox
import tkinter.font as tk_font
import time
from datetime import datetime
import csv
import os
from words_random import WordsList   # External module that provides randomized words list


class TypingSession:
    """
    Represents a typing test session, tracking words, time, and performance metrics.
    """
    def __init__(self, words):
        """
        Initializes the session with a given list of words.
        :param words (list): List of words to be typed during the session.
        """
        self.words = words
        self.start_time = None  # Timestamp when test started
        self.time_left = None  # Countdown time in seconds (default 60)
        self.correct_words = None  # Count of correctly typed words
        self.correct_chars = None  # Count of correctly typed characters
        self.current_word_index = None  # Index of the current word to type
        self.cpm_corrected = None  # Corrected characters per minute
        self.wpm = None  # Words per minute
        self.start()  # Start the session immediately
        self.timer_started = False  # Flag for timer status

    def start(self):
        """
        Initialize or reset session variables to start a new test.
        """
        self.start_time = time.time()
        self.time_left = 60
        self.correct_words = 0
        self.correct_chars = 0
        self.current_word_index = 0
        self.cpm_corrected = 0
        self.wpm = 0

    def next_word(self):
        """
        Move to the next word in the list.
        :return str or None: Next word if available, else None if at the end.
        """
        self.current_word_index += 1
        if self.current_word_index >= len(self.words):
            return None
        return self.words[self.current_word_index]

    def check_word(self, typed):
        """
        Check the typed word against the actual word and update correct characters count.
        :param typed: (str) Word typed by the user.
        :return bool: True if the typed word matches exactly, False otherwise.
        """
        actual = self.words[self.current_word_index]
        correct_chars = sum(1 for i in range(min(len(typed), len(actual))) if typed[i] == actual[i])
        self.correct_chars += correct_chars
        if typed == actual:
            self.correct_words += 1
            return True
        return False

    def update_metrics(self):
        """
        Calculate and update CPM (characters per minute) and WPM (words per minute).
        :return:
        """
        if not self.start_time:
            return
        elapsed_time = max((time.time() - self.start_time) / 60, 1 / 60) # Avoid division by zero
        self.cpm_corrected = self.correct_chars / elapsed_time
        self.wpm = self.cpm_corrected / 5 # Standard WPM calculation: 5 chars per word


class Window:
    """
    Main application window for the typing speed tester GUI.
    Handles UI components, user interactions, and session management.
    """
    def __init__(self):
        """
         Initialize the main window, load images, fonts, and start a new typing session.
        """
        self.window = Tk()
        self.window.geometry("650x300")
        self.window.resizable(width=False, height=False)
        self.window.title("Typing Speed Tester")

        self.brazil_img = PhotoImage(file="icons/brazil.png") # Brazil flag icon
        self.usa_img = PhotoImage(file="icons/usa.png") # USA flag icon

        # Entry widgets for displaying stats
        self.recent_score_entry = None
        self.corrected_cpm_entry = None
        self.wpm_entry = None
        self.time_entry = None

        self.text = None  # Text widget displaying words to type
        self.typed_text_entry = None  # Entry widget for user input
        self.large_font = tk_font.Font(family="Fira Mono", size=20)  # Custom font for better readability

        self.idiom = None  # Language identifier (e.g., "en" or "pt-br")
        self.words_list = None  # Current list of words for session
        self.after_id = None  # ID for scheduled timer callback
        self.words_indexes = []  # List of tuples with start and end positions of words in Text widget
        self.session = None  # Current TypingSession object

        self.timer_started = False  # Timer flag

        self.make_window()
        self.new_session()

    def make_window(self):
        """
        Setup all UI elements: labels, buttons, text widgets, and event bindings.
        """
        self.window.config(padx=20, pady=20)
        total_columns = 9
        for i in range(total_columns):
            self.window.grid_columnconfigure(i, weight=1)

        # Static labels for stats
        Label(text="Most recent score:").grid(row=1, column=3, columnspan=7, sticky="W", padx=65)
        Label(text="Corrected CPM:").grid(row=3, column=1, sticky="e", padx=(0, 5))
        Label(text="WPM:").grid(row=3, column=3, sticky="e", padx=(0, 5))
        Label(text="Time left:").grid(row=3, column=5, sticky="e", padx=(0, 5))

        # Read-only entries showing real-time stats
        self.recent_score_entry = Entry(self.window, width=30, state="readonly", font=self.large_font, justify="center")
        self.recent_score_entry.grid(row=2, column=2, columnspan=5, sticky='nsew', pady=5)

        self.corrected_cpm_entry = Entry(self.window, width=10, state="readonly")
        self.corrected_cpm_entry.grid(row=3, column=2, sticky="W")

        self.wpm_entry = Entry(self.window, width=10, state="readonly")
        self.wpm_entry.grid(row=3, column=4, sticky="W")

        self.time_entry = Entry(self.window, width=10, state="readonly")
        self.time_entry.grid(row=3, column=6, sticky="W")

        # Buttons for restart and language switching
        Button(text="Restart", command=self.reset).grid(row=3, column=7, padx=10, sticky="W")
        Button(image=self.usa_img, command=lambda: self.change_language(None)).grid(row=1, column=1, sticky="W")
        Button(image=self.brazil_img, command=lambda: self.change_language("pt-br")).grid(row=1, column=1, sticky="W",
                                                                                          padx=50)

        # Text widget for displaying the words to type
        self.text = Text(self.window, width=70, height=3, font=self.large_font, wrap="word")
        self.text.grid(row=4, column=1, columnspan=7, sticky="nsew", pady=10)
        self.text.tag_configure("center", justify="center")
        self.text.tag_config("highlight", background="darkolivegreen3", foreground="black")
        self.text.tag_config("correct_letter", foreground="white")
        self.text.tag_config("wrong_letter", foreground="red")
        self.text.tag_config("correct_word", foreground="blue")
        self.text.tag_config("wrong_word", foreground="red")

        # Entry for typing input, with event bindings to check input dynamically and on space press
        self.typed_text_entry = Entry(self.window, width=70, font=self.large_font, justify="center")
        self.typed_text_entry.grid(row=5, column=1, columnspan=7, sticky="nsew")
        self.typed_text_entry.bind("<KeyRelease>", self.check_typed_word)
        self.typed_text_entry.bind("<space>", self.space_pressed)

    def new_session(self):
        """
        Starts a new typing session by loading words and resetting the interface.
        Also displays the most recent score if available.
        """
        self.words_list = WordsList(idiom=self.idiom).get_list()
        self.session = TypingSession(self.words_list)
        self.reset_interface()
        self.highlight_next_word()

        last_score = self.get_last_score()
        if last_score:
            self.recent_score_entry.config(state="normal")
            self.recent_score_entry.delete(0, END)
            self.recent_score_entry.insert(0,
                                           f"Lang: {last_score['lang']} {last_score['cpm']} CPM ({last_score['wpm']} WPM)")
            self.recent_score_entry.config(state="readonly")

    def change_language(self, idiom):
        """
        Change the language (idiom) of the word list and restart the session.
        :param idiom: (str or None) Language code, e.g. "pt-br" or None for English.
        """
        self.idiom = idiom
        self.timer_started = False
        self.reset()

    def highlight_next_word(self):
        """
        Highlight the current word to type in the text widget.
        """
        if not self.session:
            return

        self.text.tag_remove("highlight", "1.0", END)

        current_index = self.session.current_word_index
        if current_index < 0 or current_index >= len(self.words_indexes):
            return  # Out of range index, no highlight

        start, end = self.words_indexes[current_index]
        self.text.tag_add("highlight", start, end)
        self.text.see(start)

    def check_typed_word(self, event):
        """
        On every key release, compare the typed letters to the target word letters
        and color-code correct and incorrect letters in real time.
        :param event: The Tkinter event object (not used).
        :return:
        """
        _ = event

        if not self.timer_started:
            self.timer_started = True
            self.update_timer()

        if not self.session or self.session.current_word_index == -1:
            return
        typed = self.typed_text_entry.get()
        start, end = self.words_indexes[self.session.current_word_index]
        actual_word = self.text.get(start, end)
        self.text.tag_remove("correct_letter", start, end)
        self.text.tag_remove("wrong_letter", start, end)

        for i in range(len(typed)):
            if i >= len(actual_word):
                break
            pos_start = f"{start}+{i}c"
            pos_end = f"{start}+{i + 1}c"
            if typed[i] == actual_word[i]:
                self.text.tag_add("correct_letter", pos_start, pos_end)
            else:
                self.text.tag_add("wrong_letter", pos_start, pos_end)

    def space_pressed(self, event):
        """
        Handle space key press event to check the typed word,
        update metrics, highlight correctness, and move to next word.
        :param event: The Tkinter event object.
        :return str: "break" to prevent the default space character insertion.
        """
        _ = event

        if not self.session:
            return "break"

        typed = self.typed_text_entry.get().strip()
        correct = self.session.check_word(typed)
        self.session.update_metrics()
        self.update_cpm(self.session.cpm_corrected)
        self.update_wpm(self.session.wpm)

        # Remove previous word highlighting
        start, end = self.words_indexes[self.session.current_word_index]
        self.text.tag_remove("correct_word", start, end)
        self.text.tag_remove("wrong_word", start, end)

        # Highlight current word as correct or wrong
        if correct:
            self.text.tag_add("correct_word", start, end)
        else:
            self.text.tag_add("wrong_word", start, end)

        # Move to next word
        self.session.next_word()

        # Check if it's over
        if self.session.current_word_index >= len(self.words_list):
            self.end_test()
            return "break"

        self.highlight_next_word()

        # Clear typed input for next word
        self.typed_text_entry.delete(0, END)

        return "break"  # Prevent inserting space character

    def update_cpm(self, cpm):
        """
        Update the corrected CPM display entry.
        :param cpm: (float) Characters per minute corrected.
        """
        self.corrected_cpm_entry.config(state="normal")
        self.corrected_cpm_entry.delete(0, END)
        self.corrected_cpm_entry.insert(0, f"{int(cpm)}")
        self.corrected_cpm_entry.config(state="readonly")

    def update_wpm(self, wpm):
        """
        Update the WPM display entry.
        :param wpm: (float) Words per minute.
        """
        self.wpm_entry.config(state="normal")
        self.wpm_entry.delete(0, END)
        self.wpm_entry.insert(0, f"{int(wpm)}")
        self.wpm_entry.config(state="readonly")

    def update_timer(self):
        """
        Update the countdown timer every second.
        When time runs out, end the test.
        """
        self.time_entry.config(state="normal")
        self.time_entry.delete(0, END)
        self.time_entry.insert(0, f"{self.session.time_left}")
        self.time_entry.config(state="readonly")
        if self.session.time_left > 0:
            self.session.time_left -= 1
            self.after_id = self.window.after(1000, self.update_timer)
        else:
            self.end_test()

    def end_test(self):
        """
        Called when the time is up.
        Disable typing, display final score, save results, and notify the user.
        """
        self.typed_text_entry.config(state="disabled")
        self.recent_score_entry.config(state="normal")
        self.recent_score_entry.delete(0, END)
        cpm = int(self.session.cpm_corrected) if self.session.cpm_corrected else 0
        wpm = int(self.session.wpm) if self.session.wpm else 0
        self.recent_score_entry.insert(0, f"{cpm} CPM ({wpm} WPM)")
        self.recent_score_entry.config(state="readonly")
        self.save_score_to_csv()
        messagebox.showinfo("Time's up", "Time's up!")

    def save_score_to_csv(self):
        """
        Save the current session's score (date, language, CPM, WPM) to a CSV file.
        Creates the directory if it does not exist.
        """
        directory = "score"
        filename = os.path.join(directory, "score.csv")
        os.makedirs(directory, exist_ok=True)
        file_exist = os.path.isfile(filename)
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exist:
                writer.writerow(["Date", "Lang", "CPM", "WPM"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.idiom if self.idiom else "en",
                int(self.session.cpm_corrected),
                int(self.session.wpm)
            ])

    @staticmethod
    def get_last_score():
        """
        Reads the last saved score from the CSV file, if available.
        :return  dict or None: Last score data with keys 'date', 'lang', 'cpm', 'wpm' or None if no data.
        """
        directory = "score"
        filename = os.path.join(directory, "score.csv")
        if not os.path.exists(filename):
            return None
        with open(filename, mode="r", newline="") as file:
            reader = list(csv.reader(file))
            if len(reader) <= 1:
                return None
            last_row = reader[-1]
            return {
                "date": last_row[0],
                "lang": last_row[1],
                "cpm": int(last_row[2]),
                "wpm": int(last_row[3])
            }

    def reset(self):
        """
        Reset the test: cancel timer, restart session, and reset UI.
        """
        self.cancel_timer()
        self.timer_started = False
        self.new_session()

    def cancel_timer(self):
        """
        Cancel the running timer callback if any.
        """
        if self.after_id:
            self.window.after_cancel(self.after_id)
            self.after_id = None

    def reset_interface(self):
        """
        Reset the UI text widgets to display the new list of words and clear inputs.
        """
        self.text.config(state="normal")
        self.text.delete("1.0", END)
        self.words_indexes.clear()

        index = "1.0"
        for word in self.words_list:
            self.text.insert(index, word + " ")
            start_index = index
            end_index = self.text.index(f"{start_index}+{len(word)}c")
            self.words_indexes.append((start_index, end_index))
            index = self.text.index(f"{end_index}+1c")

        self.typed_text_entry.config(state="normal")
        self.typed_text_entry.delete(0, END)
        self.typed_text_entry.focus()

        for entry in (self.corrected_cpm_entry, self.wpm_entry):
            entry.config(state="normal")
            entry.delete(0, END)
            entry.config(state="readonly")

        self.time_entry.config(state="normal")
        self.time_entry.delete(0, END)
        self.time_entry.insert(0, "60")
        self.time_entry.config(state="readonly")

if __name__ == "__main__":
    app = Window()
    app.window.mainloop()
