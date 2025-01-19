"""Main module for BrightTalk-Recover."""

import os
import shutil
import subprocess
from typing import Optional
import ffmpeg
from .exceptions import FFmpegNotFoundError, URLValidationError, DownloadError
from .monitoring import timing_decorator
import requests


class BrightTalkDownloader:
    """Main downloader class."""

    def __init__(
        self,
        ffmpeg_path: Optional[str] = None,
        verbose: bool = False,
        quiet: bool = False,
        debug: bool = False,
    ) -> None:
        """Initialize the downloader."""
        self.verbose = verbose
        self.quiet = quiet
        self.debug = debug
        self.ffmpeg_path = self._resolve_ffmpeg_path(ffmpeg_path)

    def _get_ffmpeg_version(self) -> str:
        """Get ffmpeg version string."""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.split("\n")[0]
        except subprocess.CalledProcessError as e:
            raise FFmpegNotFoundError(f"Error getting ffmpeg version: {e}")

    @timing_decorator
    def download(self, url: str, output_path: str, force: bool = False) -> bool:
        """
        Download and process the video.

        Args:
            url: Source m3u8 URL
            output_path: Destination file path
            force: Overwrite existing file if True

        Returns:
            bool: True if download successful
        """
        try:
            self.validate_url(url)
            output_dir = os.path.dirname(os.path.abspath(output_path))
            os.makedirs(output_dir, exist_ok=True)

            if os.path.exists(output_path) and not force:
                msg = f"Output file already exists: {output_path}"
                raise DownloadError(msg)

            stream = ffmpeg.input(url)
            stream = ffmpeg.output(stream, output_path)

            if self.verbose:
                print(f"Starting download: {url} -> {output_path}")

            ffmpeg.run(
                stream,
                cmd=self.ffmpeg_path,
                capture_stdout=self.quiet,
                capture_stderr=self.quiet,
            )

            return True
        except Exception as e:
            if self.debug:
                print(f"Download failed: {str(e)}")
            return False

    def _resolve_ffmpeg_path(self, custom_path: Optional[str] = None) -> str:
        """Resolve the path to ffmpeg binary."""
        if custom_path and self._verify_ffmpeg(custom_path):
            return custom_path

        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path and self._verify_ffmpeg(ffmpeg_path):
            return ffmpeg_path

        msg = (
            "ffmpeg not found. Please install ffmpeg or provide path with "
            "--ffmpeg option. See https://ffmpeg.org/download.html"
        )
        raise FFmpegNotFoundError(msg)

    def _verify_ffmpeg(self, path: str) -> bool:
        """Verify that ffmpeg exists and is executable."""
        try:
            subprocess.run([path, "-version"], capture_output=True, check=True)
            return True
        except (subprocess.SubprocessError, OSError):
            return False

    def validate_url(self, url: str) -> None:
        """
        Validate the provided URL.

        Args:
            url: URL to validate

        Raises:
            URLValidationError: If URL is invalid or not accessible
        """
        if not url.endswith(".m3u8"):
            raise URLValidationError("URL must end with .m3u8")

        try:
            response = requests.head(url, timeout=10)
            if response.status_code != 200:
                raise URLValidationError(
                    f"URL returned status code {response.status_code}"
                )
        except requests.RequestException as e:
            raise URLValidationError(f"Failed to access URL: {str(e)}")

    def log(self, message: str, level: str = "info") -> None:
        """Log a message based on verbosity settings."""
        if self.quiet and level != "error":
            return
        if level == "debug" and not self.debug:
            return
        if level == "info" and not self.verbose and not self.debug:
            return
        print(f"{level.upper()}: {message}")
