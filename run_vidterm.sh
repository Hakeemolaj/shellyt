#!/bin/bash

# Determine the absolute directory where this script is located
SCRIPT_DIR_REL_PATH="$(dirname "${BASH_SOURCE[0]}")"
SCRIPT_DIR_ABS_PATH=$(cd "$SCRIPT_DIR_REL_PATH" &>/dev/null && pwd)

# Define paths relative to the script's location
VENV_PYTHON="$SCRIPT_DIR_ABS_PATH/.venv/bin/python"
VIDTERM_SCRIPT="$SCRIPT_DIR_ABS_PATH/vidterm.py"
VENV_DIR="$SCRIPT_DIR_ABS_PATH/.venv" # For checking venv existence

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "ERROR: Virtual environment directory '$VENV_DIR' not found."
    echo "Please run the ./install.sh script first to set up VidTerm."
    exit 1
fi

# Check if the Python interpreter in the virtual environment exists
if [ ! -x "$VENV_PYTHON" ]; then
    echo "ERROR: Python interpreter not found in virtual environment: $VENV_PYTHON"
    echo "The virtual environment might be corrupted or incomplete."
    echo "Please try running ./install.sh again."
    exit 1
fi

# Check if the main VidTerm script exists
if [ ! -f "$VIDTERM_SCRIPT" ]; then
    echo "ERROR: VidTerm script not found: $VIDTERM_SCRIPT"
    echo "Please ensure vidterm.py is in the same directory as this script."
    exit 1
fi

# Execute VidTerm using the virtual environment's Python interpreter
# "$@" passes all command-line arguments given to run_vidterm.sh to vidterm.py
"$VENV_PYTHON" "$VIDTERM_SCRIPT" "$@"

exit 0
