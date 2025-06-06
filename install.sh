#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
VENV_DIR=".venv"
PYTHON_CMD="python3"

# --- Helper Functions ---
print_info() {
    echo "INFO: $1"
}

print_success() {
    echo "SUCCESS: $1"
}

print_error() {
    echo "ERROR: $1" >&2
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

check_python() {
    print_info "Checking for Python 3..."
    if ! command_exists $PYTHON_CMD; then
        print_error "$PYTHON_CMD is not found. Please install Python 3."
        exit 1
    fi
    # Optionally, add version check here if needed
    print_success "Python 3 found."
}

check_pip() {
    print_info "Checking for pip for $PYTHON_CMD..."
    if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
        print_error "pip for $PYTHON_CMD is not available."
        print_info "Please ensure pip is installed for your Python 3 distribution."
        print_info "On Debian/Ubuntu, try: sudo apt install python3-pip"
        print_info "On Fedora, try: sudo dnf install python3-pip"
        exit 1
    fi
    print_success "pip for $PYTHON_CMD found."
}

check_venv() {
    print_info "Checking for venv module for $PYTHON_CMD..."
    # Try to import venv module, if it fails, venv is likely not installed or not working
    if ! $PYTHON_CMD -c "import venv" >/dev/null 2>&1; then
        print_error "The venv module for $PYTHON_CMD is not available or not functional."
        print_info "Please ensure the Python 3 venv module is installed."
        print_info "On Debian/Ubuntu, try: sudo apt install python3-venv"
        print_info "On Fedora, try: sudo dnf install python3-venv"
        # On some systems, it might be part of the core python package, but often it's separate.
        exit 1
    fi
    print_success "venv module for $PYTHON_CMD found."
}

check_mpv() {
    print_info "Checking for mpv media player..."
    if ! command_exists mpv; then
        print_error "mpv is not found. mpv is required for video playback."
        print_info "Please install mpv using your system's package manager."
        if command_exists apt; then
            print_info "Suggestion for Debian/Ubuntu: sudo apt update && sudo apt install mpv"
        elif command_exists dnf; then
            print_info "Suggestion for Fedora: sudo dnf install mpv"
        elif command_exists pacman; then
            print_info "Suggestion for Arch Linux: sudo pacman -S mpv"
        fi
        exit 1
    fi
    print_success "mpv found."
}

create_virtual_env() {
    if [ -d "$VENV_DIR" ]; then
        print_info "Virtual environment '$VENV_DIR' already exists. Skipping creation."
    else
        print_info "Creating Python virtual environment in '$VENV_DIR'..."
        if $PYTHON_CMD -m venv "$VENV_DIR"; then
            print_success "Virtual environment created."
        else
            print_error "Failed to create virtual environment."
            exit 1
        fi
    fi
}

install_dependencies() {
    print_info "Activating virtual environment and installing dependencies from requirements.txt..."
    # Source activate script and then run pip install
    # This is a bit tricky in a script because `source` affects the current shell.
    # It's often more robust to directly call the pip executable from the venv.
    if [ -f "$VENV_DIR/bin/pip" ]; then
        if "$VENV_DIR/bin/pip" install -r requirements.txt; then
            print_success "Python dependencies installed successfully."
        else
            print_error "Failed to install Python dependencies from requirements.txt."
            exit 1
        fi
    else
        print_error "Could not find pip in the virtual environment: $VENV_DIR/bin/pip"
        print_info "Ensure the virtual environment was created correctly."
        exit 1
    fi
}

# --- Main Script Logic ---
echo "----- VidTerm Setup Script -----"

# 1. Check System Dependencies
check_python
check_pip
check_venv
check_mpv

# 2. Create Virtual Environment
create_virtual_env

# 3. Install Python Dependencies
install_dependencies

# 4. Post-Installation Message
echo ""
print_success "VidTerm setup is complete!"
print_info "To run VidTerm:"
print_info "1. Activate the virtual environment: source $VENV_DIR/bin/activate"
print_info "2. Run the application: $PYTHON_CMD vidterm.py"
echo "--------------------------------"

exit 0
