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


def find_files(patterns_string):
    """Finds all unique, sorted file paths matching the glob patterns."""
    patterns = [p.strip() for p in patterns_string.split(',')]
    found_files = set()

    for pattern in patterns:
        matches = glob.glob(pattern, recursive=True)
        for match in matches:
            path = Path(match)
            if path.is_file():
                found_files.add(path)
                
    return sorted(list(found_files))


def get_content_slice(content, lines_spec):
    """
    Slices the content of a file based on a comma-separated spec string.
    Example spec: ':10,-10:' -> first 10 lines and last 10 lines.
    Returns the sliced content and a user-friendly description.
    """
    all_lines = content.splitlines()
    total_lines = len(all_lines)
    selected_indices = set()

    # Split the spec into individual slice requests (e.g., ':10', '-10:')
    slice_requests = [s.strip() for s in lines_spec.split(',')]

    for req in slice_requests:
        try:
            start_str, end_str = req.split(':', 1)
            
            # Use Python's slice(start, end) object for robust index handling
            start = int(start_str) if start_str else None
            end = int(end_str) if end_str else None

            # Convert 1-based indexing from user to 0-based for Python
            if start is not None and start > 0:
                start -= 1

            # Get the actual line indices covered by this slice
            indices = range(*slice(start, end, None).indices(total_lines))
            selected_indices.update(indices)

        except (ValueError, TypeError):
            print(f"Error: Invalid slice format in --lines. Use 'START:END'. Got: '{req}'", file=sys.stderr)
            sys.exit(1)
    
    if not selected_indices:
        return "", f"(no lines selected from spec '{lines_spec}')"

    # Reconstruct the content from the unique, sorted line indices
    sorted_indices = sorted(list(selected_indices))
    
    output_blocks = []
    current_block = []
    
    if not sorted_indices:
        return "", ""

    last_index = sorted_indices[0] - 1 # Start with a non-consecutive index

    for index in sorted_indices:
        # If there's a gap between the last line and this one, start a new block
        if index > last_index + 1 and current_block:
            output_blocks.append("\n".join(current_block))
            current_block = []
        
        current_block.append(all_lines[index])
        last_index = index

    # Add the final block of lines
    if current_block:
        output_blocks.append("\n".join(current_block))

    # Join the blocks with a truncation marker
    final_content = "\n\n[... content truncated ...]\n\n".join(output_blocks)
    slice_desc = f"(lines {lines_spec})"
    
    return final_content, slice_desc


def generate_context(found_files, lines=None):
    """
    Finds files based on glob patterns, reads them, and formats them
    into a single string for an LLM context.
    """
    output_parts = []

    for filepath in sorted(found_files):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                full_content = f.read()
            
            content_to_use = full_content
            slice_desc = ""

            if lines:
                content_to_use, slice_desc = get_content_slice(full_content, lines)
            
            header = f"{filepath}".strip()
            output_parts.append(f"{header}\n```\n{content_to_use}\n```")

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
             "Example: 'src/**/*.py,tests/test_*.py'"
    )
    parser.add_argument(
        "-c", "--clipboard",
        action="store_true",
        help="Copy the output to the clipboard instead of printing it."
    )
    parser.add_argument(
        "-L", "--lines",
        type=str,
        metavar="SPEC",
        help="Include specific line ranges from each file.\n"
             "The spec is a comma-separated list of 'START:END' slices.\n"
             "Examples:\n"
             "  ':20'         -> First 20 lines.\n"
             "  '-15:'        -> Last 15 lines.\n"
             "  '50:75'       -> Lines 50 to 75.\n"
             "  ':10,-10:'    -> First 10 AND last 10 lines."
    )
    parser.add_argument(
        "-l", "--list-files",
        action="store_true",
        help="List all files matching the patterns and exit."
    )
    
    args = parser.parse_args()
    
    found_files = find_files(args.patterns)
    
    # If --list-files is used, print paths and exit immediately.
    if args.list_files:
        for filepath in found_files:
            print(filepath)
        sys.exit(0)

    generated_context = generate_context(found_files, args.lines)
    context_string = f"""
CODE CONTEXT

{generated_context}
"""

    if args.clipboard:
        try:
            import pyperclip
            pyperclip.copy(context_string)
            print("✅ Context copied to clipboard!")
        except Exception as e:
            print(f"Error: Could not copy to clipboard. Is 'xclip' installed?", file=sys.stderr)
            print(f"({e})", file=sys.stderr)
            print("\n--- Fallback: Printing to console ---\n", file=sys.stderr)
            print(context_string)
    else:
        print(context_string)

if __name__ == "__main__":
    main()