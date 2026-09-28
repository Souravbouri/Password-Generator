# 🔐 Random Password Generator

A Python-based password generator built as part of my **Oasis Infobyte Internship**.
It comes in two tiers:

- 🟢 **Beginner** — a simple, interactive command-line tool (`main.py`)
- 🔵 **Advanced** — a full GUI application with security best practices, a strength meter, and clipboard support (`gui.py`)

---

## 📁 Project Structure

```
password-generator/
├── generator.py        # Core password generation logic (shared by CLI & GUI)
├── main.py              # Beginner Tier — Command-Line Interface
├── gui.py                # Advanced Tier — GUI (tkinter)
├── requirements.txt   # Python dependencies
└── README.md
```

---

## ✨ Features

### Beginner Tier (`main.py`)
- ✅ Prompts for password length (minimum 8 characters enforced)
- ✅ Choose which character types to include — uppercase, lowercase, numbers, symbols (at least 2 required)
- ✅ Generates and displays a password matching your criteria
- ✅ Full input validation with helpful error messages
- ✅ Generate multiple passwords in one session, no restart needed

### Advanced Tier (`gui.py`)
- ✅ Clean GUI window with a **slider** for length and **checkboxes** for character types
- ✅ Uses Python's **`secrets`** module (cryptographically secure) instead of `random`
- ✅ **Password strength meter** — Weak / Medium / Strong, shown as a colored bar
- ✅ Guarantees at least **one character from every selected type**
- ✅ **Copy to Clipboard** button — password also auto-copies the moment it's generated
- ✅ Option to **exclude ambiguous characters** (`0`, `O`, `l`, `1`, `I`, `|`)
- ✅ **Session history** — view your last 5 generated passwords (never written to disk, for security)

---

## 🛠️ Tech Stack

| Tier | Technologies |
|------|-------------|
| Beginner | `Python`, `string`, `random`-free logic (delegates to `secrets`) |
| Advanced | `Python`, `secrets`, `tkinter`, `pyperclip` |

> Note: Both tiers actually use the `secrets` module under the hood (see `generator.py`) since it's the cryptographically correct choice for anything password-related — see [Python docs](https://docs.python.org/3/library/secrets.html).

---

## 💻 How to Run (Windows)

### 1. Install Python
Make sure [Python 3.9+](https://www.python.org/downloads/) is installed and added to PATH.
Check in Command Prompt / PowerShell:

```bash
python --version
```

### 2. Clone or download this repository

```bash
git clone https://github.com/<your-username>/password-generator.git
cd password-generator
```

### 3. (Recommended) Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

> `tkinter` ships with the standard Windows Python installer, so no separate install is normally needed for the GUI.

### 5. Run the Beginner CLI version

```bash
python main.py
```

### 6. Run the Advanced GUI version

```bash
python gui.py
```

---

## 🖥️ Usage Preview

**CLI (Beginner):**
```
==================================================
   RANDOM PASSWORD GENERATOR (Beginner CLI)
==================================================
Enter desired password length (minimum 8): 12

Which character types should the password include?
  Include UPPERCASE letters? (y/n): y
  Include lowercase letters? (y/n): y
  Include numbers? (y/n): y
  Include symbols (!@#$...)? (y/n): n

Your generated password:
  Xk4pQmT9wVaZ

Generate another password? (y/n): n

Goodbye! Stay secure.
```

**GUI (Advanced):** Slide to pick a length, tick the character types you want, hit **Generate Password** — it's instantly copied to your clipboard and added to your session history, with a live strength bar.

---

## 🔒 Security Notes

- Uses `secrets.choice()` and a custom `secrets`-based Fisher–Yates shuffle instead of `random`, since `random` is **not** cryptographically secure and should never be used for passwords, tokens, or keys.
- Every selected character type is guaranteed to appear at least once — plain random sampling alone doesn't guarantee this.
- Password history in the GUI is kept **in memory only** for the current session and is never written to a file or database.

---

## 📚 What I Learned

- Working with Python's `secrets` module vs `random` for security-sensitive code
- Structuring a small Python project into reusable modules (`generator.py`) rather than duplicating logic across CLI and GUI
- Building a GUI with `tkinter`, including sliders, checkboxes, and canvas-based visual indicators
- Clipboard integration using `pyperclip`
- Writing input validation that fails gracefully instead of crashing

---

## 🙌 Acknowledgements

Built as part of the **Oasis Infobyte Internship** program.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
