#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'nnsmith'))

from nnsmith.cli.torch_program_gen import main

if __name__ == "__main__":
    # Override the default backend to use C
    sys.argv = [
        'torch_program_gen',
        'mgen.torch_program_path=generated/test_c_program_with_ops.py',
        'model.type=c'
    ]
    main()