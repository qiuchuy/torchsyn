#!/usr/bin/env python3
"""
Create a dataset from generated C programs with inline and non-inline versions.
Output formats: JSON, JSONL (for Hugging Face datasets), and Parquet.
"""

import argparse
import json
import os
import glob
from datetime import datetime


def find_program_pairs(generated_dir: str):
    """Find pairs of inline and non-inline programs."""
    pairs = []

    # Find all non-inline files
    noinline_files = glob.glob(os.path.join(generated_dir, "*_noinline.c"))

    for noinline_path in noinline_files:
        # Find corresponding inline file
        inline_path = noinline_path.replace("_noinline.c", ".c")

        if os.path.exists(inline_path):
            pairs.append({"inline_path": inline_path, "noinline_path": noinline_path})

    return pairs


def read_file(path: str) -> str:
    """Read file contents."""
    with open(path, "r") as f:
        return f.read()


def create_dataset_entry(inline_path: str, noinline_path: str, idx: int) -> dict:
    """Create a single dataset entry from a pair of files.

    - before: non-inlined version (original function calls)
    - after: inlined version (code expanded in model_forward)
    """
    after_code = read_file(inline_path)  # inlined version = after
    before_code = read_file(noinline_path)  # non-inlined version = before

    # Extract some metadata
    after_lines = after_code.count("\n")
    before_lines = before_code.count("\n")

    # Count inlined operations (marked with /* INLINED */)
    inlined_count = after_code.count("/* INLINED */")

    # Count variant uses
    variant_count = after_code.count("/* variant")

    return {
        "id": idx,
        "filename": os.path.basename(inline_path),
        "before": before_code,
        "after": after_code,
        "before_lines": before_lines,
        "after_lines": after_lines,
        "inlined_ops_count": inlined_count,
        "variant_count": variant_count,
        "line_diff": after_lines - before_lines,
        "created_at": datetime.now().isoformat(),
    }


def save_json(data: list, output_path: str):
    """Save dataset as JSON."""
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved JSON dataset: {output_path}")


def save_jsonl(data: list, output_path: str):
    """Save dataset as JSONL (one JSON per line, for Hugging Face datasets)."""
    with open(output_path, "w") as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"✓ Saved JSONL dataset: {output_path}")


def save_parquet(data: list, output_path: str):
    """Save dataset as Parquet (requires pandas and pyarrow)."""
    try:
        import pandas as pd

        df = pd.DataFrame(data)
        df.to_parquet(output_path, index=False)
        print(f"✓ Saved Parquet dataset: {output_path}")
    except ImportError:
        print("⚠ Parquet export requires pandas and pyarrow. Skipping.")


def main():
    parser = argparse.ArgumentParser(
        description="Create dataset from generated C programs"
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        default="generated",
        help="Directory containing generated C programs",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="dataset/c_programs",
        help="Output path prefix for dataset files",
    )
    parser.add_argument(
        "--format",
        type=str,
        nargs="+",
        default=["json", "jsonl"],
        choices=["json", "jsonl", "parquet"],
        help="Output formats",
    )
    args = parser.parse_args()

    # Find program pairs
    pairs = find_program_pairs(args.input_dir)

    if not pairs:
        print(f"No program pairs found in {args.input_dir}")
        print("Make sure to run c_wrapper.py with --with_non_inline first")
        return

    print(f"Found {len(pairs)} program pair(s)")

    # Create dataset entries
    dataset = []
    for idx, pair in enumerate(pairs):
        entry = create_dataset_entry(pair["inline_path"], pair["noinline_path"], idx)
        dataset.append(entry)
        print(f"  [{idx+1}/{len(pairs)}] {entry['filename']}")
        print(
            f"    - Before: {entry['before_lines']} lines, After: {entry['after_lines']} lines (+{entry['line_diff']})"
        )
        print(
            f"    - Inlined ops: {entry['inlined_ops_count']}, Variants: {entry['variant_count']}"
        )

    # Create output directory
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Save in requested formats
    if "json" in args.format:
        save_json(dataset, f"{args.output}.json")

    if "jsonl" in args.format:
        save_jsonl(dataset, f"{args.output}.jsonl")

    if "parquet" in args.format:
        save_parquet(dataset, f"{args.output}.parquet")

    print(f"\nDataset created with {len(dataset)} entries")
    print("\nTo view the dataset:")
    print("  - JSON: Open with any text editor or JSON viewer")
    print(
        "  - JSONL: Use Hugging Face datasets: datasets.load_dataset('json', data_files='dataset/c_programs.jsonl')"
    )
    print("  - Or use the built-in viewer: python view_dataset.py")


if __name__ == "__main__":
    main()
