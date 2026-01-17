# V4-25: Polymetric Polyrhythmic Support

## Overview

Implement polymetric and polyrhythmic pattern support.

## Objectives

1. Define polymetric pattern structure
2. Support independent time signatures per part
3. Implement polyrhythm generation
4. Implement cross-ratio handling

## Implementation

```python
class PolymetricPattern:
    """Pattern with independent meter"""

    def __init__(
        self,
        patterns: dict[str, Pattern],
        meters: dict[str, tuple[int, int]]  # Part -> (num, den)
    ):
        ...

def polyrhythm(
    base: int,
    cross: int,
    length: int
) -> dict[str, Pattern]:
    """Generate polyrhythm (e.g., 3 over 4)"""

def polymetric(*patterns: tuple[Pattern, tuple[int, int]]) -> dict:
    """Create polymetric structure"""
```

## Files to Create

- `src/musicgen/patterns/polymetric.py`

## Success Criteria

- [ ] Polymetric patterns working
- [ ] Polyrhythms accurate
- [ ] Proper synchronization

## Next Steps

After completion, proceed to V4-26: Randomness Stochastic Patterns
