"""Module entry point for `python -m bt_recover`."""

import sys
from .cli import main


if __name__ == "__main__":
    # Set proper program name when invoked as module
    if sys.argv[0].endswith("__main__.py"):
        sys.argv[0] = "bt-recover"
    raise SystemExit(main())
