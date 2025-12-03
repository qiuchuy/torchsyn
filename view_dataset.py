#!/usr/bin/env python3
"""
Simple dataset viewer for comparing inline and non-inline C code.
Provides a terminal-based side-by-side comparison.
"""

import argparse
import json
import os


def load_dataset(path: str) -> list:
    """Load dataset from JSON or JSONL file."""
    if path.endswith(".jsonl"):
        data = []
        with open(path, "r") as f:
            for line in f:
                data.append(json.loads(line))
        return data
    else:
        with open(path, "r") as f:
            return json.load(f)


def truncate_code(code: str, max_lines: int = 50) -> str:
    """Truncate code to max_lines for display."""
    lines = code.split("\n")
    if len(lines) > max_lines:
        return (
            "\n".join(lines[:max_lines])
            + f"\n\n... ({len(lines) - max_lines} more lines)"
        )
    return code


def display_entry(entry: dict, show_full: bool = False):
    """Display a single dataset entry."""
    print("=" * 80)
    print(f"ID: {entry['id']} | File: {entry['filename']}")
    print(f"Created: {entry.get('created_at', 'N/A')}")
    print("-" * 80)
    print(f"Stats:")
    print(
        f"  - Before (non-inlined): {entry.get('before_lines', entry.get('noinline_lines', 'N/A'))} lines"
    )
    print(
        f"  - After (inlined): {entry.get('after_lines', entry.get('inline_lines', 'N/A'))} lines"
    )
    print(f"  - Line difference: {entry['line_diff']:+d}")
    print(f"  - Inlined operations: {entry['inlined_ops_count']}")
    print(f"  - Variant usages: {entry['variant_count']}")
    print("=" * 80)

    # Support both old and new field names
    before_code = entry.get("before", entry.get("noinline_code", ""))
    after_code = entry.get("after", entry.get("inline_code", ""))

    if show_full:
        print("\n### BEFORE (non-inlined) ###\n")
        print(before_code)
        print("\n### AFTER (inlined) ###\n")
        print(after_code)
    else:
        print("\n### BEFORE (non-inlined, truncated) ###\n")
        print(truncate_code(before_code))
        print("\n### AFTER (inlined, truncated) ###\n")
        print(truncate_code(after_code))


def find_inlined_sections(code: str) -> list:
    """Find and extract inlined code sections."""
    sections = []
    lines = code.split("\n")

    i = 0
    while i < len(lines):
        if "/* INLINED */" in lines[i]:
            start = i
            # Find the end of this inlined section (next allocation or function call)
            end = i + 1
            while (
                end < len(lines)
                and not lines[end].strip().startswith("//")
                and not "malloc" in lines[end]
            ):
                if lines[end].strip() and not lines[end].strip().startswith("/*"):
                    end += 1
                else:
                    break
            sections.append({"line": start + 1, "code": "\n".join(lines[start:end])})
            i = end
        else:
            i += 1

    return sections


def show_inlined_diff(entry: dict):
    """Show only the inlined sections."""
    print("=" * 80)
    print(f"Inlined Sections in: {entry['filename']}")
    print("=" * 80)

    after_code = entry.get("after", entry.get("inline_code", ""))
    sections = find_inlined_sections(after_code)

    if not sections:
        print("No inlined sections found.")
        return

    for i, section in enumerate(sections):
        print(f"\n--- Section {i+1} (line {section['line']}) ---")
        print(section["code"])


def interactive_mode(dataset: list):
    """Interactive mode for browsing the dataset."""
    current = 0

    while True:
        print("\n" + "=" * 80)
        print(f"Entry {current + 1}/{len(dataset)}")
        display_entry(dataset[current], show_full=False)

        print("\nCommands: [n]ext, [p]rev, [f]ull, [i]nlined sections, [q]uit")
        cmd = input("> ").strip().lower()

        if cmd == "n":
            current = (current + 1) % len(dataset)
        elif cmd == "p":
            current = (current - 1) % len(dataset)
        elif cmd == "f":
            display_entry(dataset[current], show_full=True)
            input("\nPress Enter to continue...")
        elif cmd == "i":
            show_inlined_diff(dataset[current])
            input("\nPress Enter to continue...")
        elif cmd == "q":
            break
        elif cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(dataset):
                current = idx
            else:
                print(f"Invalid index. Valid range: 1-{len(dataset)}")


def main():
    parser = argparse.ArgumentParser(
        description="View C code inline/non-inline dataset"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="dataset/c_programs.json",
        help="Path to dataset file (JSON or JSONL)",
    )
    parser.add_argument(
        "--entry", type=int, default=None, help="Display specific entry by index"
    )
    parser.add_argument(
        "--full", action="store_true", help="Show full code (not truncated)"
    )
    parser.add_argument(
        "--inlined", action="store_true", help="Show only inlined sections"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive browsing mode"
    )
    args = parser.parse_args()

    if not os.path.exists(args.dataset):
        # Try JSONL extension
        jsonl_path = args.dataset.replace(".json", ".jsonl")
        if os.path.exists(jsonl_path):
            args.dataset = jsonl_path
        else:
            print(f"Dataset not found: {args.dataset}")
            print("Run create_dataset.py first to generate the dataset.")
            return

    dataset = load_dataset(args.dataset)
    print(f"Loaded {len(dataset)} entries from {args.dataset}")

    if args.interactive:
        interactive_mode(dataset)
    elif args.entry is not None:
        if 0 <= args.entry < len(dataset):
            if args.inlined:
                show_inlined_diff(dataset[args.entry])
            else:
                display_entry(dataset[args.entry], show_full=args.full)
        else:
            print(f"Invalid entry index. Valid range: 0-{len(dataset)-1}")
    else:
        # Show all entries (summary)
        for entry in dataset:
            display_entry(entry, show_full=args.full)
            if not args.full:
                print()


if __name__ == "__main__":
    main()
