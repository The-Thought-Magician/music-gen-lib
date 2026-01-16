# Step 8: Type Safety with ruff/mypy

## Objective

Ensure complete type safety across the codebase:
1. Run `ruff check` to identify and fix all type issues
2. Add proper type hints throughout
3. Configure mypy for strict type checking
4. Fix any remaining issues

## Overview

Run type checking after all code changes are complete. This is the final step to ensure code quality.

## Tasks

### 8.1 Configure ruff

Update `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
]
ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # do not perform function calls in argument defaults
    "W191",   # indentation contains tabs
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # unused imports
"tests/*" = ["ARG"]       # unused arguments in tests

[tool.ruff.lint.isort]
known-first-party = ["musicgen"]
```

### 8.2 Configure mypy

Update `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
follow_imports = "normal"
strict_equality = true

[[tool.mypy.overrides]]
module = [
    "mido.*",
    "pretty_midi.*",
    "yaml.*",
    "google.*",
    "genai.*",
]
ignore_missing_imports = true
```

### 8.3 Type Check Process

Run these commands to identify and fix issues:

```bash
# Check with ruff
ruff check src/

# Auto-fix ruff issues
ruff check --fix src/

# Check with mypy
mypy src/

# For specific file
mypy src/musicgen/ai_models/composition.py
```

### 8.4 Common Type Issues to Fix

#### Missing return types
```python
# Before
def get_note_events(self):
    return [...]

# After
def get_note_events(self) -> List[AINoteEvent]:
    return [...]
```

#### Optional handling
```python
# Before
def get_api_key(self):
    return os.environ.get("API_KEY")

# After
def get_api_key(self) -> Optional[str]:
    return os.environ.get("API_KEY")
```

#### Union types
```python
# Before
def process(note):
    if isinstance(note, AINote):
        return note.get_midi_number()
    return 0

# After
def process(note: AINoteEvent) -> int:
    if isinstance(note, AINote):
        return note.get_midi_number()
    return 0
```

#### Type narrowing
```python
# Before
def render(composition, formats):
    for fmt in formats:
        ...

# After
def render(
    composition: AIComposition,
    formats: List[str],
) -> Dict[str, Path]:
    for fmt in formats:
        ...
```

### 8.5 Add Type Stubs for External Dependencies

Create `src/musicgen/stubs/` for problematic imports if needed:

```python
# stubs/mido.pyi
from typing import Any

class Message:
    ...

class MetaMessage:
    ...

class MidiFile:
    def save(self, path: str) -> None: ...
```

### 8.6 Update All Module __init__.py Files

Ensure proper type exports:

```python
# __init__.py example
from musicgen.composer.composer import (
    AIComposer,
    ValidationError,
    compose,
    compose_from_file,
)

__all__ = [
    "AIComposer",
    "ValidationError",
    "compose",
    "compose_from_file",
]
```

### 8.7 Fix Common ruff Issues

```bash
# Run and fix
ruff check --fix src/

# Common fixes:
# - F401: Remove unused imports or add to __all__
# - UP: Upgrade syntax (e.g., typing imports)
# - I: Sort imports
# - SIM: Simplify code
# - C4: Use comprehensions
```

### 8.8 Final Validation

```bash
# 1. Ruff check (should pass)
ruff check src/

# 2. Mypy check (should pass)
mypy src/

# 3. Run tests
pytest

# 4. Build check
python -m build
```

### 8.9 Update pyproject.toml Dependencies

Ensure all type-checking tools are included:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.8.0",
    "mypy>=1.8.0",
]
```

## Deliverables

- Updated `pyproject.toml` with ruff/mypy config
- All files passing `ruff check`
- All files passing `mypy`
- Type stubs if needed

## Type Check Workflow

After making any code changes:

```bash
# 1. Auto-fix what can be fixed
ruff check --fix src/

# 2. Check remaining issues
ruff check src/

# 3. Type check
mypy src/

# 4. Fix remaining issues manually
# 5. Repeat until clean
```

## Pre-Commit Hook (Optional)

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic]
```

## Summary

After completing this step:
- All code passes ruff linting
- All code passes mypy strict type checking
- Type hints are complete and accurate
- Code is production-ready

---

## All Steps Complete!

When all 8 steps are done, the architecture will be:

```
User Prompt → AI Composer → AIComposition → Renderer → MIDI/Audio
                      ↓
                 (Schema + Gemini 2.5 Pro)
```

This is a true AI-first music generation system where the AI generates the actual note sequences, not just parameters.
