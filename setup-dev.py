#!/usr/bin/env python3
"""Setup script for development environment."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=check)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"Command not found: {cmd[0]}")
        return False


def main():
    """Main setup function."""
    repo_root = Path(__file__).parent
    
    print("Setting up development environment...")
    
    # Check if we're in a git repository
    if not (repo_root / ".git").exists():
        print("Error: Not in a git repository")
        return 1
    
    # Install pre-commit hooks if pre-commit is available
    if run_command(["pre-commit", "--version"], check=False):
        print("Installing pre-commit hooks...")
        if run_command(["pre-commit", "install"]):
            print("✓ Pre-commit hooks installed successfully")
        else:
            print("✗ Failed to install pre-commit hooks")
    else:
        print("pre-commit not installed. Install with: pip install pre-commit")
    
    print("\nDevelopment environment setup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements-dev.txt")
    print("2. Install package in development mode: pip install -e .")
    print("3. Run tests: pytest")
    print("4. Run pre-commit on all files: pre-commit run --all-files")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())