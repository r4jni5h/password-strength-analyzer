import tkinter as tk
from tkinter import messagebox
from zxcvbn import zxcvbn
import os

# GUI app
class PasswordAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer")
        self.root.geometry("450x400")
        self.root.resizable(False, False)

        # Password strength section
        tk.Label(root, text="🔐 Enter Password to Analyze:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(root, show="*", width=40)
        self.password_entry.pack(pady=5)
        tk.Button(root, text="Check Strength", command=self.check_strength).pack(pady=10)

        self.result_label = tk.Label(root, text="", fg="blue", wraplength=400)
        self.result_label.pack(pady=5)

        # Wordlist generator section
        tk.Label(root, text="🧠 Enter Personal Info (name, pet, year):", font=("Arial", 12)).pack(pady=10)
        self.info_entry = tk.Entry(root, width=40)
        self.info_entry.pack(pady=5)
        tk.Button(root, text="Generate Wordlist", command=self.generate_wordlist).pack(pady=10)

        self.wordlist_status = tk.Label(root, text="", fg="green")
        self.wordlist_status.pack(pady=5)

    def check_strength(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Input Error", "Please enter a password.")
            return
        result = zxcvbn(password)
        score = result['score']
        crack_time = result['crack_times_display']['offline_fast_hashing_1e10_per_second']
        suggestions = result['feedback']['suggestions']
        self.result_label.config(
            text=f"Score: {score}/4\nCrack Time (Offline): {crack_time}\nSuggestions: {', '.join(suggestions)}"
        )

    def generate_wordlist(self):
        info = self.info_entry.get().split()
        if not info:
            messagebox.showwarning("Input Error", "Please enter some info.")
            return
        patterns = []
        for item in info:
            patterns.extend([
                item, item[::-1], item + "123", item + "@2025", item.upper()
            ])
        if not os.path.exists("output"):
            os.makedirs("output")
        with open("output/wordlist.txt", "w") as f:
            for word in set(patterns):
                f.write(word + "\n")
        self.wordlist_status.config(text="✅ Wordlist saved to output/wordlist.txt")


# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordAnalyzerApp(root)
    root.mainloop()
