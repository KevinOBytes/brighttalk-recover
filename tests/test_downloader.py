import pytest
import os
from bt_recover.main import BrightTalkDownloader, FFmpegNotFoundError

def test_downloader_initialization():
    downloader = BrightTalkDownloader()
    assert not downloader.verbose
    assert not downloader.quiet
    assert not downloader.debug

def test_validate_url():
    downloader = BrightTalkDownloader()
    
    # Should fail with invalid URL
    with pytest.raises(ValueError):
        downloader.validate_url("not-a-url")
    
    # Should fail with non-m3u8 URL
    with pytest.raises(ValueError):
        downloader.validate_url("https://example.com/video.mp4") 

def test_ffmpeg_path_resolution():
    downloader = BrightTalkDownloader()
    assert downloader.ffmpeg_path is not None
    assert os.path.exists(downloader.ffmpeg_path)

def test_custom_ffmpeg_path():
    with pytest.raises(FFmpegNotFoundError):
        BrightTalkDownloader(ffmpeg_path="/nonexistent/ffmpeg")

def test_logging_levels():
    downloader = BrightTalkDownloader(quiet=True)
    # Should not print anything
    downloader.log("test message")
    
    downloader = BrightTalkDownloader(debug=True)
    # Should print debug messages
    downloader.log("test message", "debug")

@pytest.mark.parametrize("url,should_raise", [
    ("not-a-url", True),
    ("http://example.com/video.mp4", True),
    ("http://example.com/video.m3u8", False),
])
def test_url_validation(url, should_raise):
    downloader = BrightTalkDownloader()
    if should_raise:
        with pytest.raises(ValueError):
            downloader.validate_url(url)
    else:
        # Mock the requests.head call
        # This would require proper mocking setup
        pass 