# Changelog

All notable changes to this project will be documented in this file.

## [0.1.7] - 2025-08-22

### Fixed
- CI: corrected YAML syntax and consolidated workflows.
- Style: Black formatting fixes for cli.py to satisfy CI.
- Docs: README updates (config section, tests listing, release link).
- CI: made Test PyPI workflow manual/optional to avoid accidental runs.

## [0.1.6] - 2024-01-19

### Fixed
- Removed unused imports
- Fixed line length issues
- Improved code formatting per flake8

## [0.1.5] - 2024-01-19

### Fixed
- GitHub Actions workflow permissions
- Code formatting with black
- Type checking with mypy stubs

## [0.1.4] - 2024-01-19

### Added
- Enhanced URL validation with actual HTTP checks
- Better error messages for URL validation

### Fixed
- Integration test for URL validation
- Improved error handling for network issues

## [0.1.3] - 2024-01-19

### Fixed
- Integration test compatibility with URLValidationError
- Improved test consistency across unit and integration tests

## [0.1.2] - 2024-01-19

### Fixed
- Test suite compatibility with URLValidationError
- Added missing log method to BrightTalkDownloader
- Improved test coverage

## [0.1.1] - 2024-01-19

### Added
- Integration tests
- Improved error handling
- Type hints and documentation
- Docker support
- GitHub Actions workflows
- Added version testing

### Fixed
- Version number consistency
- Test suite improvements

## [0.1.0] - 2024-01-19

### Added
- Initial release
- Basic m3u8 video downloading functionality
- Docker support
- Command-line interface 