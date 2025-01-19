import pytest
import os
from unittest.mock import patch, MagicMock
from bt_recover.main import BrightTalkDownloader, FFmpegNotFoundError
from bt_recover.exceptions import URLValidationError

@pytest.fixture
def mock_ffmpeg():
    """Mock ffmpeg-related functions."""
    with patch('shutil.which') as mock_which, \
         patch('os.path.isfile') as mock_isfile, \
         patch('bt_recover.main.BrightTalkDownloader._verify_ffmpeg') as mock_verify:
        mock_which.return_value = '/usr/bin/ffmpeg'
        mock_isfile.return_value = True
        mock_verify.return_value = True
        yield {
            'which': mock_which,
            'isfile': mock_isfile,
            'verify': mock_verify
        }

def test_downloader_initialization(mock_ffmpeg):
    """Test basic initialization of downloader."""
    downloader = BrightTalkDownloader()
    assert not downloader.verbose
    assert not downloader.quiet
    assert not downloader.debug
    assert downloader.ffmpeg_path == '/usr/bin/ffmpeg'

def test_validate_url(mock_ffmpeg):
    """Test URL validation."""
    downloader = BrightTalkDownloader()
    
    # Should fail with invalid URL
    with pytest.raises(URLValidationError):
        downloader.validate_url("not-a-url")
    
    # Should fail with non-m3u8 URL
    with pytest.raises(URLValidationError):
        downloader.validate_url("https://example.com/video.mp4")

def test_ffmpeg_path_resolution(mock_ffmpeg):
    """Test ffmpeg path resolution."""
    # Test with custom path
    custom_path = "/custom/ffmpeg"
    mock_ffmpeg['verify'].return_value = True
    downloader = BrightTalkDownloader(ffmpeg_path=custom_path)
    assert downloader.ffmpeg_path == custom_path

    # Test with invalid custom path
    mock_ffmpeg['verify'].return_value = False
    with pytest.raises(FFmpegNotFoundError):
        BrightTalkDownloader(ffmpeg_path="/invalid/path")

def test_logging_levels(mock_ffmpeg):
    """Test different logging levels."""
    # Test quiet mode
    downloader = BrightTalkDownloader(quiet=True)
    with patch('builtins.print') as mock_print:
        downloader.log("test message")
        mock_print.assert_not_called()

    # Test debug mode
    downloader = BrightTalkDownloader(debug=True)
    with patch('builtins.print') as mock_print:
        downloader.log("test message", "debug")
        mock_print.assert_called_once()

@pytest.mark.parametrize("url,should_raise", [
    ("not-a-url", True),
    ("http://example.com/video.mp4", True),
    ("http://example.com/video.m3u8", False),
])
def test_url_validation(mock_ffmpeg, url, should_raise):
    """Test URL validation with different URLs."""
    downloader = BrightTalkDownloader()
    if should_raise:
        with pytest.raises(URLValidationError):
            downloader.validate_url(url)
    else:
        # Mock the requests.head call
        with patch('requests.head') as mock_head:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_head.return_value = mock_response
            downloader.validate_url(url)  # Should not raise 

def test_version():
    """Test version is properly formatted."""
    from bt_recover import __version__
    assert isinstance(__version__, str)
    # Version should be in format: x.y.z
    parts = __version__.split('.')
    assert len(parts) >= 2, "Version should have at least major.minor"
    assert all(part.isdigit() for part in parts), "Version parts should be numeric" 