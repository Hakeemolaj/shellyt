import yt_dlp
import json
import subprocess
import shlex
import asyncio # For running mpv and handling UI updates

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import TextArea, Label, Frame, Box # TextArea might still be used for results if that was the intention
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import message_dialog # For simple error popups

# --- Core yt-dlp and mpv logic ---

# Global application instance to access UI elements from functions
application_instance = None

def show_status_message(message, duration=None):
    """ Displays a message in the status bar. Clears after duration if specified. """
    if application_instance and hasattr(application_instance, 'status_bar_control'):
        application_instance.status_bar_control.text = message
        application_instance.invalidate()
        if duration:
            async def clear_message():
                await asyncio.sleep(duration)
                if application_instance.status_bar_control.text == message: # Clear only if not overwritten
                    application_instance.status_bar_control.text = get_default_status_text()
                application_instance.invalidate()
            asyncio.create_task(clear_message())

def get_default_status_text():
    return "VidTerm | (Ctrl-C/Q to quit) | (Up/Down, Enter to play)"

async def search_videos_async(query):
    show_status_message(f"Searching for: {query}...")
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'search',
        'default_search': 'ytsearch10:',
        'forcejson': True,
    }
    results = []
    try:
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = await loop.run_in_executor(None, lambda: ydl.extract_info(f"ytsearch10:{query}", download=False))

            if info_dict and 'entries' in info_dict:
                for entry in info_dict['entries']:
                    if entry and isinstance(entry, dict) and entry.get('id'):
                        results.append({
                            'id': entry.get('id'),
                            'title': entry.get('title', 'N/A'),
                            'uploader': entry.get('uploader', 'N/A'),
                            'duration_string': entry.get('duration_string', 'N/A')
                        })
        if not results:
            show_status_message(f"No results found for '{query}'.", 3)
        else:
            show_status_message(f"Found {len(results)} videos.", 3)
        return results
    except yt_dlp.utils.DownloadError as e:
        show_status_message(f"Search Error: {e}", 5)
    except Exception as e:
        show_status_message(f"Unexpected Search Error: {e}", 5)
    return []

async def get_stream_url_async(video_id):
    show_status_message(f"Fetching stream for {video_id}...")
    ydl_opts = {'quiet': True, 'format': 'best'}
    try:
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = await loop.run_in_executor(None, lambda: ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False))

            if info_dict and 'url' in info_dict:
                show_status_message(f"Stream ready for {video_id}.", 2)
                return info_dict['url']

            formats = info_dict.get('formats', [])
            for f in formats:
                if f.get('url'):
                    show_status_message(f"Stream ready for {video_id}.", 2)
                    return f['url']

            show_status_message("Could not find direct stream URL.", 3)
            return None
    except Exception as e:
        show_status_message(f"Error getting stream URL: {e}", 5)
        return None

async def play_video_in_terminal_async(video_id):
    show_status_message(f"Preparing video ID: {video_id}...")

    try:
        process = await asyncio.create_subprocess_exec('which', 'mpv', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        await process.wait()
        if process.returncode != 0:
            show_status_message("mpv not found. Please install mpv.", 5)
            if application_instance: # Check if app instance exists before calling dialog
                 await message_dialog(title="Error", text="mpv not found. Please install mpv to play videos.").run_async()
            return
    except FileNotFoundError:
        show_status_message("'which' command not found. Cannot check for mpv.", 5)
        if application_instance:
            await message_dialog(title="Error", text="'which' command not found. Cannot verify mpv installation.").run_async()
        return

    stream_url = await get_stream_url_async(video_id)
    if not stream_url:
        show_status_message("Failed to get stream URL. Cannot play video.", 3)
        return

    show_status_message(f"Starting playback: {video_id}. (mpv will take over)")

    if application_instance:
        await application_instance.suspend_to_background()

    try:
        command = ["mpv", stream_url, f"--title=VidTerm: {video_id}"]
        mpv_process = await asyncio.create_subprocess_exec(*command)
        await mpv_process.wait()
    except FileNotFoundError:
        show_status_message("mpv not found (during play attempt). Please install mpv.", 5)
    except Exception as e:
        show_status_message(f"Error during playback: {e}", 5)
    finally:
        if application_instance:
            application_instance.renderer.clear()
            await application_instance.resume_from_background()
        show_status_message(get_default_status_text(), 3)


# --- TUI Implementation ---
current_search_results = []
selected_video_index = 0

kb = KeyBindings()

@kb.add('c-c', eager=True)
@kb.add('c-q', eager=True)
def _(event):
    event.app.exit()

# --- Search Input Field: Refactored ---
# Accept handler for the search buffer
async def search_accept_handler_async(buffer_instance): # Renamed arg for clarity
    global current_search_results, selected_video_index, application_instance
    query = buffer_instance.text # Use text from the buffer passed to handler
    if query:
        current_search_results = await search_videos_async(query)
        selected_video_index = 0
        update_results_display()
    # buffer_instance.reset() # Optionally clear search field after search - keeping text can be useful

search_buffer = Buffer(
    accept_handler=lambda buf: asyncio.create_task(search_accept_handler_async(buf)),
    multiline=False
)
# Removed: search_field.accept_handler = ... (now part of Buffer constructor)

# Use BufferControl within a Window for the search field
search_input_control = BufferControl(buffer=search_buffer, focusable=True)
# This window will be the actual element you interact with for text input
search_field_window = Window(
    content=search_input_control,
    height=1,
    dont_extend_height=True # Important for single line input
)
# --- End of Search Input Field Refactor ---


results_text_area_control = FormattedTextControl(text="Enter a search query above and press Enter.") # Renamed for clarity
results_window = Window(content=results_text_area_control, wrap_lines=False, allow_scroll_beyond_bottom=False)

def update_results_display():
    global current_search_results, selected_video_index, results_text_area_control
    if not current_search_results:
        results_text_area_control.text = "No results found, or perform a search."
    else:
        formatted_results = []
        for i, video in enumerate(current_search_results):
            prefix = "[SELECTED] " if i == selected_video_index else "           "
            line = f"{prefix}{i+1}. {video['title']} ({video['duration_string']}) - {video['uploader']}"
            formatted_results.append(line)
        results_text_area_control.text = "\n".join(formatted_results)

    if application_instance:
        application_instance.invalidate()


@kb.add('down')
def _(event):
    global selected_video_index, current_search_results
    if current_search_results:
        selected_video_index = min(len(current_search_results) - 1, selected_video_index + 1)
        update_results_display()

@kb.add('up')
def _(event):
    global selected_video_index, current_search_results # Added current_search_results
    if current_search_results:
        selected_video_index = max(0, selected_video_index - 1)
        update_results_display()

# Ensure 'enter' for playback doesn't trigger if search field is focused.
# The focus check should refer to the new search_field_window or its control.
@kb.add('enter', filter=lambda: application_instance.layout.has_focus(search_field_window) == False)
def _(event):
    global current_search_results, selected_video_index
    if current_search_results and 0 <= selected_video_index < len(current_search_results):
        video_to_play = current_search_results[selected_video_index]
        asyncio.create_task(play_video_in_terminal_async(video_to_play['id']))

# Layout
status_bar_control = FormattedTextControl(get_default_status_text())
status_bar = Window(status_bar_control, height=1, style="reverse", align=WindowAlign.LEFT)

# Frame the search_field_window (the new input window)
search_frame = Frame(search_field_window, title="Search Query") # Changed search_field to search_field_window
results_frame = Frame(results_window, title="Results (Up/Down, Enter to play)")

body = HSplit([
    search_frame, # Use the refactored search_frame
    results_frame,
    status_bar
])

def main():
    global application_instance
    application_instance = Application(
        layout=Layout(body),
        key_bindings=kb,
        full_screen=True,
        mouse_support=True
    )
    application_instance.status_bar_control = status_bar_control

    update_results_display()
    asyncio.run(application_instance.run_async())

if __name__ == '__main__':
    main()
