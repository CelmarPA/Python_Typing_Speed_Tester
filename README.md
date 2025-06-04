# ⌨️ Typing Speed Tester - Python GUI App

A simple and intuitive Python GUI application to test and improve your typing speed. Built with Tkinter for the interface, this app measures Words Per Minute (WPM) and Characters Per Minute (CPM) with real-time feedback.

## 📌 Table of Contents

- [⌨️ Typing Speed Tester - Python GUI App](#️-typing-speed-tester---python-gui-app)
  - [📌 Table of Contents](#-table-of-contents)
  - [🚀 Features](#-features)
  - [💽 How to Use](#-how-to-use)
  - [▶️ Getting Started](#️-getting-started)
    - [Prerequisites](#prerequisites)
    - [Running the Application](#running-the-application)
  - [📄 Files](#-files)
  - [🧪 Example](#-example)
  - [✅ License](#-license)
  - [👤 Author](#-author)
  - [💬 Feedback](#-feedback)

---

## 🚀 Features

* Graphical interface using Tkinter  
* Real-time typing accuracy feedback (correct/wrong letters and words)  
* Measures Words Per Minute (WPM) and Characters Per Minute (CPM)  
* Timer-based session (60 seconds)  
* Language selection (English and Portuguese)  
* Automatic saving of typing scores to CSV for later review

## 💽 How to Use

1. Open the application.
2. Select your preferred language by clicking the flag icons.
3. Start typing the displayed words; the timer starts automatically.
4. View your real-time WPM and CPM metrics.
5. At the end of 60 seconds, your score will be saved automatically.

## ▶️ Getting Started

### Prerequisites

* Python 3.x installed on your system  
* Required libraries:  
  - `tkinter` (standard with Python)  
  - `requests` (`pip install requests`)

### Running the Application

1. Clone or download this repository.
2. Make sure the files `words_random.py`, `typing_speed_tester.py`, and `brazil.png`, `usa.png` are in the same directory.
3. Run the application using:

```bash
python typing_speed_tester.py
```

## 📄 Files

* `typing_speed_tester.py`: Main script containing the TypingSession and Window classes responsible for logic and GUI.
* `words_random.py`: Handles fetching a random list of words from an online API.
* `icons/brazil.png` and `icons/usa.png`: Flag icons for switching between Portuguese and English.
* `score/score.csv`: Auto-generated CSV file where all typing test results are saved.

## 🧪 Example

```plaintext
[User selects Portuguese flag]
[Starts typing: "palavra exemplo casa..."]
[Real-time feedback highlights correct and incorrect letters]
[After 60 seconds: "Result: 230 CPM (46 WPM)"]
[Score is saved in 'score/score.csv']
```

## ✅ License

This project is open-source and free to use for educational or personal purposes.

---

## 👤 Author

**Celmar Pereira**

- [GitHub](https://github.com/CelmarPA)
- [LinkedIn](https://linkedin.com/in/celmar-pereira-de-andrade-039830181)
- [Portfolio](https://yourportfolio.com)

---

## 💬 Feedback

Enjoy the app and feel free to customize it!
