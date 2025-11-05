# TorchSyn

TorchSyn is a PyTorch program synthesis tool that serves as a wrapper around NNSmith for generating random neural network programs. The project uses NNSmith as a git submodule to automatically generate diverse and valid PyTorch models and C programs for testing and research purposes.

## Install

### Requirement
torch>=2.0.0

### Install `NNSmith`
```bash
git submodule update --init --recursive
cd nnsmith
pip install -e ".[torch]"
```

## Usage

### PyTorch Program Generation
```bash
usage: wrapper.py [-h] [--output_path OUTPUT_PATH] [--generated_nums GENERATED_NUMS]

Wrapper for nnsmith.torch_program_gen CLI tool

options:
  -h, --help            show this help message and exit
  --output_path OUTPUT_PATH
                        Base path to save the generated programs (automatic numbering will be added)
  --generated_nums GENERATED_NUMS
                        Number of programs to generate
```

### C Program Generation
```bash
usage: c_wrapper.py [-h] [--output_path OUTPUT_PATH] [--generated_nums GENERATED_NUMS] [--max_nodes MAX_NODES] [--compile]

Wrapper for nnsmith.c_program_gen CLI tool

options:
  -h, --help            show this help message and exit
  --output_path OUTPUT_PATH
                        Base path to save the generated C programs (automatic numbering will be added)
  --generated_nums GENERATED_NUMS
                        Number of C programs to generate
  --max_nodes MAX_NODES
                        Maximum number of nodes in generated graphs
  --compile             Compile generated C programs after generation
```

## Running Generated C Programs

### Prerequisites
- GCC compiler (or any C99-compatible compiler)
- Math library support (-lm flag)

### Compilation

#### Method 1: Using the Wrapper (Recommended)
```bash
# Generate and compile C programs in one step
python c_wrapper.py --output_path generated/my_c_program --generated_nums 5 --compile

# The wrapper will automatically compile the programs and place executables in the same directory
```

#### Method 2: Manual Compilation
```bash
# Compile a specific C program
gcc -O2 -Wall -std=c99 -o generated/my_program generated/my_program.c -lm

# Compile with debugging symbols
gcc -g -O0 -Wall -std=c99 -o generated/my_program_debug generated/my_program.c -lm

# Compile with optimization and OpenMP support (if supported)
gcc -O3 -fopenmp -Wall -std=c99 -o generated/my_program_fast generated/my_program.c -lm
```

### Running the Executables

#### Basic Execution
```bash
# Run the compiled program
./generated/my_program
```

#### Program Output
Generated C programs typically:
- Execute neural network computations
- Print execution status and timing information
- Save output tensors to files or display results

### Example Workflow

```bash
# 1. Generate C programs
python c_wrapper.py --output_path generated/test_c --generated_nums 3 --max_nodes 5

# 2. Compile and run one program
gcc -O2 -Wall -std=c99 -o generated/test_c_0 generated/test_c_0_20251104_123456.c -lm
./generated/test_c_0

# 3. Check the output
ls -la generated/
# You should see both .c source files and compiled executables
```

### Program Structure

Generated C programs typically follow this structure:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

// Tensor utility functions
// Neural network operation implementations
// Model initialization and weight loading
// Main execution function

int main() {
    // Initialize model
    // Load weights
    // Run inference
    // Print results
    return 0;
}
```

### Advanced Usage

#### Custom Compilation Flags
```bash
# For performance profiling
gcc -O2 -pg -o program_profile program.c -lm
./program_profile
gprof ./program_profile gmon.out > analysis.txt

# For memory debugging
gcc -g -fsanitize=address -o program_asan program.c -lm
./program_asan
```

#### Batch Processing
```bash
# Generate, compile, and test multiple programs
for i in {1..10}; do
    python c_wrapper.py --output_path generated/batch_$i --generated_nums 1 --compile
    ./generated/batch_$i_*.exe
done
```
