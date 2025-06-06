# VidTerm - Watch and Search Videos in Your Linux Terminal

VidTerm is a Python-based command-line tool that allows you to search for videos (primarily from YouTube) and watch them directly in your Linux terminal using the `mpv` media player. It features a simple, text-based user interface (TUI) for ease of use.

## Features

*   Search for videos from platforms supported by `yt-dlp` (defaulting to YouTube).
*   Interactive Text-based User Interface (TUI) for searching and browsing results.
*   Playback of videos directly in the terminal using `mpv`.
*   Navigation of search results using keyboard shortcuts.
*   Status messages and error notifications within the TUI.

## Prerequisites

Before you begin, ensure you have the following installed on your Linux system:

*   **Python 3.7+**: VidTerm is written in Python 3. You can check your Python version with `python3 --version`.
*   **mpv Media Player**: This is essential for video playback.
    *   On Debian/Ubuntu: `sudo apt update && sudo apt install mpv`
    *   On Fedora: `sudo dnf install mpv`
    *   On Arch Linux: `sudo pacman -S mpv`
    *   For other distributions, please refer to their package manager documentation.
*   **yt-dlp**: While installed as a Python dependency, `yt-dlp` is the core engine for fetching video information.
*   **`which` command**: Used by the script to detect if `mpv` is installed. This is typically available by default on most Linux systems.

## Installation

1.  **Get the script:**
    *   If you have cloned this repository: `git clone <repository_url>` and `cd <repository_directory>`
    *   Otherwise, ensure you have the `vidterm.py` script.

2.  **Create a Python virtual environment:**
    ```bash
    python3 -m venv .venv
    ```

3.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```
    *(To deactivate later, simply type `deactivate`)*

4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Ensure your virtual environment is activated:**
    ```bash
    source .venv/bin/activate
    ```
    *(If you haven't already in the current terminal session)*

2.  **Run VidTerm:**
    ```bash
    python vidterm.py
    ```

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

*   **"mpv not found" message:** Ensure `mpv` is correctly installed and accessible in your system's PATH. Try running `mpv --version` in your terminal to verify.
*   **"which command not found" message:** This is unlikely but indicates the `which` utility is missing. It's a standard Linux utility.
*   **Python errors:** Ensure you are using Python 3.7+ and that all dependencies were installed correctly in an active virtual environment.
*   **Video playback issues:** These could be due to `mpv` configuration, network problems, or issues with the video stream itself. Test `mpv` with a direct YouTube URL (`mpv "youtube_url"`) to isolate the issue.
