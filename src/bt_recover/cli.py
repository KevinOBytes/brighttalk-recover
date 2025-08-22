"""Command-line interface for BrightTalk-Recover."""

import argparse
import os
import sys
from typing import List, Optional

from .exceptions import BTRecoverError, FFmpegNotFoundError, URLValidationError
from .main import BrightTalkDownloader
from . import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Download BrightTalk videos from m3u8 streams.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--url", dest="url", help="The BrightTalk m3u8 URL")
    parser.add_argument(
        "--output",
        dest="output",
        help="Output file path (e.g., video.mp4)",
    )
    parser.add_argument(
        "--ffmpeg",
        dest="ffmpeg_path",
        default=None,
        help="Custom path to ffmpeg binary",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate only")
    parser.add_argument("--force", action="store_true", help="Overwrite output file")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    parser.add_argument("--debug", action="store_true", help="Debug output")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Fallback to environment variables if flags are missing
    url = args.url or os.getenv("BT_URL")
    output = args.output or os.getenv("BT_OUTPUT")

    if not url or not output:
        parser.error("--url and --output are required (or set BT_URL and BT_OUTPUT)")

    try:
        downloader = BrightTalkDownloader(
            ffmpeg_path=args.ffmpeg_path,
            verbose=args.verbose,
            quiet=args.quiet,
            debug=args.debug,
        )

        if args.dry_run:
            downloader.validate_url(url)
            if args.verbose or args.debug:
                print("Dry run successful: URL is valid")
            return 0

        ok = downloader.download(url, output, force=args.force)
        return 0 if ok else 1
    except (BTRecoverError, FFmpegNotFoundError, URLValidationError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1
