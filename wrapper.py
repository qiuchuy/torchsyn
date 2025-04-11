import argparse
import subprocess
import sys
import argparse
from datetime import datetime


def parse_args():
    """Parse command line arguments for the torch_program_gen wrapper."""
    parser = argparse.ArgumentParser(
        description="Wrapper for nnsmith.torch_program_gen CLI tool"
    )
    # Add common arguments for torch_program_gen
    parser.add_argument(
        "--output_path",
        type=str,
        help="Base path to save the generated programs (automatic numbering will be added)",
        default=f"generated/torch_program",
    )
    parser.add_argument(
        "--generated_nums",
        type=int,
        help="Number of programs to generate",
        default=10,
    )
    return parser.parse_args()


def main():
    args = parse_args()

    for i in range(args.generated_nums):
        # Append a unique number to the output path
        output_file = (
            f"{args.output_path}_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )

        # Build the command to execute
        cmd = [
            "nnsmith.torch_program_gen",
            f"mgen.torch_program_path={output_file}",
        ]

        # Execute the command
        print(f"[{i + 1}/{args.generated_nums}] Executing: {' '.join(cmd)}")

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running torch_program_gen: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
