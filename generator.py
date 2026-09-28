"""
generator.py
------------
Core password generation logic for the Random Password Generator project.

This module is intentionally kept separate from the CLI (main.py) and GUI
(gui.py) so both interfaces reuse the exact same, security-reviewed logic
instead of duplicating it.

Uses the `secrets` module (NOT `random`) because `secrets` is
cryptographically secure and suitable for generating passwords, tokens,
and other security-sensitive values.
Reference: https://docs.python.org/3/library/secrets.html
"""

import string
import secrets

# Characters that are easy to visually confuse with one another.
AMBIGUOUS_CHARS = "0Ol1I|"


class PasswordGenerationError(ValueError):
    """Raised when password generation criteria are invalid."""
    pass


def get_character_pool(use_upper, use_lower, use_digits, use_symbols,
                        exclude_ambiguous=False):
    """
    Build the pool of characters to draw from, based on selected types.

    Returns a tuple: (full_pool_string, dict_of_required_pools)
    dict_of_required_pools maps each *selected* type name to its own
    character set, which is used later to guarantee at least one
    character from every selected type appears in the password.
    """
    pools = {}

    if use_upper:
        pools["upper"] = string.ascii_uppercase
    if use_lower:
        pools["lower"] = string.ascii_lowercase
    if use_digits:
        pools["digits"] = string.digits
    if use_symbols:
        pools["symbols"] = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"

    if exclude_ambiguous:
        cleaned = {}
        for key, chars in pools.items():
            filtered = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
            # Guard against a pool becoming empty after filtering
            cleaned[key] = filtered if filtered else chars
        pools = cleaned

    full_pool = "".join(pools.values())
    return full_pool, pools


def validate_criteria(length, use_upper, use_lower, use_digits, use_symbols,
                       min_length=8):
    """
    Validate password generation criteria.
    Raises PasswordGenerationError with a human-readable message on failure.
    """
    if not isinstance(length, int):
        raise PasswordGenerationError("Password length must be an integer.")

    if length < min_length:
        raise PasswordGenerationError(
            f"Password length must be at least {min_length} characters."
        )

    selected_types = sum([use_upper, use_lower, use_digits, use_symbols])
    if selected_types == 0:
        raise PasswordGenerationError(
            "You must select at least one character type."
        )
    if selected_types < 2:
        raise PasswordGenerationError(
            "Please select at least two character types for a stronger password."
        )

    if length < selected_types:
        raise PasswordGenerationError(
            "Password length is too short to include one of each selected "
            "character type."
        )

    return True


def generate_password(length, use_upper=True, use_lower=True,
                       use_digits=True, use_symbols=True,
                       exclude_ambiguous=False, min_length=8):
    """
    Generate a single cryptographically secure password.

    Guarantees that at least one character from EVERY selected character
    type is present in the final password (a common security requirement
    that plain random sampling does not guarantee on its own).
    """
    validate_criteria(length, use_upper, use_lower, use_digits, use_symbols,
                       min_length=min_length)

    full_pool, required_pools = get_character_pool(
        use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous
    )

    if not full_pool:
        raise PasswordGenerationError("Character pool is empty. Adjust your selections.")

    # Step 1: guarantee at least one character from each selected type
    guaranteed_chars = [secrets.choice(chars) for chars in required_pools.values()]

    # Step 2: fill the remaining length randomly from the full pool
    remaining_length = length - len(guaranteed_chars)
    random_chars = [secrets.choice(full_pool) for _ in range(remaining_length)]

    password_chars = guaranteed_chars + random_chars

    # Step 3: shuffle securely so guaranteed characters aren't predictably
    # placed at the start of the password.
    secure_shuffle(password_chars)

    return "".join(password_chars)


def secure_shuffle(items):
    """
    Cryptographically secure in-place shuffle (Fisher-Yates using `secrets`).
    `random.shuffle` is NOT used here because it is not cryptographically
    secure.
    """
    for i in range(len(items) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        items[i], items[j] = items[j], items[i]
    return items


def calculate_strength(password, use_upper=None, use_lower=None,
                        use_digits=None, use_symbols=None):
    """
    Estimate password strength as one of: "Weak", "Medium", "Strong".

    Scoring is based on two factors:
      1. Length of the password
      2. Diversity of character types actually present in the password

    If the use_* flags aren't provided, they are inferred directly from
    the password's contents.
    """
    length = len(password)

    has_upper = any(c.isupper() for c in password) if use_upper is None else use_upper
    has_lower = any(c.islower() for c in password) if use_lower is None else use_lower
    has_digit = any(c.isdigit() for c in password) if use_digits is None else use_digits
    has_symbol = (
        any(c not in string.ascii_letters + string.digits for c in password)
        if use_symbols is None else use_symbols
    )

    diversity = sum([has_upper, has_lower, has_digit, has_symbol])

    score = 0

    # Length scoring
    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    # Diversity scoring
    score += diversity

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"
