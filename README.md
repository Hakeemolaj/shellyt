# VidTerm - Watch and Search Videos in Your Linux Terminal

VidTerm is a Python-based command-line tool that allows you to search for videos (primarily from YouTube) and watch them directly in your Linux terminal using the `mpv` media player. It features a simple, text-based user interface (TUI) for ease of use.

This project includes an automated installation script (`install.sh`) and a convenient wrapper script (`run_vidterm.sh`) for easy setup and execution.

## Features

*   Search for videos from platforms supported by `yt-dlp` (defaulting to YouTube).
*   Interactive Text-based User Interface (TUI) for searching and browsing results.
*   Playback of videos directly in the terminal using `mpv`.
*   Navigation of search results using keyboard shortcuts.
*   Status messages and error notifications within the TUI.
*   Automated installation script (`install.sh`).
*   Wrapper script (`run_vidterm.sh`) for easy execution.

## Prerequisites

Before you begin, ensure you have the following installed on your Linux system:

*   **Python 3.7+**: VidTerm is written in Python 3. The `install.sh` script will check for `python3`.
    *   You can typically install it via your system's package manager (e.g., `sudo apt install python3 python3-pip python3-venv`).
*   **mpv Media Player**: This is essential for video playback. The `install.sh` script will check for `mpv` and provide installation suggestions if it's missing.
    *   On Debian/Ubuntu: `sudo apt update && sudo apt install mpv`
    *   On Fedora: `sudo dnf install mpv`
    *   On Arch Linux: `sudo pacman -S mpv`
*   **`git` (Optional, for cloning):** If you plan to clone the repository.
*   **Standard build tools (Optional):** Some Python packages might need them if they build from source, though `yt-dlp` and `prompt-toolkit` often have wheels. `python3-dev` or `python3-devel` can be useful.

The `install.sh` script will also verify the availability of `pip` and `venv` for your Python 3 installation.

## Installation

1.  **Get the VidTerm scripts:**
    *   If using git: `git clone <repository_url>` and `cd <repository_directory>`
    *   Otherwise, download `vidterm.py`, `install.sh`, `run_vidterm.sh`, and `requirements.txt` into the same directory.

2.  **Make the scripts executable:**
    ```bash
    chmod +x install.sh
    chmod +x run_vidterm.sh
    ```

3.  **Run the installation script:**
    ```bash
    ./install.sh
    ```
    This script will:
    *   Check for necessary dependencies (Python 3, pip, venv, mpv).
    *   Create a Python virtual environment named `.venv` in the current directory.
    *   Install the required Python packages into this virtual environment.

## Usage

1.  **Run VidTerm using the wrapper script:**
    ```bash
    ./run_vidterm.sh
    ```
    This script automatically uses the Python interpreter and packages from the `.venv` virtual environment. You do **not** need to manually activate the virtual environment.

### Keyboard Controls

Once VidTerm is running:

*   **Search Field:**
    *   Type your search query and press `Enter` to search.
*   **Results List:**
    *   Use `Arrow Up` and `Arrow Down` keys to navigate through the search results.
    *   Press `Enter` on a selected video to start playback with `mpv`.
*   **General:**
    *   Press `Ctrl-C` or `Ctrl-Q` to quit VidTerm at any time.

`mpv` will take over the terminal during playback. You can use `mpv`'s own keyboard shortcuts (e.g., `q` to quit playback, space to pause/play, arrow keys to seek). After `mpv` exits, you will return to VidTerm.

## Customization

If you need to pass specific options to `mpv` (e.g., for audio-only playback, video quality settings, etc.), you can modify the `mpv` command directly within the `vidterm.py` script. Look for the `command = ["mpv", stream_url, ...]` line in the `play_video_in_terminal_async` function.

Example: For audio-only playback, you could change it to:
`command = ["mpv", "--no-video", stream_url, ...]`

## Troubleshooting

*   **`install.sh` script errors:**
    *   Pay attention to messages from the script. It will guide you if Python 3, pip, venv, or mpv are missing.
    *   Ensure `install.sh` has execute permissions (`chmod +x install.sh`).
*   **`run_vidterm.sh` script errors:**
    *   This usually means `install.sh` was not run or did not complete successfully. Ensure the `.venv` directory exists and contains the necessary files.
    *   Ensure `run_vidterm.sh` has execute permissions.
*   **Video playback issues:**
    *   These could be due to `mpv` configuration, network problems, or issues with the video stream itself. Test `mpv` with a direct YouTube URL (`mpv "youtube_url"`) to isolate the issue.
*   **Other Python errors:**
    *   If you encounter Python errors after running `./run_vidterm.sh`, it might indicate an issue with the installed dependencies or the script itself. Ensure `requirements.txt` is up to date and all packages installed correctly.
