# torchsyn

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




