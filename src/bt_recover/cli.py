"""Command-line interface for BrightTalk-Recover."""

import argparse
import sys
from typing import List, Optional
from .exceptions import BTRecoverError


def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Download BrightTalk videos from m3u8 streams.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # ... argument definitions ...
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    try:
        parser = create_parser()
        _ = parser.parse_args(argv)  # Use _ for unused variable
        # ... implementation ...
        return 0
    except BTRecoverError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1
