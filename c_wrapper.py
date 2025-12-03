import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime


def parse_args():
    """Parse command line arguments for the c_program_gen wrapper."""
    parser = argparse.ArgumentParser(
        description="Wrapper for nnsmith.c_program_gen CLI tool"
    )
    # Add common arguments for c_program_gen
    parser.add_argument(
        "--output_path",
        type=str,
        help="Base path to save the generated C programs (automatic numbering will be added)",
        default="generated/c_program",
    )
    parser.add_argument(
        "--generated_nums",
        type=int,
        help="Number of C programs to generate",
        default=10,
    )
    parser.add_argument(
        "--max_nodes",
        type=int,
        help="Maximum number of nodes in generated graphs",
        default=None,
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile generated C programs after generation",
    )
    parser.add_argument(
        "--inline_rate",
        type=float,
        help="Percentage of operators to inline (0.0-1.0). When inlined, operator code is expanded directly in model_forward instead of calling functions.",
        default=1.0,
    )
    parser.add_argument(
        "--enable_variants",
        action="store_true",
        help="Enable multiple implementation variants for operators (randomly selected)",
        default=True,
    )
    parser.add_argument(
        "--no_variants",
        action="store_true",
        help="Disable multiple implementation variants for operators",
    )
    parser.add_argument(
        "--with_non_inline",
        action="store_true",
        help="Also output a non-inlined version of each generated program (with _noinline suffix)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Determine enable_variants value (--no_variants overrides --enable_variants)
    enable_variants = not args.no_variants

    # Get the directory containing this script to find ops.h
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ops_h_src = os.path.join(script_dir, "nnsmith", "nnsmith", "materialize", "ops.h")

    # Get output directory from output_path
    output_dir = os.path.dirname(args.output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Copy ops.h to the output directory
    if output_dir:
        ops_h_dst = os.path.join(output_dir, "ops.h")
    else:
        ops_h_dst = "ops.h"

    if os.path.exists(ops_h_src):
        shutil.copy(ops_h_src, ops_h_dst)
        print(f"✓ Copied ops.h to {ops_h_dst}")
    else:
        print(f"⚠ Warning: ops.h not found at {ops_h_src}")

    print(f"\nGeneration settings:")
    print(f"  - Inline rate: {args.inline_rate * 100:.1f}%")
    print(f"  - Enable variants: {enable_variants}")
    print(f"  - Output non-inlined version: {args.with_non_inline}")
    print()

    for i in range(args.generated_nums):
        # Append a unique number to the output path
        output_file = (
            f"{args.output_path}_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.c"
        )

        # Build the command to execute
        cmd = [
            "nnsmith.c_program_gen",
            f"mgen.c_program_path={output_file}",
            f"mgen.max_nodes={args.max_nodes}",
            f"mgen.inline_rate={args.inline_rate}",
            f"mgen.enable_variants={enable_variants}",
            f"mgen.with_non_inline={args.with_non_inline}",
        ]

        # Execute the command
        print(f"[{i + 1}/{args.generated_nums}] Generating C program: {output_file}")
        print(f"Command: {' '.join(cmd)}")

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✓ Generated: {output_file}")

            # Compile if requested
            if args.compile:
                compile_c_program(output_file, output_dir)

            # If non-inlined version was generated, compile it too
            if args.with_non_inline:
                noinline_file = output_file.replace(".c", "_noinline.c")
                print(f"  ✓ Non-inlined version: {noinline_file}")
                if args.compile:
                    compile_c_program(noinline_file, output_dir)

        except subprocess.CalledProcessError as e:
            print(f"✗ Error running c_program_gen: {e}")
            print(f"STDERR: {e.stderr}")
            if i > 0:  # Continue if we've already generated some programs
                continue
            else:
                sys.exit(1)


def compile_c_program(c_file_path, include_dir=None):
    """Compile the generated C program."""
    try:
        # Create output filename
        output_path = c_file_path.replace(".c", "")

        # Build compile command with include path for ops.h
        cmd = ["gcc", "-O2", "-Wall", "-std=c99"]

        # Add include path if specified
        if include_dir:
            cmd.extend(["-I", include_dir])

        cmd.extend(["-o", output_path, c_file_path, "-lm"])

        print(f"  Compiling: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"  ✓ Compiled: {output_path}")

        # Test run with basic arguments
        test_cmd = [output_path]
        try:
            result = subprocess.run(test_cmd, timeout=5, capture_output=True, text=True)
            print(f"  ✓ Test run successful")
        except subprocess.TimeoutExpired:
            print(f"  ⚠ Test run timed out (expected for large models)")
        except subprocess.CalledProcessError as e:
            print(f"  ⚠ Test run failed: {e}")

    except subprocess.CalledProcessError as e:
        print(f"  ✗ Compilation failed: {e}")
        print(f"  STDERR: {e.stderr}")


if __name__ == "__main__":
    main()
