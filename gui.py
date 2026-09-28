"""
gui.py
------
Advanced Tier: GUI Random Password Generator

Feature checklist covered:
- GUI window with a slider for length + checkboxes for character types
- Uses `secrets` (via generator.py) for cryptographically secure generation
- Password strength indicator (Weak / Medium / Strong) with a colored bar
- Guarantees at least one character from each selected type
- "Copy to Clipboard" button using pyperclip (auto-copies on generation)
- Option to exclude ambiguous characters (0, O, l, 1, I, |)
- Generation history: last 5 passwords shown in-session only (not saved to file)

Run with:
    python gui.py

Requires: pyperclip  (pip install pyperclip)
tkinter ships with standard Python on Windows, so no separate install
is normally needed for it.
"""

import tkinter as tk
from tkinter import ttk, messagebox

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

from generator import generate_password, calculate_strength, PasswordGenerationError

MIN_LENGTH = 8
MAX_LENGTH = 64
HISTORY_LIMIT = 5

STRENGTH_COLORS = {
    "Weak": "#e74c3c",
    "Medium": "#f39c12",
    "Strong": "#27ae60",
}
STRENGTH_FRACTION = {
    "Weak": 0.33,
    "Medium": 0.66,
    "Strong": 1.0,
}


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Random Password Generator - Advanced")
        self.geometry("480x620")
        self.resizable(False, False)
        self.configure(bg="#1e1e2f")

        self.history = []  # in-memory only, never written to disk

        self._build_styles()
        self._build_widgets()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e2f")
        style.configure("TLabel", background="#1e1e2f", foreground="#f0f0f5",
                         font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("TCheckbutton", background="#1e1e2f", foreground="#f0f0f5",
                         font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("Horizontal.TScale", background="#1e1e2f")

    def _build_widgets(self):
        pad = {"padx": 20, "pady": 6}

        header = ttk.Label(self, text="Password Generator", style="Header.TLabel")
        header.pack(pady=(20, 10))

        # --- Password output field ---
        output_frame = ttk.Frame(self)
        output_frame.pack(fill="x", **pad)

        self.password_var = tk.StringVar(value="Click Generate")
        self.password_entry = tk.Entry(
            output_frame, textvariable=self.password_var, font=("Consolas", 14),
            justify="center", state="readonly", readonlybackground="#2c2c40",
            fg="#00e0a0", relief="flat"
        )
        self.password_entry.pack(fill="x", ipady=8)

        # --- Strength indicator ---
        strength_frame = ttk.Frame(self)
        strength_frame.pack(fill="x", **pad)

        self.strength_label = ttk.Label(strength_frame, text="Strength: -")
        self.strength_label.pack(anchor="w")

        self.strength_canvas = tk.Canvas(strength_frame, height=14, bg="#2c2c40",
                                          highlightthickness=0)
        self.strength_canvas.pack(fill="x", pady=(4, 0))

        # --- Length control ---
        length_frame = ttk.Frame(self)
        length_frame.pack(fill="x", **pad)

        self.length_var = tk.IntVar(value=16)
        length_label_row = ttk.Frame(length_frame)
        length_label_row.pack(fill="x")
        ttk.Label(length_label_row, text="Password Length").pack(side="left")
        self.length_value_label = ttk.Label(length_label_row, text="16")
        self.length_value_label.pack(side="right")

        self.length_slider = ttk.Scale(
            length_frame, from_=MIN_LENGTH, to=MAX_LENGTH, orient="horizontal",
            variable=self.length_var, command=self._on_length_change
        )
        self.length_slider.pack(fill="x", pady=(4, 0))

        # --- Character type checkboxes ---
        types_frame = ttk.Frame(self)
        types_frame.pack(fill="x", **pad)
        ttk.Label(types_frame, text="Include Character Types").pack(anchor="w", pady=(0, 4))

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        ttk.Checkbutton(types_frame, text="Uppercase (A-Z)",
                         variable=self.use_upper).pack(anchor="w")
        ttk.Checkbutton(types_frame, text="Lowercase (a-z)",
                         variable=self.use_lower).pack(anchor="w")
        ttk.Checkbutton(types_frame, text="Numbers (0-9)",
                         variable=self.use_digits).pack(anchor="w")
        ttk.Checkbutton(types_frame, text="Symbols (!@#$...)",
                         variable=self.use_symbols).pack(anchor="w")
        ttk.Checkbutton(types_frame, text="Exclude ambiguous characters (0, O, l, 1, I, |)",
                         variable=self.exclude_ambiguous).pack(anchor="w", pady=(6, 0))

        # --- Action buttons ---
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", **pad)

        generate_btn = ttk.Button(button_frame, text="Generate Password",
                                   command=self.on_generate)
        generate_btn.pack(fill="x", pady=(0, 6))

        copy_btn = ttk.Button(button_frame, text="Copy to Clipboard",
                               command=self.on_copy)
        copy_btn.pack(fill="x")

        # --- History ---
        history_frame = ttk.Frame(self)
        history_frame.pack(fill="both", expand=True, **pad)
        ttk.Label(history_frame, text=f"History (last {HISTORY_LIMIT}, this session only)").pack(anchor="w")

        self.history_listbox = tk.Listbox(
            history_frame, height=5, font=("Consolas", 10),
            bg="#2c2c40", fg="#f0f0f5", relief="flat", highlightthickness=0
        )
        self.history_listbox.pack(fill="both", expand=True, pady=(4, 0))

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_length_change(self, _event=None):
        self.length_value_label.config(text=str(int(self.length_var.get())))

    def on_generate(self):
        length = int(self.length_var.get())

        try:
            password = generate_password(
                length=length,
                use_upper=self.use_upper.get(),
                use_lower=self.use_lower.get(),
                use_digits=self.use_digits.get(),
                use_symbols=self.use_symbols.get(),
                exclude_ambiguous=self.exclude_ambiguous.get(),
                min_length=MIN_LENGTH,
            )
        except PasswordGenerationError as e:
            messagebox.showerror("Cannot generate password", str(e))
            return

        self.password_var.set(password)
        self._update_strength(password)
        self._add_to_history(password)

        # Auto-copy on generation, as required by the spec
        self._copy_to_clipboard(password, silent=True)

    def on_copy(self):
        password = self.password_var.get()
        if not password or password == "Click Generate":
            messagebox.showwarning("Nothing to copy", "Generate a password first.")
            return
        self._copy_to_clipboard(password, silent=False)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _copy_to_clipboard(self, password, silent=False):
        if not CLIPBOARD_AVAILABLE:
            if not silent:
                messagebox.showwarning(
                    "pyperclip not installed",
                    "Install it with:\n\npip install pyperclip"
                )
            return
        try:
            pyperclip.copy(password)
            if not silent:
                messagebox.showinfo("Copied", "Password copied to clipboard!")
        except Exception as e:
            if not silent:
                messagebox.showerror("Clipboard error", str(e))

    def _update_strength(self, password):
        strength = calculate_strength(
            password,
            use_upper=self.use_upper.get(),
            use_lower=self.use_lower.get(),
            use_digits=self.use_digits.get(),
            use_symbols=self.use_symbols.get(),
        )
        self.strength_label.config(text=f"Strength: {strength}")

        self.strength_canvas.delete("all")
        self.update_idletasks()
        width = self.strength_canvas.winfo_width() or 400
        fraction = STRENGTH_FRACTION.get(strength, 0)
        color = STRENGTH_COLORS.get(strength, "#888888")
        self.strength_canvas.create_rectangle(
            0, 0, width * fraction, 14, fill=color, outline=""
        )

    def _add_to_history(self, password):
        self.history.insert(0, password)
        self.history = self.history[:HISTORY_LIMIT]

        self.history_listbox.delete(0, tk.END)
        for pw in self.history:
            self.history_listbox.insert(tk.END, pw)


def main():
    app = PasswordGeneratorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
