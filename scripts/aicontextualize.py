#!/usr/bin/env python3
import argparse
import glob
from pathlib import Path

"""
REQUIREMENTS:

    sudo apt install xclip
    pip3 install pyperclip --break-system-packages
"""


def generate_context(patterns_string):
    """
    Finds files based on glob patterns, reads them, and formats them
    into a single string for an LLM context.
    """
    patterns = [p.strip() for p in patterns_string.split(',')]
    output_parts = []
    
    # Use a set to store found files to avoid duplicates
    found_files = set()

    for pattern in patterns:
        # The recursive=True flag allows the use of '**'
        matches = glob.glob(pattern, recursive=True)
        for match in matches:
            path = Path(match)
            # Ensure we only add files, not directories, and that they exist
            if path.is_file():
                found_files.add(path)

    if not found_files:
        return "No files found matching the provided patterns."

    # Sort files for a consistent order
    for filepath in sorted(found_files):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            output_parts.append(f"{filepath}\n```\n{content}\n```")
        except Exception as e:
            output_parts.append(f"Error reading file {filepath}: {e}")

    return "\n\n".join(output_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a formatted context of code files for LLMs.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "patterns",
        help="A comma-separated string of glob patterns to find files.\n"
             "Example: 'src/**/*.py,tests/test_*.py,README.md'"
    )
    parser.add_argument(
        "-c", "--clipboard",
        action="store_true",
        help="Copy the output to the clipboard instead of printing it."
    )
    args = parser.parse_args()

    context_string = generate_context(args.patterns)

    if args.copy:
        try:
            import pyperclip
            pyperclip.copy(context_string)
            print("✅ Context copied to clipboard!")
        except ImportError:
            print("Error: 'pyperclip' is not installed. Cannot copy to clipboard.")
            print("Please install it with: pip install pyperclip")
            print("\n--- Fallback: Printing to console ---\n")
            print(context_string)
    else:
        print(context_string)


if __name__ == "__main__":
    main()