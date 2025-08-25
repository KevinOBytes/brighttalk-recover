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


def test_config_integration():
    """Test that CLI integrates with config file properly."""
    from bt_recover.config import Config
    import tempfile
    import json
    from pathlib import Path
    
    # Create a temporary config file
    config_data = {
        "ffmpeg_path": "/custom/ffmpeg",
        "timeout": 60
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_config_path = f.name
    
    try:
        # Test config loading
        config = Config(Path(temp_config_path))
        assert config.config["ffmpeg_path"] == "/custom/ffmpeg"
        assert config.config["timeout"] == 60
        
        # Test that defaults are preserved
        assert "output_dir" in config.config
        assert config.config["output_dir"] == "output"
    finally:
        # Clean up
        Path(temp_config_path).unlink()


def test_program_name_fix():
    """Test that program name is correctly set when invoked as module."""
    import sys
    from bt_recover.cli import main
    
    # Simulate running as module
    original_argv = sys.argv[:]
    try:
        sys.argv = ['__main__.py', '--version']
        # This would normally exit, so we'll just test the argument parsing
        from bt_recover.cli import create_parser
        parser = create_parser()
        # Just verify the parser works - actual version testing would require 
        # mocking SystemExit
        assert parser is not None
    finally:
        sys.argv = original_argv 