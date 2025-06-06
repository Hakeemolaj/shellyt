#!/bin/bash
# Ensure the virtual environment is active if you run this script directly
# source .venv/bin/activate
echo "Running unit tests..."
# Ensure vidterm.py can be imported by adding project root to PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH
python -m unittest discover -s tests -p "test_*.py"
# Or specific file: python -m unittest tests.test_vidterm
