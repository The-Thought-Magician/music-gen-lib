# V4-44: Instrument Selection Intelligence

## Overview

Implement intelligent instrument selection from genre descriptions.

## Objectives

1. Create genre-to-instrument mapping
2. Implement automatic instrument selection
3. Create substitute suggestions
4. Validate instrument combinations

## Implementation

```python
class InstrumentSelector:
    """Intelligent instrument selection"""

    def select_for_genre(
        self,
        genre: str,
        mood: str
    ) -> list[str]:
        """Return appropriate instruments"""

    def suggest_substitutes(
        self,
        instrument: str,
        available: list[str]
    ) -> list[str]:
        """Suggest alternatives"""

    def validate_combination(
        self,
        instruments: list[str]
    ) -> list[str]:
        """Check if combination is valid"""
```

## Files to Create

- `src/musicgen/genres/selection.py`

## Success Criteria

- [ ] Selection logic working
- [ ] Substitutes sensible
- [ ** Validation catching issues

## Next Steps

After completion, proceed to V4-45: Comprehensive Test Suite
