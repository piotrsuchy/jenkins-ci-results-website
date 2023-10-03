#!/bin/bash
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$PYTHONPATH:$script_dir/.."
robot --listener -r NONE -l NONE -o NONE "$script_dir/../tests/PythonListener.py" "$script_dir/../tests/$1.robot"
