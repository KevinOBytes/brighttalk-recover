"""
BrightTalk-Recover - A tool to download BrightTalk videos from m3u8 streams.
"""

from .__version__ import __version__
from .main import BrightTalkDownloader, FFmpegNotFoundError

__author__ = "Kevin O'Connor"
__email__ = "kevin@kevinbytes.com"
__license__ = "MIT"

# Export main classes and functions
__all__ = [
    "__version__",
    "BrightTalkDownloader",
    "FFmpegNotFoundError",
]
