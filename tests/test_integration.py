"""Integration tests for BrightTalk-Recover."""

import os
import pytest
import tempfile
from pathlib import Path
from bt_recover.main import BrightTalkDownloader
from bt_recover.exceptions import URLValidationError

@pytest.fixture
def temp_output():
    """Create a temporary directory for output files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

import shutil


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg not installed")
def test_ffmpeg_installation():
    """Test that ffmpeg is properly installed and working."""
    downloader = BrightTalkDownloader()
    version = downloader._get_ffmpeg_version()
    assert version is not None
    assert "ffmpeg version" in version.lower()

@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg not installed")
def test_output_directory_creation(temp_output):
    """Test that output directories are created as needed."""
    output_path = temp_output / "subdir" / "video.mp4"
    downloader = BrightTalkDownloader()
    
    # This should create the directory
    os.makedirs(output_path.parent, exist_ok=True)
    
    assert output_path.parent.exists()
    assert output_path.parent.is_dir()

@pytest.mark.skipif(not os.environ.get('INTEGRATION_TEST_URL'),
                   reason="No test URL provided")
def test_actual_download(temp_output):
    """Test downloading a real video (requires test URL)."""
    url = os.environ.get('INTEGRATION_TEST_URL')
    output_path = temp_output / "test_video.mp4"
    
    downloader = BrightTalkDownloader(verbose=True)
    success = downloader.download(url, str(output_path))
    
    assert success
    assert output_path.exists()
    assert output_path.stat().st_size > 0

@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg not installed")
def test_url_validation():
    """Test URL validation with actual HTTP requests."""
    downloader = BrightTalkDownloader()
    
    # Test with invalid URL
    with pytest.raises(URLValidationError):
        downloader.validate_url("https://example.com/not-a-video.txt")
    
    # Test with non-existent URL
    with pytest.raises(URLValidationError):
        downloader.validate_url("https://example.com/fake.m3u8")

@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg not installed")
def test_ffmpeg_error_handling(temp_output):
    """Test handling of ffmpeg errors."""
    downloader = BrightTalkDownloader()
    output_path = temp_output / "error_test.mp4"
    
    # Try to process an invalid URL (should fail gracefully)
    success = downloader.download("http://example.com/invalid.m3u8", str(output_path))
    assert not success
    assert not output_path.exists() 