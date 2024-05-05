import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Password Generator")
        self.master.geometry("400x300")

        self.length_label = ttk.Label(self.master, text="Password Length:")
        self.length_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.length_var = tk.IntVar(value=False)
        self.length_entry = ttk.Entry(self.master, textvariable=self.length_var)
        self.length_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.complexity_label = ttk.Label(self.master, text="Password Complexity:")
        self.complexity_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.use_letters_var = tk.BooleanVar(value=False)
        self.use_numbers_var = tk.BooleanVar(value=False)
        self.use_symbols_var = tk.BooleanVar(value=False)

        self.use_letters_checkbox = ttk.Checkbutton(self.master, text="Letters", variable=self.use_letters_var)
        self.use_numbers_checkbox = ttk.Checkbutton(self.master, text="Numbers", variable=self.use_numbers_var)
        self.use_symbols_checkbox = ttk.Checkbutton(self.master, text="Symbols", variable=self.use_symbols_var)

        self.use_letters_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.use_numbers_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.use_symbols_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.generate_button = ttk.Button(self.master, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=5, column=0, columnspan=4, padx=10, pady=20, sticky="w")

        self.result_label = ttk.Label(self.master, text="", font=("Helvetica", 9, "bold"))
        self.result_label.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")

    def generate_password(self):
        length = self.length_var.get()
        use_letters = self.use_letters_var.get()
        use_numbers = self.use_numbers_var.get()
        use_symbols = self.use_symbols_var.get()

        characters = ""
        if use_letters:
            characters += string.ascii_letters
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation

        if not characters:
            self.result_label.config(text="Error: Select at least one character type.")
            return

        password = []

        if use_letters:
            password.append(random.choice(string.ascii_letters))
        if use_numbers:
            password.append(random.choice(string.digits))
        if use_symbols:
            password.append(random.choice(string.punctuation))

        remaining_length = length - len(password)
        password.extend(random.choice(characters) for _ in range(max(remaining_length, 0)))

        random.shuffle(password)

        generated_password = ''.join(password)
        formatted_password = f"{generated_password}"
        self.result_label.config(text=f"Generated Password: {formatted_password}")

        # Copy the password to clipboard
        pyperclip.copy(generated_password)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

