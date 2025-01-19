# Contributing to BrightTalk-Recover

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install development dependencies: `pip install -e ".[dev]"`
5. Install pre-commit hooks: `pre-commit install`

## Running Tests

```bash
pytest
```

## Code Style

- We use Black for formatting
- MyPy for type checking
- Flake8 for linting

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Run tests and style checks
4. Update documentation if needed
5. Submit PR

## Release Process

1. Update version in `src/bt_recover/__version__.py`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. PyPI release will be automated via GitHub Actions 