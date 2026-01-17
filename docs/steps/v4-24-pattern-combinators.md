# V4-24: Pattern Combinators

## Overview

Implement pattern combination and layering functions.

## Objectives

1. Define stack (layer) function
2. Define cat (concatenate) functions
3. Define overlay functions
4. Define choose functions
5. Define zip functions

## Functions

```python
def stack(*patterns: Pattern) -> Pattern:
    """Layer patterns simultaneously"""

def cat(*patterns: Pattern) -> Pattern:
    """Concatenate patterns sequentially"""

def fastcat(*patterns: Pattern) -> Pattern:
    """Concatenate and speed up"""

def overlay(base: Pattern, overlay: Pattern) -> Pattern:
    """Overlay one pattern on another"""

def choose(options: list[Any], count: int | None = None) -> Pattern:
    """Randomly choose from options"""

def chooseBy(pattern: Pattern, options: list[Any]) -> Pattern:
    """Use pattern to select from options"""

def zip(patterns: list[Pattern]) -> Pattern:
    """Zip patterns together (take one from each)"""
```

## Files to Create

- `src/musicgen/patterns/combinators.py`

## Success Criteria

- [ ] All combinators working
- [ ] Proper handling of different pattern lengths
- [ ] Tests for edge cases

## Next Steps

After completion, proceed to V4-25: Polymetric Polyrhythmic Support
