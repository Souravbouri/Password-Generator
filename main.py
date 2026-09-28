"""
main.py
-------
Beginner Tier: Command-Line Random Password Generator

Feature checklist covered:
- Prompt user for password length (minimum 8 enforced)
- Prompt user to choose character types (at least 2 required)
- Generate and display a password matching the criteria
- Input validation for length and character type selection
- Option to generate another password without restarting the program

Run with:
    python main.py
"""

from generator import generate_password, PasswordGenerationError

MIN_LENGTH = 8


def ask_yes_no(prompt):
    """Ask a yes/no question and return True/False."""
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def ask_length():
    """Ask the user for password length, enforcing the minimum."""
    while True:
        raw = input(f"Enter desired password length (minimum {MIN_LENGTH}): ").strip()
        if not raw.isdigit():
            print("Please enter a valid whole number.")
            continue
        length = int(raw)
        if length < MIN_LENGTH:
            print(f"Length must be at least {MIN_LENGTH}. Try again.")
            continue
        return length


def ask_character_types():
    """Ask the user which character types to include."""
    print("\nWhich character types should the password include?")
    use_upper = ask_yes_no("  Include UPPERCASE letters?")
    use_lower = ask_yes_no("  Include lowercase letters?")
    use_digits = ask_yes_no("  Include numbers?")
    use_symbols = ask_yes_no("  Include symbols (!@#$...)?")
    return use_upper, use_lower, use_digits, use_symbols


def main():
    print("=" * 50)
    print("   RANDOM PASSWORD GENERATOR (Beginner CLI)")
    print("=" * 50)

    while True:
        length = ask_length()
        use_upper, use_lower, use_digits, use_symbols = ask_character_types()

        try:
            password = generate_password(
                length=length,
                use_upper=use_upper,
                use_lower=use_lower,
                use_digits=use_digits,
                use_symbols=use_symbols,
                min_length=MIN_LENGTH,
            )
            print("\nYour generated password:")
            print(f"  {password}\n")
        except PasswordGenerationError as e:
            print(f"\n[Error] {e}\n")
            # Loop back so the user can retry without restarting the program
            continue

        if not ask_yes_no("Generate another password?"):
            print("\nGoodbye! Stay secure.")
            break
        print()


if __name__ == "__main__":
    main()
