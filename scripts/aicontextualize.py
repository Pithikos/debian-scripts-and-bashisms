#!/usr/bin/env python3
import argparse
import glob
from pathlib import Path
import sys
import re

def parse_patterns(patterns_string):
    """
    Splits patterns into include and exclude glob patterns.
    Excludes are prefixed with '-'.
    """
    includes = []
    excludes = []

    for raw in patterns_string.split(","):
        p = raw.strip()
        if not p:
            continue
        if p.startswith("-"):
            excludes.append(p[1:])
        else:
            includes.append(p)

    if not includes:
        print("Error: At least one include pattern is required.", file=sys.stderr)
        sys.exit(1)

    return includes, excludes


def is_excluded(path: Path, exclude_patterns):
    """
    Checks whether a path matches any exclude glob.
    """
    for pat in exclude_patterns:
        if path.match(pat) or any(parent.match(pat) for parent in path.parents):
            return True
    return False


def find_and_read_files(patterns_string, content_filters=None):
    includes, excludes = parse_patterns(patterns_string)
    found_files = {}

    compiled_filters = []
    if content_filters:
        for p in content_filters.split(","):
            try:
                compiled_filters.append(re.compile(p.strip(), re.I | re.M))
            except re.error as e:
                print(f"Invalid regex '{p}': {e}", file=sys.stderr)
                sys.exit(1)

    for pattern in includes:
        for match in glob.glob(pattern, recursive=True):
            path = Path(match)

            if is_excluded(path, excludes):
                continue

            if not path.is_file():
                continue

            if path.stat().st_size == 0:
                continue

            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                print(f"Warning: could not read {path}: {e}", file=sys.stderr)
                continue

            if not content.strip():
                continue

            if compiled_filters and not any(r.search(content) for r in compiled_filters):
                continue

            found_files[path] = content

    return [(p, found_files[p]) for p in sorted(found_files)]


def get_content_slice(content, lines_spec):
    all_lines = content.splitlines()
    total = len(all_lines)
    selected = set()

    for spec in lines_spec.split(","):
        try:
            a, b = spec.split(":", 1)
            start = int(a) - 1 if a else None
            end = int(b) if b else None
            selected.update(range(*slice(start, end).indices(total)))
        except Exception:
            print(f"Invalid --lines spec: {spec}", file=sys.stderr)
            sys.exit(1)

    if not selected:
        return "", "(no lines selected)"

    blocks, block = [], []
    last = -2

    for i in sorted(selected):
        if i > last + 1 and block:
            blocks.append("\n".join(block))
            block = []
        block.append(all_lines[i])
        last = i

    if block:
        blocks.append("\n".join(block))

    return "\n\n[...]\n\n".join(blocks), f"(lines {lines_spec})"


def generate_context(files, lines=None):
    out = []
    for path, content in files:
        slice_desc = ""
        if lines:
            content, slice_desc = get_content_slice(content, lines)

        out.append(f"{path} {slice_desc}\n```\n{content}\n```")

    return "\n\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("patterns", help="Glob patterns. Prefix with '-' to exclude.")
    parser.add_argument("-p", "--print", action="store_true", help="Print file contents.")
    parser.add_argument("-c", "--clipboard", action="store_true", help="Copy output to clipboard (implies --print).")
    parser.add_argument("-l", "--lines", help="Line slices (e.g. :20,10:50)")
    parser.add_argument("-f", "--filter", metavar="REGEX",
        help=(
            "Filter by file CONTENT using regex (not glob).\n"
            "Comma-separated patterns; file is included if ANY match.\n"
            "Examples: 'TODO|FIXME', 'class\\s+Actor,def\\s+run'"
        )
    )

    args = parser.parse_args()

    files = find_and_read_files(args.patterns, args.filter)

    if not files:
        print("No matching files.")
        sys.exit(0)

    if not (args.print or args.clipboard):
        for path, _ in files:
            print(path)
        sys.exit(0)

    context = "CODE CONTEXT\n\n" + generate_context(files, args.lines)

    if args.clipboard:
        try:
            import pyperclip
            pyperclip.copy(context)
            print("✅ Copied to clipboard")
        except Exception as e:
            print(f"Clipboard error: {e}", file=sys.stderr)
    else:
        print(context)


if __name__ == "__main__":
    main()