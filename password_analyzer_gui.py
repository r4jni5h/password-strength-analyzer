import tkinter as tk
from tkinter import messagebox
from zxcvbn import zxcvbn
import os

# 🔐 Function to analyze password strength
def analyze_password(password):
    if not password:
        return None
    result = zxcvbn(password)
    return {
        "score": result["score"],
        "crack_time": result["crack_times_display"]["offline_fast_hashing_1e10_per_second"],
        "suggestions": result["feedback"]["suggestions"]
    }

# 🧠 Function to generate wordlist from personal info
def generate_wordlist(info_list, output_dir="output", output_file="wordlist.txt"):
    if not info_list:
        return None

    patterns = []
    for item in info_list:
        patterns.extend([
            item,
            item[::-1],
            item + "123",
            item + "@2025",
            item.upper()
        ])

    # Create output folder if not present
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, output_file)
    with open(filepath, "w") as f:
        for word in sorted(set(patterns)):
            f.write(word + "\n")

    return filepath

# 🖥️ GUI Application Class
class PasswordAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer")
        self.root.geometry("460x440")
        self.root.resizable(False, False)

        # --- Password Input Section ---
        tk.Label(root, text="🔐 Enter Password to Analyze:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(root, show="*", width=40)
        self.password_entry.pack(pady=5)
        tk.Button(root, text="Check Strength", command=self.check_strength).pack(pady=10)

        self.result_label = tk.Label(root, text="", fg="blue", wraplength=400, justify="left")
        self.result_label.pack(pady=5)

        # --- Wordlist Section ---
        tk.Label(root, text="🧠 Enter Personal Info (space-separated):", font=("Arial", 12)).pack(pady=10)
        self.info_entry = tk.Entry(root, width=40)
        self.info_entry.pack(pady=5)
        tk.Button(root, text="Generate Wordlist", command=self.handle_generate_wordlist).pack(pady=10)

        self.wordlist_status = tk.Label(root, text="", fg="green")
        self.wordlist_status.pack(pady=5)

    def check_strength(self):
        password = self.password_entry.get()
        result = analyze_password(password)
        if result:
            text = f"✅ Score: {result['score']}/4\n" \
                   f"🕒 Crack Time (Offline): {result['crack_time']}\n" \
                   f"💡 Suggestions: {', '.join(result['suggestions']) if result['suggestions'] else 'None'}"
            self.result_label.config(text=text)
        else:
            messagebox.showwarning("Missing Input", "Please enter a password.")

    def handle_generate_wordlist(self):
        raw_info = self.info_entry.get().strip()
        if not raw_info:
            messagebox.showwarning("Missing Input", "Please enter some info (name, pet, year, etc).")
            return
        info_list = raw_info.split()
        filepath = generate_wordlist(info_list)
        if filepath:
            self.wordlist_status.config(text=f"✅ Wordlist saved to: {filepath}")
        else:
            messagebox.showerror("Error", "Failed to generate wordlist.")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordAnalyzerApp(root)
    root.mainloop()
