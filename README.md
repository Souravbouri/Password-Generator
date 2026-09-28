# 🔐 Password Generator

A simple and secure **Password Generator** built with Python.
The application generates random passwords based on user-selected requirements such as password length and character types.

## ✨ Features

* Generate random passwords
* Choose password length
* Include uppercase letters
* Include lowercase letters
* Include numbers
* Include special characters
* Generate strong and unpredictable passwords
* Simple command-line interface
* Lightweight and easy to use

## 🛠️ Technologies Used

* **Python**
* `random`
* `string`

## 📂 Project Structure

```text
Password-Generator/
│
├── password_generator.py
├── README.md
└── .gitignore
```

> If your Python file has a different name, replace `password_generator.py` with the actual filename.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Souravbouri/Password-Generator.git
```

### 2. Navigate to the project

```bash
cd Password-Generator
```

### 3. Run the program

```bash
python password_generator.py
```

## 🔑 How It Works

The program creates a pool of possible characters using Python's built-in `string` module.

The character pool can contain:

* Lowercase letters: `a-z`
* Uppercase letters: `A-Z`
* Numbers: `0-9`
* Special characters: `!@#$%^&*...`

The program then randomly selects characters from the available pool until the requested password length is reached.

### Example

```text
Password Length: 16

Generated Password:
G7@kP2!xQ9#mL4$z
```

## 🎯 Purpose

This project was created to practice:

* Python programming
* Functions
* Conditional statements
* Loops
* String manipulation
* Random character generation
* User input handling

## 🔒 Security Note

This project is intended for **learning and personal use**.

For highly sensitive accounts, consider using a dedicated password manager with a cryptographically secure password generator.

## 👨‍💻 Author

**Sourav Bouri**

GitHub:
https://github.com/Souravbouri

## 📄 License

This project is available for educational and personal use.
