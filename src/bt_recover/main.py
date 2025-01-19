import ffmpeg 
import argparse
import os
import sys
import re
import requests
import shutil
from pathlib import Path
from typing import Optional, Tuple, Literal, Union, Dict, Any
from urllib.parse import urlparse
from .__version__ import __version__
import logging

logger = logging.getLogger(__name__)

def setup_logging(verbose: bool = False, quiet: bool = False, debug: bool = False) -> None:
    """Configure logging based on verbosity settings."""
    level = logging.WARNING
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    elif quiet:
        level = logging.ERROR
        
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

class FFmpegNotFoundError(Exception):
    """Raised when ffmpeg is not found or not executable."""
    pass

class BrightTalkDownloader:
    """
    A class to handle downloading of BrightTalk videos from m3u8 streams.
    
    This class provides functionality to:
    - Validate and process m3u8 stream URLs
    - Download videos using ffmpeg
    - Handle various output formats and options
    
    Attributes:
        verbose (bool): Enable verbose output
        quiet (bool): Suppress all output except errors
        debug (bool): Enable debug logging
        ffmpeg_path (Optional[Path]): Custom path to ffmpeg binary
    """
    
    def __init__(
        self,
        verbose: bool = False,
        quiet: bool = False,
        debug: bool = False,
        ffmpeg_path: Optional[Union[str, Path]] = None
    ) -> None:
        """
        Initialize the downloader with specified options.
        
        Args:
            verbose: Enable verbose output
            quiet: Suppress all output except errors
            debug: Enable debug logging
            ffmpeg_path: Optional custom path to ffmpeg binary
            
        Raises:
            FFmpegNotFoundError: If ffmpeg is not found or not executable
        """
        self.verbose = verbose
        self.quiet = quiet
        self.debug = debug
        self.ffmpeg_path = self._resolve_ffmpeg_path(ffmpeg_path)
    
    def _resolve_ffmpeg_path(self, custom_path: Optional[str] = None) -> str:
        """
        Resolve the path to ffmpeg binary.
        
        Args:
            custom_path: Optional custom path to ffmpeg binary
            
        Returns:
            Resolved path to ffmpeg binary
            
        Raises:
            FFmpegNotFoundError: If ffmpeg is not found or not executable
        """
        # First check custom path if provided
        if custom_path:
            if self._verify_ffmpeg(custom_path):
                return custom_path
            raise FFmpegNotFoundError(f"ffmpeg not found or not executable at: {custom_path}")

        # Check if ffmpeg is in PATH
        ffmpeg_path = shutil.which('ffmpeg')
        if ffmpeg_path:
            if self._verify_ffmpeg(ffmpeg_path):
                return ffmpeg_path

        # Check common installation locations
        common_locations = [
            '/usr/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
            '/opt/homebrew/bin/ffmpeg',  # Common macOS Homebrew location
            'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',  # Windows
            'C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe',
        ]

        for location in common_locations:
            if os.path.isfile(location) and self._verify_ffmpeg(location):
                return location

        raise FFmpegNotFoundError(
            "ffmpeg not found. Please install ffmpeg or provide path using --ffmpeg option. "
            "See https://ffmpeg.org/download.html for installation instructions."
        )

    def _verify_ffmpeg(self, ffmpeg_path: str) -> bool:
        """
        Verify that the given ffmpeg path is valid and executable.
        
        Args:
            ffmpeg_path: Path to ffmpeg binary
            
        Returns:
            bool: True if ffmpeg is valid and executable
        """
        try:
            # Check if file exists and is executable
            if not os.path.isfile(ffmpeg_path) or not os.access(ffmpeg_path, os.X_OK):
                return False

            # Try to run ffmpeg -version
            result = ffmpeg.run(
                ffmpeg.input('pipe:0').output('pipe:1'),
                cmd=ffmpeg_path,
                capture_stdout=True,
                capture_stderr=True,
                input=b''
            )
            return True
        except (ffmpeg.Error, OSError):
            return False

    def _get_ffmpeg_version(self) -> Optional[str]:
        """Get ffmpeg version information."""
        try:
            result = ffmpeg.run(
                ffmpeg.input('pipe:0').output('pipe:1'),
                cmd=self.ffmpeg_path,
                capture_stdout=True,
                capture_stderr=True,
                input=b''
            )
            # Extract version from stderr
            stderr = result[1].decode()
            version_match = re.search(r'ffmpeg version (\S+)', stderr)
            return version_match.group(1) if version_match else None
        except (ffmpeg.Error, OSError):
            return None

    def log(self, message, level="info"):
        """Log messages based on verbosity settings."""
        if self.quiet and level == "info":
            return
        if level == "debug" and not self.debug:
            return
        if level == "error":
            print(message, file=sys.stderr)
        else:
            print(message)

    def validate_url(self, url):
        """Validate if URL is a valid m3u8 stream."""
        try:
            # Check if URL is well-formed
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError("Invalid URL format")

            # Check if URL points to an m3u8 file
            if not url.endswith('.m3u8'):
                raise ValueError("URL must point to an m3u8 file")

            # Try to fetch the m3u8 file
            response = requests.head(url, timeout=5)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '')
            if not any(t in content_type.lower() for t in ['application/vnd.apple.mpegurl', 'application/x-mpegurl', 'video/', 'audio/']):
                self.log(f"Warning: Unexpected content type: {content_type}", "debug")
            
            return True
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to access URL: {str(e)}")

    def download(self, url: str, output_file: str, dry_run: bool = False) -> bool:
        """
        Download the video from the m3u8 URL.
        
        Args:
            url: M3U8 stream URL
            output_file: Output file path
            dry_run: If True, only print what would be done
            
        Returns:
            bool: True if download was successful
        """
        try:
            if dry_run:
                self.log(f"Would download: {url} -> {output_file}")
                return True

            self.log(f"Downloading: {url} -> {output_file}")
            
            # Configure ffmpeg options
            stream = ffmpeg.input(url)
            
            # Add output options
            output_options = {
                'acodec': 'copy',  # Copy audio codec without re-encoding
                'vcodec': 'copy',  # Copy video codec without re-encoding
                'loglevel': 'info' if self.verbose else 'error',
            }
            
            stream = ffmpeg.output(stream, output_file, **output_options)
            
            # Add progress monitoring if verbose
            if self.verbose:
                stream = stream.global_args('-progress', 'pipe:1')
                
            # Add overwrite option
            stream = stream.overwrite_output()
            
            # Get the ffmpeg command for debugging
            args = ffmpeg.get_args(stream)
            if self.debug:
                self.log(f"FFmpeg command: {' '.join(args)}", "debug")
            
            # Run the ffmpeg command
            ffmpeg.run(
                stream,
                cmd=self.ffmpeg_path,
                capture_stdout=self.debug,
                capture_stderr=self.debug
            )
            
            return True
            
        except requests.exceptions.RequestException as e:
            self.log(f"Network error: {str(e)}", "error")
            return False
        except ffmpeg.Error as e:
            error_message = e.stderr.decode() if e.stderr else str(e)
            self.log(f"FFmpeg error: {error_message}", "error")
            return False
        except OSError as e:
            self.log(f"OS error: {str(e)}", "error")
            return False

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Download BrightTalk videos from m3u8 streams',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments with env var fallback
    parser.add_argument('--url', type=str, 
                      default=os.environ.get('BT_URL'),
                      required='BT_URL' not in os.environ,
                      help='The BrightTalk m3u8 stream URL (env: BT_URL)')
    parser.add_argument('--output', type=str,
                      default=os.environ.get('BT_OUTPUT'),
                      required='BT_OUTPUT' not in os.environ,
                      help='The output file name (env: BT_OUTPUT)')
    
    # Optional arguments
    parser.add_argument('--dry-run', action='store_true',
                      help='Do not download, just verify the URL')
    parser.add_argument('--force', action='store_true',
                      help='Overwrite output file if it exists')
    parser.add_argument('--ffmpeg', type=str,
                      help='Custom path to ffmpeg binary')
    
    # Logging options
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument('--verbose', action='store_true',
                        help='Enable verbose output')
    log_group.add_argument('--quiet', action='store_true',
                        help='Suppress non-error output')
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug output')
    
    # Version
    parser.add_argument('--version', action='version',
                      version=f'bt-recover {__version__}')
    
    return parser.parse_args()

def ensure_output_directory(output_file: str) -> None:
    """
    Ensure the output directory exists.
    
    Args:
        output_file: Path to the output file
    """
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

def main():
    """Main entry point for the application."""
    args = parse_arguments()
    
    try:
        # Initialize downloader with logging settings
        downloader = BrightTalkDownloader(
            verbose=args.verbose,
            quiet=args.quiet,
            debug=args.debug,
            ffmpeg_path=args.ffmpeg
        )
        
        if args.debug:
            version = downloader._get_ffmpeg_version()
            downloader.log(f"Using ffmpeg version: {version}", "debug")
            downloader.log(f"FFmpeg path: {downloader.ffmpeg_path}", "debug")

        # Check if output file exists
        if os.path.exists(args.output) and not args.force:
            downloader.log(f"Error: Output file {args.output} already exists. Use --force to overwrite.", "error")
            return 1

        # Validate URL
        downloader.log("Validating URL...", "debug")
        try:
            downloader.validate_url(args.url)
        except ValueError as e:
            downloader.log(f"Error: {str(e)}", "error")
            return 1

        # Ensure output directory exists
        ensure_output_directory(args.output)

        # Download the video
        if not downloader.download(args.url, args.output, args.dry_run):
            return 1

        if not args.quiet:
            downloader.log("Download completed successfully")
        return 0

    except FFmpegNotFoundError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        if args.debug:
            raise
        return 1

if __name__ == '__main__':
    sys.exit(main()) 