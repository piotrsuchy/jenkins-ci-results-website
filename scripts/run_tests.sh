#!/bin/bash
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$PYTHONPATH:$script_dir/.."
robot --listener "$script_dir/../tests/PythonListener.py" "$script_dir/../tests/example_tests.robot"
