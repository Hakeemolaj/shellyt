import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

# Assuming vidterm.py is in the parent directory or PYTHONPATH is set up
# For simplicity in subtask, we might need to adjust path or copy vidterm.py
# For now, let's assume it can be imported if tests are run from project root.
# If not, the subtask runner might need to handle this.
import vidterm

# Helper to run async tests
def async_test(f):
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

class TestVidtermVideoFunctions(unittest.TestCase):

    @patch('yt_dlp.YoutubeDL')
    @async_test
    async def test_search_videos_async_success(self, MockYoutubeDL):
        # Mock the context manager and its extract_info method
        mock_ydl_instance = MockYoutubeDL.return_value.__enter__.return_value
        mock_ydl_instance.extract_info = MagicMock(return_value={
            'entries': [
                {'id': '123', 'title': 'Test Video 1', 'uploader': 'User1', 'duration_string': '10:00'},
                {'id': '456', 'title': 'Test Video 2', 'uploader': 'User2', 'duration_string': '05:30'}
            ]
        })

        # Mock the global application_instance and its status bar for show_status_message
        with patch('vidterm.application_instance', MagicMock()) as mock_app:
            mock_app.status_bar_control = MagicMock()
            mock_app.invalidate = MagicMock()
            vidterm.show_status_message = MagicMock() # Also mock this helper directly

            results = await vidterm.search_videos_async("test query")

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], '123')
        self.assertEqual(results[0]['title'], 'Test Video 1')
        self.assertEqual(results[1]['id'], '456')
        self.assertEqual(results[1]['title'], 'Test Video 2')
        mock_ydl_instance.extract_info.assert_called_once_with("ytsearch10:test query", download=False)
        vidterm.show_status_message.assert_any_call("Searching for: test query...")


    @patch('yt_dlp.YoutubeDL')
    @async_test
    async def test_search_videos_async_no_results(self, MockYoutubeDL):
        mock_ydl_instance = MockYoutubeDL.return_value.__enter__.return_value
        mock_ydl_instance.extract_info = MagicMock(return_value={'entries': []})

        with patch('vidterm.application_instance', MagicMock()) as mock_app:
            mock_app.status_bar_control = MagicMock()
            vidterm.show_status_message = MagicMock()
            results = await vidterm.search_videos_async("empty query")

        self.assertEqual(len(results), 0)
        vidterm.show_status_message.assert_any_call("No results found for 'empty query'.", 3)

    @patch('yt_dlp.YoutubeDL')
    @async_test
    async def test_search_videos_async_download_error(self, MockYoutubeDL):
        mock_ydl_instance = MockYoutubeDL.return_value.__enter__.return_value
        # Simulate a yt-dlp DownloadError
        # Need to ensure yt_dlp.utils is available or mock DownloadError itself if not
        # For now, assuming yt_dlp is in the environment for the test execution context
        mock_ydl_instance.extract_info = MagicMock(side_effect=yt_dlp.utils.DownloadError("Simulated download error"))

        with patch('vidterm.application_instance', MagicMock()) as mock_app:
            mock_app.status_bar_control = MagicMock()
            vidterm.show_status_message = MagicMock()
            results = await vidterm.search_videos_async("error query")

        self.assertEqual(len(results), 0)
        vidterm.show_status_message.assert_any_call("Search Error: Simulated download error", 5)


    @patch('yt_dlp.YoutubeDL')
    @async_test
    async def test_get_stream_url_async_success_direct_url(self, MockYoutubeDL):
        mock_ydl_instance = MockYoutubeDL.return_value.__enter__.return_value
        mock_ydl_instance.extract_info = MagicMock(return_value={'url': 'http://example.com/stream.mp4'})

        with patch('vidterm.application_instance', MagicMock()) as mock_app:
            mock_app.status_bar_control = MagicMock()
            vidterm.show_status_message = MagicMock()
            url = await vidterm.get_stream_url_async('video123')

        self.assertEqual(url, 'http://example.com/stream.mp4')
        mock_ydl_instance.extract_info.assert_called_once_with("https://www.youtube.com/watch?v=video123", download=False)
        vidterm.show_status_message.assert_any_call("Stream ready for video123.", 2)

    @patch('yt_dlp.YoutubeDL')
    @async_test
    async def test_get_stream_url_async_success_from_formats(self, MockYoutubeDL):
        mock_ydl_instance = MockYoutubeDL.return_value.__enter__.return_value
        mock_ydl_instance.extract_info = MagicMock(return_value={
            'formats': [{'url': 'http://example.com/format_stream.mp4'}]
        })
        with patch('vidterm.application_instance', MagicMock()) as mock_app:
            mock_app.status_bar_control = MagicMock()
            vidterm.show_status_message = MagicMock()
            url = await vidterm.get_stream_url_async('video456')

        self.assertEqual(url, 'http://example.com/format_stream.mp4')
        vidterm.show_status_message.assert_any_call("Stream ready for video456.", 2)

    @patch('yt_dlp.YoutubeDL')
    @async_test
    async def test_get_stream_url_async_no_url(self, MockYoutubeDL):
        mock_ydl_instance = MockYoutubeDL.return_value.__enter__.return_value
        mock_ydl_instance.extract_info = MagicMock(return_value={'formats': []}) # No url, no formats with url

        with patch('vidterm.application_instance', MagicMock()) as mock_app:
            mock_app.status_bar_control = MagicMock()
            vidterm.show_status_message = MagicMock()
            url = await vidterm.get_stream_url_async('video789')

        self.assertIsNone(url)
        vidterm.show_status_message.assert_any_call("Could not find direct stream URL.", 3)

    @patch('yt_dlp.YoutubeDL')
    @async_test
    async def test_get_stream_url_async_download_error(self, MockYoutubeDL):
        mock_ydl_instance = MockYoutubeDL.return_value.__enter__.return_value
        mock_ydl_instance.extract_info = MagicMock(side_effect=yt_dlp.utils.DownloadError("Stream fetch error"))

        with patch('vidterm.application_instance', MagicMock()) as mock_app:
            mock_app.status_bar_control = MagicMock()
            vidterm.show_status_message = MagicMock()
            url = await vidterm.get_stream_url_async('video_error')

        self.assertIsNone(url)
        vidterm.show_status_message.assert_any_call("Error getting stream URL: Stream fetch error", 5)


if __name__ == '__main__':
    # This allows running the tests directly via `python tests/test_vidterm.py`
    # It might be necessary to adjust PYTHONPATH if vidterm is not found.
    # e.g., export PYTHONPATH=$(pwd):$PYTHONPATH (from project root)
    unittest.main()
