# V4-23: Pattern Transformation Functions

## Overview

Implement pattern transformation functions inspired by TidalCycles.

## Objectives

1. Define time transformation functions
2. Define reversal functions
3. Define rotation functions
4. Define repetition/variation functions
5. Define degradation functions

## Functions

```python
# Time transformations
def slow(pattern: Pattern, factor: float) -> Pattern:
    """Slow down pattern by factor"""

def fast(pattern: Pattern, factor: float) -> Pattern:
    """Speed up pattern by factor"""

def density(pattern: Pattern, factor: float) -> Pattern:
    """Change event density"""

# Reversal
def rev(pattern: Pattern) -> Pattern:
    """Reverse pattern"""

def palindrome(pattern: Pattern) -> Pattern:
    """Create palindrome (forward + reverse)"""

# Rotation
def rotate(pattern: Pattern, offset: int) -> Pattern:
    """Rotate pattern by offset"""

# Repetition
def repeat(pattern: Pattern, count: int) -> Pattern:
    """Repeat pattern count times"""

# Degradation
def degrade(pattern: Pattern, amount: float = 0.5) -> Pattern:
    """Randomly remove events (50% by default)"""

def degrade_by(pattern: Pattern, amount: float) -> Pattern:
    """Remove events with specific probability"""

# Variation
def sometimes(
    pattern: Pattern,
    function: Callable,
    probability: float = 0.5
) -> Pattern:
    """Apply function with probability"""
```

## Files to Create

- `src/musicgen/patterns/transform.py`

## Success Criteria

- [ ] All transformations working
- [ ] Functions composable
- [ ] Tests for each function

## Next Steps

After completion, proceed to V4-24: Pattern Combinators
