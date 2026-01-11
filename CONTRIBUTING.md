# Contributing to MusicGen

Thank you for your interest in contributing to MusicGen! This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming community for all contributors.

## How to Contribute

### Reporting Bugs

Report bugs via GitHub Issues with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (Python version, OS)
- Minimal code example if applicable

### Suggesting Features

Feature suggestions are welcome! Please include:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach (if known)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass
5. Update documentation as needed
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/music-gen-lib.git
cd music-gen-lib

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (if configured)
pre-commit install
```

## Coding Standards

### Style Guide

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints for function signatures

### Documentation

- Use Google-style docstrings
- Document all public classes and functions
- Include examples for complex functionality

```python
def generate_melody(scale: Scale, length: int) -> Melody:
    """Generate a melody from the given scale.

    Args:
        scale: The scale to use for note selection
        length: Number of notes to generate

    Returns:
        A Melody object containing the generated notes

    Example:
        >>> scale = Scale("C", "major")
        >>> melody = generate_melody(scale, 16)
        >>> len(melody.notes)
        16
    """
```

### Testing

- Write tests for all new functionality
- Aim for >80% code coverage
- Use descriptive test names
- Include edge cases and error conditions

```python
def test_generate_melody_with_valid_scale():
    """Test melody generation with a valid scale."""
    scale = Scale("C", "major")
    melody = generate_melody(scale, 8)

    assert len(melody.notes) == 8
    assert all(n.name in scale.notes for n in melody.notes)
```

## Project Structure

```
src/musicgen/
├── core/           # Fundamental classes (Note, Chord)
├── theory/         # Music theory (Scale, Key, Progression)
├── composition/    # Composition (Melody, Form)
├── orchestration/  # Instruments and ensembles
├── io/             # Export (MIDI, MusicXML, LilyPond, audio)
├── config/         # Configuration and presets
└── generator.py    # Main generation interface
```

## Adding Features

### New Scale Types

1. Add to `ScaleType` enum in `src/musicgen/theory/scales.py`
2. Add interval pattern to `INTERVALS` dictionary
3. Add tests in `tests/test_scales.py`
4. Update documentation

### New Moods

1. Add preset to `MOOD_PRESETS` in `src/musicgen/config/moods.py`
2. Add tests in `tests/test_moods.py`
3. Update README mood table

### New Export Formats

1. Create writer class in appropriate `io/` module
2. Implement required interface methods
3. Add comprehensive tests
4. Update documentation with usage examples

## Submitting Changes

### Before Submitting

- Run full test suite: `pytest`
- Check coverage: `pytest --cov`
- Format code: `black .`
- Lint: `flake8` or `ruff`

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] Coverage maintained or improved
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] PR description explains changes

## Getting Help

- Open an issue for bugs or questions
- Check existing documentation
- Browse example code

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
