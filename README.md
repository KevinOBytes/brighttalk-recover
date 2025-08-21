# BrightTalk-Recover

![PyPI](https://img.shields.io/pypi/v/bt-recover)
![Python Versions](https://img.shields.io/pypi/pyversions/bt-recover)
![License](https://img.shields.io/github/license/KevinOBytes/brighttalk-recover)
![CI](https://github.com/KevinOBytes/brighttalk-recover/actions/workflows/ci.yml/badge.svg)
![Docker](https://img.shields.io/badge/ghcr.io-kevinobytes%2Fbt--recover-blue)

A Python command-line tool to download BrightTalk videos from m3u8 streams. This tool uses ffmpeg to efficiently download and process video streams.

## Features

- Download BrightTalk videos from m3u8 stream URLs
- Support for custom ffmpeg binary paths
- Progress bar for download tracking
- Dry-run mode to verify URLs before downloading
- Force mode to overwrite existing files
- Verbose logging options
- Docker support with multi-stage builds
- Environment variable support

## Requirements

- Python 3.10 or higher (tested on 3.10, 3.11, and 3.12)
- ffmpeg (runtime system requirement - not needed for installation)

### System Requirements

- Recommended OS: Ubuntu 24.04 LTS or newer
- Other Linux distributions, macOS, and Windows are also supported

### Installing ffmpeg

Note: ffmpeg is only needed when running the application, not for installing it.

#### macOS
```bash
brew install ffmpeg
```

#### Debian/Ubuntu
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows
Download the ffmpeg binaries from [ffmpeg.org](https://ffmpeg.org/download.html) and add them to your system PATH.

## Installation

### For Users (Production)
```bash
# Install from PyPI
pip install bt-recover

# Or install from source (production dependencies only)
pip install -r requirements.txt
pip install .
```

### For Developers
```bash
# Clone the repository
git clone https://github.com/KevinOBytes/brighttalk-recover.git
cd brighttalk-recover

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .

# Install pre-commit hooks
pre-commit install
```

## Usage

### Basic Usage
```bash
bt-recover --url "https://cdn.brighttalk.com/ams/california/vod/video-screencast_932117.m3u8" --output "video.mp4"
```

### Using Environment Variables
```bash
export BT_URL="https://cdn.brighttalk.com/ams/california/vod/video-screencast_932117.m3u8"
export BT_OUTPUT="video.mp4"
bt-recover
```

### Command Line Options

```
--url URL         The BrightTalk video URL (required if BT_URL not set)
--output FILE     The output file name (required if BT_OUTPUT not set)
--dry-run         Do not download, just verify the command
--force           Overwrite existing output file
--verbose         Enable verbose output
--quiet           Minimize output
--debug           Enable debug output
--ffmpeg PATH     Custom path to ffmpeg binary
--version         Show version number and exit
```

### Examples

Download with verbose output:
```bash
bt-recover --url "https://cdn.brighttalk.com/...m3u8" --output "video.mp4" --verbose
```

Use custom ffmpeg path:
```bash
bt-recover --url "https://cdn.brighttalk.com/...m3u8" --output "video.mp4" --ffmpeg "/opt/ffmpeg/bin/ffmpeg"
```

Dry run to verify URL:
```bash
bt-recover --url "https://cdn.brighttalk.com/...m3u8" --output "video.mp4" --dry-run
```

## Docker Usage

### Using Pre-built Image
```bash
docker pull ghcr.io/kevinobytes/bt-recover:latest

docker run --rm \
    -v "$(pwd):/home/appuser/output" \
    ghcr.io/kevinobytes/bt-recover:latest \
    --url "https://cdn.brighttalk.com/...m3u8" \
    --output "/home/appuser/output/video.mp4"
```

Latest image tags
- The `latest` tag is built automatically from the `main` branch by GitHub Actions.
- Release tags (e.g., `v1.2.3`) and commit `sha` tags are also pushed.

### Using Environment Variables with Docker
You can pass `BT_URL` and `BT_OUTPUT` instead of CLI flags:
```bash
export BT_URL="https://cdn.brighttalk.com/...m3u8"
export BT_OUTPUT="/home/appuser/output/video.mp4"

docker run --rm \
    -v "$(pwd):/home/appuser/output" \
    -e BT_URL -e BT_OUTPUT \
    ghcr.io/kevinobytes/bt-recover:latest
```
### Building Locally

```bash
docker build -t bt-recover .

docker run --rm -v "$(pwd):/home/appuser/output" bt-recover \
    --url "https://cdn.brighttalk.com/...m3u8" \
    --output "/home/appuser/output/video.mp4"
```

### Using Docker Compose
```bash
# For production
docker-compose up

# For development
docker-compose -f docker-compose.dev.yml up
```

## Development

### Project Structure
```
brighttalk-recover/
├── LICENSE
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── pyproject.toml
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── docker-compose.yml       # Production Docker setup
├── docker-compose.dev.yml   # Development Docker setup
├── Dockerfile
├── .pre-commit-config.yaml
├── src/
│   └── bt_recover/
│       ├── __init__.py
│       ├── __version__.py
│       ├── main.py
│       ├── cli.py           # CLI handling
│       ├── config.py        # Configuration management
│       ├── exceptions.py    # Custom exceptions
│       ├── progress.py      # Progress tracking
│       └── monitoring.py    # Performance monitoring
└── tests/
    ├── __init__.py
    ├── conftest.py         # Test fixtures
    └── test_downloader.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=bt_recover

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_downloader.py

# Run tests in Docker
docker-compose -f docker-compose.dev.yml up
```

### Code Quality Checks

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run individual checks
black src/bt_recover tests     # Code formatting
flake8 src/bt_recover tests    # Style guide enforcement
mypy src/bt_recover           # Type checking

# Run performance monitoring
python -m bt_recover.monitoring
```

### Dependencies

The project uses two requirements files:
- `requirements.txt`: Production dependencies needed to run the application
- `requirements-dev.txt`: Additional dependencies for development and testing

Key development dependencies include:
- pytest: Testing framework
- black: Code formatting
- flake8: Style guide enforcement
- mypy: Static type checking
- pre-commit: Git hooks management
- pytest-cov: Test coverage reporting
- tox: Test automation

### Configuration

The application supports various configuration methods:
1. Command line arguments
2. Environment variables
3. Configuration file (~/.bt-recover.json)

Example configuration file:
```json
{
    "ffmpeg_path": "/usr/local/bin/ffmpeg",
    "output_dir": "~/videos",
    "default_format": "mp4",
    "timeout": 30,
    "retry_attempts": 3
}
```

### Monitoring and Debugging

The application includes built-in monitoring tools:
- Progress bars for downloads
- Performance timing decorators
- Debug logging
- Error tracking

Enable debugging:
```bash
bt-recover --debug --verbose ...
```

### Docker Development

For development with Docker:

```bash
# Build and run tests
docker-compose -f docker-compose.dev.yml up

# Run specific tests
docker-compose -f docker-compose.dev.yml run bt-recover-dev pytest tests/test_downloader.py

# Run with mounted source code
docker-compose -f docker-compose.dev.yml run --rm -v .:/app bt-recover-dev
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Troubleshooting

### Common Issues

1. **ffmpeg not found**
   - Ensure ffmpeg is installed and accessible in your system PATH
   - Use the `--ffmpeg` option to specify a custom path

2. **Permission denied**
   - Ensure you have write permissions in the output directory
   - When using Docker, ensure the mounted volume has correct permissions

3. **Output file already exists**
   - Use the `--force` flag to overwrite existing files

4. **Network issues**
   - Check your internet connection
   - Verify the m3u8 URL is accessible
   - Try using `--debug` for more detailed error messages

## Support

- Open an issue on GitHub for bug reports or feature requests
- Check existing issues before creating a new one
- Include your OS, Python version, and bt-recover version when reporting issues

## Acknowledgments

- [ffmpeg](https://ffmpeg.org/) for video processing
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) for Python bindings
- [tqdm](https://github.com/tqdm/tqdm) for progress bars
