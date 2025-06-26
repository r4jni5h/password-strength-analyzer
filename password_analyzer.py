from zxcvbn import zxcvbn
import argparse
import os

# Analyze password
def analyze_password(password):
    result = zxcvbn(password)
    print("\nPassword Strength Score (0-4):", result['score'])
    print("Crack Time (offline):", result['crack_times_display']['offline_fast_hashing_1e10_per_second'])
    print("Feedback:", result['feedback'])

# Generate custom wordlist
def generate_wordlist(info, output_file="wordlist.txt"):
    patterns = []
    for item in info:
        patterns.append(item)
        patterns.append(item[::-1])
        patterns.append(item + "123")
        patterns.append(item + "@2025")
        patterns.append(item.upper())
    with open(output_file, "w") as f:
        for word in set(patterns):
            f.write(word + "\n")
    print(f"\nCustom wordlist saved to {output_file}")

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--password", help="Password to analyze")
    parser.add_argument("--info", nargs='*', help="Personal info for wordlist generation (e.g., name, pet, DOB)")
    args = parser.parse_args()

    if args.password:
        analyze_password(args.password)
    if args.info:
        generate_wordlist(args.info)
