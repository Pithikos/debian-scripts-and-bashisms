#!/usr/bin/env python3
import argparse
import glob
from pathlib import Path
import sys

"""
Generates a formatted context of code files for Large Language Models.

REQUIREMENTS:
    # On Debian/Ubuntu for clipboard support
    sudo apt install xclip
    
    # Python dependency for clipboard
    pip install pyperclip
"""

def find_and_read_files(patterns_string):
    """
    Finds all unique, sorted file paths matching the glob patterns,
    skipping any files that are empty or contain only whitespace.
    Returns a list of tuples: [(pathlib.Path, str_content), ...].
    """
    patterns = [p.strip() for p in patterns_string.split(',')]
    found_files = {} # Use a dict to store Path: content, ensuring uniqueness

    for pattern in patterns:
        for match in glob.glob(pattern, recursive=True):
            path = Path(match)
            # Ensure it's a file and check size as a quick optimization
            if path.is_file() and path.stat().st_size > 0:
                try:
                    content = path.read_text(encoding='utf-8', errors='ignore')
                    # If content is not just whitespace, add it
                    if content.strip():
                        found_files[path] = content
                except Exception as e:
                    print(f"Warning: Could not read file {path}: {e}", file=sys.stderr)
    
    # Sort by path and return as a list of tuples
    sorted_paths = sorted(found_files.keys())
    return [(path, found_files[path]) for path in sorted_paths]


def get_content_slice(content, lines_spec):
    """
    Slices the content of a file based on a comma-separated spec string.
    Returns the sliced content and a user-friendly description.
    """
    all_lines = content.splitlines()
    total_lines = len(all_lines)
    selected_indices = set()

    for req in [s.strip() for s in lines_spec.split(',')]:
        try:
            start_str, end_str = req.split(':', 1)
            start = int(start_str) if start_str else None
            end = int(end_str) if end_str else None
            if start is not None and start > 0:
                start -= 1 # Convert 1-based to 0-based

            indices = range(*slice(start, end, None).indices(total_lines))
            selected_indices.update(indices)
        except (ValueError, TypeError):
            print(f"Error: Invalid slice format in --lines. Use 'START:END'. Got: '{req}'", file=sys.stderr)
            sys.exit(1)
    
    if not selected_indices:
        return "", f"(no lines selected from spec '{lines_spec}')"

    sorted_indices = sorted(list(selected_indices))
    output_blocks, current_block = [], []
    last_index = -2 # Guarantees the first line starts a new block

    for index in sorted_indices:
        if index > last_index + 1 and current_block:
            output_blocks.append("\n".join(current_block))
            current_block = []
        
        current_block.append(all_lines[index])
        last_index = index

    if current_block:
        output_blocks.append("\n".join(current_block))

    final_content = "\n\n[... content truncated ...]\n\n".join(output_blocks)
    return final_content, f"(lines {lines_spec})"


def generate_context(files_with_content, lines=None):
    """
    Formats the content of pre-read files into a single string.
    """
    output_parts = []
    for filepath, full_content in files_with_content:
        content_to_use = full_content
        slice_desc = ""

        if lines:
            content_to_use, slice_desc = get_content_slice(full_content, lines)
        
        header = f"{filepath} {slice_desc}".strip()
        output_parts.append(f"{header}\n```\n{content_to_use}\n```")

    return "\n\n".join(output_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a formatted context of code files for LLMs.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("patterns", help="A comma-separated string of glob patterns.")
    parser.add_argument("-c", "--clipboard", action="store_true", help="Copy output to clipboard.")
    parser.add_argument("-l", "--list-files", action="store_true", help="List matching non-empty files and exit.")
    parser.add_argument(
        "-L", "--lines", type=str, metavar="SPEC",
        help="Include specific line ranges from each file.\n"
             "Examples: ':20', '-15:', '50:75', ':10,-10:'"
    )
    args = parser.parse_args()
    
    # Find and read all non-empty files once.
    files_with_content = find_and_read_files(args.patterns)
    
    if not files_with_content:
        print("No non-empty files found matching the provided patterns.", file=sys.stderr)
        sys.exit(0)

    if args.list_files:
        for filepath, _ in files_with_content:
            print(filepath)
        sys.exit(0)

    generated_context = generate_context(files_with_content, args.lines)
    
    context_string = f"CODE CONTEXT\n\n{generated_context}"

    if args.clipboard:
        try:
            import pyperclip
            pyperclip.copy(context_string)
            print("✅ Context copied to clipboard!")
        except Exception as e:
            print(f"Error: Could not copy to clipboard. Is 'xclip' installed?", file=sys.stderr)
            print(f"({e})\n\n--- Fallback: Printing to console ---\n", file=sys.stderr)
            print(context_string)
    else:
        print(context_string)

if __name__ == "__main__":
    main()