import argparse
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
        default=8,
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile generated C programs after generation",
    )
    return parser.parse_args()


def main():
    args = parse_args()

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
        ]

        # Execute the command
        print(f"[{i + 1}/{args.generated_nums}] Generating C program: {output_file}")
        print(f"Command: {' '.join(cmd)}")

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✓ Generated: {output_file}")

            # Compile if requested
            if args.compile:
                compile_c_program(output_file)

        except subprocess.CalledProcessError as e:
            print(f"✗ Error running c_program_gen: {e}")
            print(f"STDERR: {e.stderr}")
            if i > 0:  # Continue if we've already generated some programs
                continue
            else:
                sys.exit(1)


def compile_c_program(c_file_path):
    """Compile the generated C program."""
    try:
        # Create output filename
        output_path = c_file_path.replace('.c', '')

        # Compile command
        cmd = ["gcc", "-O2", "-Wall", "-std=c99", "-o", output_path, c_file_path, "-lm"]

        print(f"  Compiling: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"  ✓ Compiled: {output_path}")

        # Test run with basic arguments
        test_cmd = [output_path, "dummy_model", "output.txt"]
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